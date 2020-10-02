"""
    Preset configurations based on environment
    example: Flask().config.from_object('config.className')
"""


class Config(object):
    """ Default Class of what should be defined in children """
    DEBUG = None
    TESTING = None


class DevelopmentConfig(Config):
    """ For use with flask run to catch application errors """
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """ For use with production server handler and test the application with pytest"""
    DEBUG = False
    TESTING = True


class ProductionConfig(Config):
    """ For deployments to production server """
    DEBUG = False
    TESTING = False
