def demo(*args, **kwargs):
    print "***************** - ", args
    print kwargs['a']

demo(1, a=1, b=2)