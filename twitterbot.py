import tweepy
import random
import requests
import os

# for acct in account_list:
# 	user = api.get_user(acct)
# 	# print(user.__dict__)

def get_api():
	consumer_key 	= os.getenv('CONSUMER_KEY')
	consumer_secret = os.getenv('CONSUMER_SECRET')
	access_token 	= os.getenv('ACCESS_TOKEN')
	access_secret 	= os.getenv('ACCESS_SECRET')

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	return tweepy.API(auth)	

def tweet_image(api, url, message):
	# api = get_api()
	file_name = 'temp.jpg'
	request = requests.get(url, stream=True)
	if request.status_code == 200:
		with open(file_name, 'wb') as image:
			for chunk in request:
				image.write(chunk)
		api.update_with_media(file_name, status=message)
	else:
		print("Unable to download image.")

if __name__ == "__main__":
	api = get_api()

	with open('pokemon.txt') as f:
		pokeymans = [line.strip() for line in f]

	choice = random.choice(pokeymans)
	print(choice)

	tweet_body 	= "A wild " + choice + " appears!"
	image_url 	= 'https://i.imgur.com/Zq0iBJKg.jpg'
	# api.update_status("A wild "+choice+" appears!")
	tweet_image(api, image_url, tweet_body)
