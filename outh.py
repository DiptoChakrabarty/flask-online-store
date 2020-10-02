import os 
from flask import g  #this can hold variables globally inside the whole app 
from flask_oauthlib.client import OAuth
from dotenv import load_dotenv
load_dotenv()

oauth = OAuth()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CILENT_SECRET")
#print(client_id,client_secret)

github = oauth.remote_app(
    'github',
    consumer_key= client_id,
    consumer_secret = client_secret,
    request_token_params = {"scope": "user:email"},
    base_url="https://api.github.com/",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url= "https://github.com/login/oauth/authorize"
)


#pass the access token to the github user object
@github.tokengetter
def get_github_token():
    if "access_token" in g:
        return g.access_token