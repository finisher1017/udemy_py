import constants
import oauth2
import urllib.parse as urlparse
import json
from user import User
from database import Database

Database.initialise()

# Create a consumer, which uses CONSUMER_KEY and CONSUMER_SECRET to identify our app uniquely
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)

# Use the client to perform a request for the request token 
response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
if response.status != 200:
    print("An error occured")

# Get the request token parsing the query string returned
request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

# login with twitter button
# choose "Sign In" with twitter
# Twitter sends back to our website
# We get auth code

# Ask the user to authorize our app and give us the pin code
print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

oauth_verifier = input("What is the PIN? ")

# Creae a Token object which contains the request token, and the verifier
token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)

# Create a client with our consumer (our app) and the newly (and verified) token
client = oauth2.Client(consumer, token)

# Ask Twitter for an access token, and Twitter knows it should give us it because we've verified the request token
response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

print(access_token)

email = input("Enter your email: ")
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
    
my_user = User(email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
my_user.save_to_db()

# Create an 'authorized_token' Token object and use that to perform Twitter API calls on behalf of the user
authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
authorized_client = oauth2.Client(consumer, authorized_token)

# Make Twitter API calls!
response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images', 'GET')
if response.status != 200:
    print("An error occured when searching!")

tweets = json.loads(content.decode('utf-8'))

for tweet in tweets['statuses']:
    print(tweet['text'])

