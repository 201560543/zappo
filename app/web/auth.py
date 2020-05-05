from authlib.integrations.flask_client import OAuth 

auth0 = OAuth()

def create_auth(app):
    """
    Initialize Auth0
    """
    # Initialize auth0
    global auth0
    oauth = OAuth(app)
    auth0 = oauth.register(
        'auth0',
        client_id='6s0USrL78smCn92sPwDt6m5ezfiq1sIG',
        client_secret='ti0eaqYemFhWpzGkbvFPFKnn54CXKbN1tX2T9gRr4GPsh84O4OAnWuKWewOS45Zs', # TO DO: UPDATE
        api_base_url='https://patdeguz.auth0.com', # TO DO: UPDATE
        access_token_url='https://patdeguz.auth0.com/oauth/token', # TO DO: UPDATE
        authorize_url='https://patdeguz.auth0.com/authorize', # TO DO: UPDATE
        client_kwargs={
            'scope': 'openid profile email',
        },
    )