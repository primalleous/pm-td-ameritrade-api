from configparser import ConfigParser
from td.client import TdAmeritradeClient
from td.credentials import TdCredentials

# Initialize the `TdAmeritradeClient`
td_client = TdAmeritradeClient()


# TODO: Old way currently doesn't work (i.e. without config env variable, need to investigate)

# # Initialize the Parser.
# config = ConfigParser()
# # Read the file.
# config.read("config/config.ini")
# # Get the specified credentials.
# client_id = config.get("main", "client_id")
# redirect_uri = config.get("main", "redirect_uri")
# # Intialize our `Credentials` object.
# td_credentials = TdCredentials(
#     client_id=client_id,
#     redirect_uri=redirect_uri,
#     credential_file="config/td_credentials.json",
# )
# # Initalize the `TdAmeritradeClient`
# td_client = TdAmeritradeClient(credentials=td_credentials)
