class Config:
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
            #self.__setattr__(k, kwargs[k])

class InvalidConfig(Exception):
    pass
