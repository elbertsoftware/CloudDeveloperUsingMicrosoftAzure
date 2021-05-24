import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'

    # Blob storage account name
    BLOB_ACCOUNT = os.environ.get(
        'BLOB_ACCOUNT') or 'articlecmsblob'

    # Blob storage access key
    BLOB_STORAGE_KEY = os.environ.get(
        'BLOB_STORAGE_KEY') or 'TgjW0Q2L7ejI0d3t55eR+SGfTYnfYQX7BIRH3mFIcfCW4FVY4UoSeXiws1jlBVHcqrNxDCJaBeXoIO+grwiGfg=='

    # Container name under the blob storage
    BLOB_CONTAINER = os.environ.get(
        'BLOB_CONTAINER') or 'images'

    # Database server name (in full)
    SQL_SERVER = os.environ.get(
        'SQL_SERVER') or 'articlecmsserver.database.windows.net'

    # Database name
    SQL_DATABASE = os.environ.get('SQL_DATABASE') or 'articlecmsdb'

    # Database username and password
    SQL_USER_NAME = os.environ.get(
        'SQL_USER_NAME') or 'sqladmin'
    SQL_PASSWORD = os.environ.get(
        'SQL_PASSWORD') or 'art!cl3cms'

    # Below URI may need some adjustments for driver version, based on your OS, if running locally
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://' + SQL_USER_NAME + '@' + SQL_SERVER + ':' + \
        SQL_PASSWORD + '@' + SQL_SERVER + ':1433/' + \
        SQL_DATABASE + '?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ### Info for MS Authentication ###
    ### As adapted from: https://github.com/Azure-Samples/ms-identity-python-webapp ###
    # articlecms app client secret
    CLIENT_SECRET = "n3lVS5-UINSx-vfBQNq52._OEo2cYZ14Kg"  # Client secret's value
    # Client secret's id: 9c03c446-b6ab-45a3-a24c-97ac51974559

    # In your production app, Microsoft recommends you to use other ways to store your secret,
    # such as KeyVault, or environment variable as described in Flask's documentation here:
    # https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
    # CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    # if not CLIENT_SECRET:
    #     raise ValueError("Need to define CLIENT_SECRET environment variable")

    # For multi-tenant app, else put tenant name
    AUTHORITY = "https://login.microsoftonline.com/common"
    # AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

    # articlecms application (client) id
    CLIENT_ID = "63c4c52a-cf51-4aff-b825-4538d2581ebd"

    # Used to form an absolute URL; must match to app's redirect_uri set in AAD
    REDIRECT_PATH = "/getAToken"

    # You can find the proper permission names from this document
    # https://docs.microsoft.com/en-us/graph/permissions-reference
    SCOPE = ["User.Read"]  # Only need to read user profile for this app

    SESSION_TYPE = "filesystem"  # Token cache will be stored in server-side session
