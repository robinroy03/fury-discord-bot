import discord

import os
import requests

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents = intents)
token = os.environ.get('TOKEN_DISCORD')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="help", description="list of commands and other info.")
async def help(ctx: discord.ApplicationContext):
    await ctx.respond("Hello! FURY Bot responds to all your messages\
                      \n1)Inside Forum channel and\
                      \n2)Those that tag the bot.")

@bot.event
async def on_message(message):
    url = 'http://127.0.0.1:8000/completion'
    obj = {'user': message.author.id,
           'text': message.content.replace("<@1243428204124045385>", "")}

    if (message.author != bot.user) and (bot.user.mentioned_in(message)):
        await message.reply(content="Your message was received, it'll take around 10 seconds for FURY to process an answer.")

        try:
            return_obj = requests.post(url, json=obj)
            print(return_obj.text)
            await message.reply(content=return_obj.text)
        except requests.exceptions.RequestException as e:
            print(e)
            await message.reply(content="Sorry something internally went wrong. Retry again.")


bot.run(token)