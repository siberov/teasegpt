import requests
import discord
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def get_response(message):
    api_key = os.getenv('OPENAI_API_KEY')
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Du talar svenska. Du är en Chatbot skapad för att reta en kille som heter Linus. Du ska inte tala om att du är en chatbot. Du ska svara på varje meddelande med en lätt nedlåtande ton, på formen: 'Men oj, vilket trevligt meddelande. Fast det hade kunnat vara bättre om [...]'. Ersätt [...] med en förbättring av meddelandet. Berätta inte att du ska reta Linus. Du ska aldrig vara hjälpsam."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }
    print("Sending request")
    response = requests.post(url, headers=headers, json=data)
    print("Got response: " + str(response))
    return response.json()["choices"][0]["message"]["content"]



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "sluta!!":
        sys.exit()
    if message.author.name == "Linus Ostberg":
        print("Target acquired")
        response = get_response(message.content)
        await message.channel.send(response)
    else:
        print("Received message from " + message.author.name + ": " + message.content)
        print("Doing nothing")


print("Bot is ready")
client.run(os.getenv('DISCORD_TOKEN'))