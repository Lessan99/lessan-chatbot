import discord
import os
from dotenv import load_dotenv


intents = discord.Intents.all()
client = discord.Client(intents=intents)


import math
from openai import OpenAI
import base64
load_dotenv()
openAiClient=OpenAI(api_key=os.getenv('OPEN_API_KEY'))

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author ==client.user:
    return

  elif message.content.startswith('$ask:'):
      if message.author.id != os.getenv('DISCORD_ID'):
          await message.channel.send("You are not authorized to use this command")
          return
      print("message received: "+message.content)
      response = openAiClient.responses.create(model=os.getenv('ASK_MODEL'),input=message.content[5:]).output_text
      print(response)
      if(len(response) <=2000):
          await message.channel.send(response)
      else:
          parts = [response[i:i + 2000] for i in range(0, len(response), 2000)]
          for part in parts:
              await message.channel.send(part)


  elif message.content.startswith('$gen:'):
      if message.author.id != os.getenv('DISCORD_ID'):
          await message.channel.send("You are not authorized to use this command.")
          return
      print("message received: "+message.content)
      img=openAiClient.images.generate(model=os.getenv('GEN_IMAGE_MODEL'),prompt=message.content[5:],n=1,size="1024x1024")
      image_bytes=base64.b64decode(img.data[0].b64_json)
      with open("output.png","wb") as f:
               f.write(image_bytes)
               f.close
    



client.run(os.getenv('DISCORD_TOKEN'))

