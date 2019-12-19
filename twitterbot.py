import tweepy
import random
import requests
import os

from PIL import Image

def get_api():
	consumer_key 	= os.getenv('CONSUMER_KEY')
	consumer_secret = os.getenv('CONSUMER_SECRET')
	access_token 	= os.getenv('ACCESS_TOKEN')
	access_secret 	= os.getenv('ACCESS_SECRET')

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	return tweepy.API(auth)	

def tweet_image(api, url, message):
	file_name = 'temp.png'
	request = requests.get(url, stream=True)
	if request.status_code == 200:
		with open(file_name, 'wb') as image:
			for chunk in request:
				image.write(chunk)
		resize_png(file_name)
		api.update_with_media(file_name, status=message)
	else:
		print("Unable to download image.")

def generate_dict(link_file):
	with open(link_file) as f:
		link_dict = {}
		for line in f:
			(key, val) = line.split('|')
			link_dict[key] = val.strip()
		return link_dict

def resize_png(file_name):
	im = Image.open(file_name)
	newsize = (256, 256)
	im_out = im.resize(newsize)
	im_out.save(file_name)

if __name__ == "__main__":

	# API setup
	api = get_api()
	
	# Read text file to generate pokemon->icon dict
	link_dict = generate_dict('pokemon_links.txt')
	
	# Create list of pokemon
	with open('pokemon.txt') as f:
		pokeymans = [line.strip() for line in f]

	# Choose random one and construct tweet body, image link
	choice  = raw_input("Enter pokeyman: ")
	if choice not in pokeymans:
		choice = random.choice(pokeymans)
	tweet_body 	= "Wild #" + choice.upper() + " appeared!"
	image_url 	= link_dict[choice]
	
	print(tweet_body)
	tweet_image(api, image_url, tweet_body)