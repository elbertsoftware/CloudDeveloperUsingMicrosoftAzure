import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    DEBUG = True

    POSTGRES_URL = 'techconfdbserver.postgres.database.azure.com'  # TODO: Update value
    POSTGRES_DB = 'techconfdb'  # TODO: Update value
    POSTGRES_USER = 'dbadmin@techconfdbserver'  # TODO: Update value
    POSTGRES_PW = 'Postgres65432!'  # TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'

    SERVICE_BUS_CONNECTION_STRING = 'Endpoint=sb://techconfservicebus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=IDtMFj+4w+sNj2fxDtNq3ihyjkREMRSHm6wncp0Qgmc='  # TODO: Update value
    SERVICE_BUS_QUEUE_NAME = 'notificationqueue'

    ADMIN_EMAIL_ADDRESS = 'info@techconf.com'
    # Configuration not required, required SendGrid Account
    SENDGRID_API_KEY = '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'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
