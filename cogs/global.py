import discord
from discord.ext import tasks, commands
from datetime import datetime
from random import choice
import json


class general(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self,message):
		if message.content in ['a','ah','AH','A','ah!','AH!']:
			file = 'assets/ah.jpg'
		if message.content in ["mais oui c'est clair",'mais ui c clair','mais oui c clair','mais oui c claire',"oui c'est clair",'oui c clair',"MAIS OUI C CLAIR","MAIS OUI C'EST CLAIR","Mais oui c'est clair","Mais ui c clair","Mais oui c clair","Oui c clair","Oui c'est clair"]:
			file = 'assets/maisouicclair.jpg'
		if message.content in ['rip',"rip in peace","RIP"]:
			file = 'assets/rip.png'
		if message.content in ['yee']:
			file = 'assets/yee.jpg'
		try:
			await message.channel.send(file=discord.File(file))
			await message.delete()
		except:
			pass

	@commands.command(help='your beautiful face')
	async def avatar(self,ctx,mention:discord.Member=None):
		await ctx.message.delete()
		avatar = mention.avatar_url if mention != None else ctx.author.avatar_url
		await ctx.send(avatar)

	@commands.command(help='shows the differents memes available')
	async def memes(self,ctx):
		await ctx.send(embed=discord.Embed(title="the bot replace your message by a picture",description="Denis brogniart : 'a','ah','AH','A','ah!','AH!'\nEddy Malou : "+"'mais oui c'est clair'"+"'mais ui c clair','mais oui c clair','mais oui c claire',"+"'oui c'est clair'"+"'oui c clair','MAIS OUI C CLAIR','MAIS OUI C'EST CLAIR'\nyee : 'yee'",color = discord.Color(0xFFCC00)))

def setup(client):
	client.add_cog(general(client))