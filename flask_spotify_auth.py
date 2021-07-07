import base64, json, requests

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'
RESPONSE_TYPE = 'code'   
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''
ENCODED = ''
    
def getAuth(client_id, redirect_uri, scope):
    data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, client_id, redirect_uri, scope) 
    return data

def getToken(code, client_id, client_secret, redirect_uri):
    global ENCODED
    body = {
        "grant_type": 'authorization_code',
        "code" : code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    data_string = client_id + ":" + client_secret
    data_bytes = data_string.encode("utf-8")
     
    encoded = base64.urlsafe_b64encode(data_bytes).decode("utf-8")
    ENCODED = encoded
    headers = {"Content-Type" : HEADER, "Authorization" : "Basic {}".format(encoded)} 
    post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)
    print(post.text)
    print("!!!")
    return handleToken(json.loads(post.text))
    
def handleToken(response):
    #print(response)
    print(response)
    print("YEYEYEYEYEYYE")
    auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
    # REFRESH_TOKEN = response["refresh_token"]
    #print('hellooooooo')
    #print(response["refresh_token"])
    if (response.get('refresh_token')):
        return [response["access_token"], auth_head, response["scope"], response["expires_in"], response["refresh_token"]]
    else:
        return [response["access_token"], auth_head, response["scope"], response["expires_in"]]

def refreshAuth(refresh_token):
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : refresh_token
    }
    print("Basic {}".format(ENCODED))
    print('!!!!')
    headers = {"Content-Type" : HEADER, "Authorization" : "Basic {}".format(ENCODED)} 
    post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=headers)
    p_back = json.loads(post_refresh.text)
    print(post_refresh.text)
    print('!!!!!!!!!!!')
    
    return handleToken(p_back)
