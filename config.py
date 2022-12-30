import os


class TestConfig:
    FLASK_ENV = "development"
    TEMPLATES_AUTO_RELOAD = True
    TESTING = True
    DEBUG = True

    SECRET_KEY = "superdupersecretysecretkey"

class ProdConfig:
    FLASK_ENV = "production"
    TESTING = False
    DEBUG = False

    SERVER_NAME = "text2notes.com"

    SECRET_KEY = "superdupersecretysecretkey"

