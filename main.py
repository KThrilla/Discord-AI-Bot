import discord
import os
import openai
#from keep_alive import keep_alive
from replit import db

client = discord.Client()
openai.api_key = os.getenv("OPENAI_API_KEY")

humanLine = "\nHuman: " 
aiLine = "\nAI:"

db["prompt"] = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?"

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  db["prompt"] = db["prompt"] + humanLine + message.content + aiLine

  response = openai.Completion.create(
    engine="davinci",
    prompt=db["prompt"],
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=["\n", " Human:", " AI:"]
  )

  await message.channel.send(response.choices[0].text)
  db["prompt"] = db["prompt"] + response.choices[0].text

  print()
  print(db["prompt"])


#keep_alive()
client.run(os.environ['BotToken'])