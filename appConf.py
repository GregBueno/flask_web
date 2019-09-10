class Config(object):
    DEBUG=False
    TESTING=False

class Development(Config):
    DEBUG=True    

class Production(Config):
    DEBUG=False