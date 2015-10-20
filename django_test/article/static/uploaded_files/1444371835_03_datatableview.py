class OperationalDeviceListingTable(PermissionsRequiredMixin, DatatableOrganizationFilterMixin, BaseDatatableView, AdvanceFilteringMixin):
    """
    Render JQuery datatables for listing operational devices only
    """
    model = Device
    required_permissions = ('device.view_device',)
    # columns are used for list of fields which should be displayed on data table.
    columns = [
        'device_name', 
        'site_instance__name', 
        'machine__name', 
        'organization__name', 
        'device_technology',
        'device_type', 
        'host_state', 
        'ip_address', 
        'mac_address', 
        'state__state_name', 
        'city__city_name'
    ]

    # order_columns is used for list of fields which is used for sorting the data table.
    order_columns = [
        '',
        'organization__name', 
        'device_name', 
        'site_instance__name', 
        'machine__name', 
        'device_technology',
        'device_type', 
        'host_state', 
        'ip_address', 
        'mac_address', 
        'state__state_name', 
        'city__city_name'
    ]

    # search_columns is used for list of fields which is used for searching the data table.
    search_columns = [
        'device_alias', 
        'site_instance__name', 
        'machine__name', 
        'organization__name', 
        'host_state',
        'ip_address', 
        'mac_address', 
        'state__state_name', 
        'city__city_name'
    ]

    # extra_qs_kwargs is used for filter the device using some extra fields in Mixin DatatableOrganizationFilterMixin.
    extra_qs_kwargs = {
        'is_deleted': 0,
        'is_added_to_nms__in': [1, 2]
    }

    def filter_queryset(self, qs):
        """
        The filtering of the queryset with respect to the search keyword entered.
        :param qs:
        :return qs:
        """
        
        sSearch = self.request.GET.get('search[value]', None)

        # If searched character is 3 or more than 3. Then search the entered text on the basis fields of search_columns.
        if sSearch:

            state_qs = State.objects.filter(state_name__icontains=sSearch)
            device_type_qs = DeviceType.objects.filter(name__icontains=sSearch)
            device_tech_qs = DeviceTechnology.objects.filter(name__icontains=sSearch)

            query_object = Q()
            for column in self.search_columns:
                query_object = query_object | Q(**{"%s__icontains" % column: sSearch})

            query_object = query_object | Q(state__in=state_qs) | Q(device_type__in=device_type_qs) | Q(
                device_technology__in=device_tech_qs)
            qs = qs.filter(query_object)

        return self.advance_filter_queryset(qs)

    def ordering(self, qs):
        """
        Get parameters from the request and prepare order by clause
        """
        order_columns = self.get_order_columns()
        return nocout_utils.nocout_datatable_ordering(self, qs, order_columns)

    def prepare_results(self, qs):
        """
        Preparing the final result after fetching from the data base to render on the data table.
        :param qs:
        :return json:
        """

        json_data = [{key: val if val else "" for key, val in dct.items()} for dct in qs]
        for dct in json_data:
            # modify device name format in datatable i.e. <device alias> (<device ip>)
            try:
                if 'device_name' in dct:
                    device_alias = Device.objects.get(pk=dct['id']).device_alias
                    device_ip = Device.objects.get(pk=dct['id']).ip_address
                    dct['device_name'] = "{} ({})".format(device_alias, device_ip)
            except Exception as e:
                logger.exception("Device not present. Exception: ", e.message)

            # current device in loop

            current_device = Device.objects.get(pk=dct['id'])

            try:
                dct['device_type__name'] = DeviceType.objects.get(pk=int(dct['device_type'])).name if dct[
                    'device_type'] else ''
            except Exception as e:
                dct['device_type__name'] = ""

            try:
                dct['device_technology__name'] = DeviceTechnology.objects.get(pk=int(dct['device_technology'])).name \
                    if dct['device_technology'] else ''
            except Exception as e:
                dct['device_technology__name'] = ""

            if current_device.is_monitored_on_nms == 1:
                status_icon_color = "green-dot"
                dct.update(status_icon='<i class="fa fa-circle {0}"></i>'.format(status_icon_color))
            else:
                status_icon_color = "light-green-dot"
                dct.update(status_icon='<i class="fa fa-circle {0}"></i>'.format(status_icon_color))

            # Following are two set of links in device list view:
            # 1. Device Actions --> Device detail, edit, delete from inventory.
            # They are always present in device table if user role is 'Admin'
            # 2. NMS Actions --> Device add, sync, service add etc. from nocout nms core.
            #                    Following are the device type present in device listing:
            #                       a. backhaul configured on (from model Backhaul)
            #                       b. sector configures on (from model Sector)
            #                       c. sub-station configured on (from model SubStation)
            #                       d. others (any device, may be out of inventory)

            # device detail action
            detail_action = '<a href="/device/{0}"><i class="fa fa-list-alt text-info" title="Detail"></i>\
                            </a>&nbsp&nbsp'.format(dct['id'])

            # view device edit action only if user has permissions
            if self.request.user.has_perm('device.change_device'):
                edit_action = '<a href="/device/{0}/edit/"><i class="fa fa-pencil text-dark"></i></a>&nbsp&nbsp'.format(
                    dct['id'])
            else:
                edit_action = ''

            # view device delete action only if user has permissions
            if self.request.user.has_perm('device.delete_device'):
                delete_action = '<a href="javascript:;" class="device_soft_delete_btn" pk="{0}">\
                                 <i class="fa fa-trash-o text-danger" title="Soft Delete"></i></a>'.format(dct['id'])
            else:
                delete_action = ''

            if edit_action or delete_action:
                dct.update(actions=detail_action + edit_action + delete_action)

            dct.update(nms_actions='')

            # text color
            text_color = "text-dark"
            try:
                if len(Backhaul.objects.filter(bh_configured_on=current_device)):
                    text_color = "text-info"
                elif len(Sector.objects.filter(sector_configured_on=current_device)) or \
                        len(Sector.objects.filter(dr_configured_on=current_device)):
                    text_color = "text-success"
                elif SubStation.objects.get(device=current_device):
                    text_color = "text-danger"
                else:
                    pass
            except Exception as e:
                pass

            try:
                dct.update(nms_actions='<a href="javascript:;" class="nms_action view" pk="{0}">\
                                        <i class="fa fa-list-alt {1}" title="Services Status"></i></a>\
                                        <a href="javascript:;" class="nms_action disable" pk="{0}">\
                                        <i class="fa fa-ban {1}" title="Disable Device"></i></a>\
                                        <a href="javascript:;" class="nms_action add" pk="{0}">\
                                        <i class="fa fa-plus {1}" title="Add Services"></i></a>\
                                        <a href="javascript:;" class="nms_action edit" pk="{0}">\
                                        <i class="fa fa-pencil {1}" title="Edit Services"></i></a>\
                                        <a href="javascript:;" class="nms_action delete" pk="{0}">\
                                        <i class="fa fa-minus {1}" title="Delete Services"></i></a>'.format(
                    dct['id'], text_color))
            except Exception as e:
                logger.exception("Device is not a substation. %s" % e.message)

            # show sync button only if user is superuser or admin
            if 'admin' in self.request.user.userprofile.role.values_list('role_name', flat=True):
                try:
                    dct['nms_actions'] += '<a href="javascript:;" onclick="sync_devices();">\
                                            <i class="fa fa-refresh {1}" title="Sync Device"></i></a>'.format(
                        dct['id'], text_color)
                except Exception as e:
                    logger.exception("Device is not a substation. %s" % e.message)
        return json_data
