from flask_spotify_auth import getAuth, refreshAuth, getToken

#Add your client ID
CLIENT_ID = "07babcfeaea747f0967bb1d5145fc21f"

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "45e1dbda55da450b808e50aaf728365b"

#Callback url can be changed
#CALLBACK_URL = "http://localhost:3334"

CALLBACK_URL = "https://spotify-stats.mybluemix.net"

#Add needed scope from spotify user
SCOPE = "user-top-read"
#streaming user-read-birthdate user-read-email user-read-private 
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}/callback/".format(CALLBACK_URL), SCOPE)

def getUserToken(code):
    return getToken(code, CLIENT_ID, CLIENT_SECRET, "{}/callback/".format(CALLBACK_URL))
    #return TOKEN_DATA
 
def refreshToken(refresh_token):
    #time.sleep(time)
    return refreshAuth(refresh_token)

def getAccessToken():
    return TOKEN_DATA

def clearTokenData():
    global TOKEN_DATA
    TOKEN_DATA = []
