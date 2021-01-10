import discord
import requests
import json
import random
import appp

client = discord.Client()

sad_words = ["sad", "depressed", "hopeless", "despairing", "miserable", "mournful", "gloomy", "heartbroken",
             "unhappy", "depressing"]
encouragements = ["Don't give up", "Keep pushing", "Stay strong", "Come on! You can do it", "Hang in there"]

def read_token():
    return appp.TK

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

def get_nasa(object):
    params = {
        "q": object,
        "page": "1",
        "media_type": "image",
        "year_start": "1920",
        "year_end": "2020"
    }
    response = requests.get("https://images-api.nasa.gov/search", params = params)
    images = response.json()["collection"]["items"]
    image = random.choice(images)
    url = image["links"][0]["href"]
    image_url = url[:url.rfind("~")] + "~orig.jpg"
    return image_url

def get_advice():
    response = requests.get("https://api.adviceslip.com/advice")
    advice = response.json()["slip"]["advice"]
    id = response.json()["slip"]["id"]
    print(id)
    return advice

token = read_token()

@client.event
async def on_ready():
    print('We have logged in {0.user}'.format(client))

@client.event
async def on_message(message):
    msg = message.content

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(encouragements))

    if message.content.startswith('$nasa'):
        list = msg.split()
        object = list[1]
        nasa = get_nasa(object)
        await message.channel.send(nasa)

    if message.content.startswith('$advice'):
        advice = get_advice()
        await message.channel.send(advice)


client.run(token)