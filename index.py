import discord
from discord.ext import tasks, commands
from datetime import datetime
from random import choice
import os
import json

class game(object):
	def __init__(self,date,creator,channel,cround,cnote,trounds,players,level):
		self.date = date
		self.creator = creator
		self.channel = channel
		self.round = cround
		self.cnote = cnote
		self.trounds = trounds
		self.players = players
		self.level = level
		self.isplaying = False

prefix = "*"

client = commands.Bot(command_prefix = prefix,activity=discord.Game(f'{prefix}help'),help_command=None)

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
        print('The bot is ready!')


client.run('')

#mettre les commandes dans une cogs sinon ca marche pas
