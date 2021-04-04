import discord
from discord.ext import tasks, commands
from datetime import datetime
from random import choice
import json
import os

class newgame(object):
	def __init__(self,date,creator,channel,cround,cnote,trounds,player,level,language):
		self.date = date
		self.creator = creator
		self.channel = channel
		self.round = cround
		self.cnote = cnote
		self.trounds = trounds
		self.players = {}
		self.players[player.id] = [0,player]
		self.level = level
		self.isplaying = False
		self.language = language

def current_date(e):
	date = str(datetime.now())
	a = {"full":date,"date":date.split(' ')[0],
		"time":date.split(' ')[1],
		"day":date.split(' ')[0].split('-')[2],
		"month":date.split(' ')[0].split('-')[1],
		"year":date.split(' ')[0].split('-')[0],
		"hour":date.split(' ')[1].split(':')[0],
		"minutes":date.split(' ')[1].split(':')[1],
		"seconds":date.split(' ')[1].split(':')[2]}
	return a[e]

def init_game():
	notes = {}
	for filename in os.listdir(f'{notes_dir}'):
		if filename.endswith('.json'):
			notes1 = {}
			notes2 = {}
			with open(f'{notes_dir}/{filename}','rb') as infile:
				notes3 = json.load(infile)
				for i in notes3.keys():
					if not '#' in i:
						if '4' in i:
							notes1[i] = notes3[i]
						notes2[i] = notes3[i]
				notes[f"{filename[:-5]}"] = [notes1,notes2,notes3]
	return notes

async def play_note(ctx,game):
	if game.round < game.trounds:
		note = choice(tuple(notes[game.language][game.level-1]))
		game.cnote = note
		game.round += 1
		await ctx.send(file=discord.File(f'{notes[game.language][game.level-1][note]}'))
	else:
		await stop_game(ctx,game)	

async def stop_game(ctx,game):
	desc = f"{crown_emoji}\t"
	player_list = game.players.copy()
	for player_x in player_list:
		best_score = [0,None,None]
		for player in game.players:
			if game.players[player][0] > best_score[0]:
				best_score[0] = game.players[player][0]
				best_score[1] = game.players[player][1].mention
				best_score[2] = player
		desc += f'\t{best_score[1]} : {best_score[0]}\n'
		del game.players[best_score[2]]
	embed = discord.Embed(title="scores",description=desc,color = discord.Color(0xFFCC00))
	embed.set_footer(text='gg everyone')
	await ctx.send("game is finished !!",embed=embed)
	games.remove(game)


crown_emoji = "👑"
games = []
notes_dir = "notes"
notes = init_game()


class perfect_pitch(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self,message):
		try:
			for game in games:
				if game.channel == message.channel and message.content in game.cnote and message.author.id in game.players:
					game.players[message.author.id][0] += 1
					await message.channel.send(embed=discord.Embed(description=f"gg {message.author.mention}, you got 1 point",color = discord.Color(0xFFCC00)))
					await play_note(message.channel,game)
		except:
			pass

	@commands.command()
	async def ppcreate(self,ctx,level:int=1,rounds=10,language='en'):
		if 0 < level < 4:
			found = False
			for game in games:
				if game.channel	== ctx.channel:
					found = True
			if found == False:
				if language in ["en","fr"]:
					games.append(newgame(current_date('full'),ctx.author,ctx.channel,0,None,rounds,ctx.author,level,language))
					await ctx.send(embed=discord.Embed(title='game sucessfully created !',description='type\n*join to join the game\n*players to see who is playing\n*game-info to see the game details\n*start to start the game\n*current-round to see the current round',color = discord.Color(0xFFCC00)))
				else:
					await ctx.send(embed=discord.Embed(title="wrong language",color = discord.Color(0xFFCC00)))
			else:
				await ctx.send(embed=discord.Embed(title="a game in already launched in this channel",color = discord.Color(0xFFCC00)))
		else:
			await ctx.send(embed=discord.Embed(title='choose a level between 1 , 2 and 3 please',color = discord.Color(0xFFCC00)))

	@commands.command()
	async def join(self,ctx):
		for game in games:
			if not ctx.author.id in game.players.keys() and ctx.channel == game.channel and game.isplaying == False:
				game.players[ctx.author.id] = [0,ctx.author]
				await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} is playing',color = discord.Color(0xFFCC00)))

	@commands.command()
	async def players(self,ctx):
		for game in games:
			if ctx.channel == game.channel:
				desc = f''
				for player in game.players:
					desc += f'{game.players[player][1].mention}\n'
				await ctx.send(embed=discord.Embed(title='players:',description=desc,color = discord.Color(0xFFCC00)))

	@commands.command(name="game-info")
	async def game_info(self,ctx):
		for game in games:
			if game.channel == ctx.channel:
				embed = discord.Embed(title=f"game informations",color = discord.Color(0xFFCC00))
				embed.set_author(name=f"game created by {game.creator.name}",icon_url=game.creator.avatar_url)
				embed.add_field(name= "level",value=game.level,inline= True)
				embed.add_field(name= "total rounds",value=game.trounds,inline= True)
				embed.add_field(name= "number of players",value=len(game.players),inline= True)
				embed.set_footer(text=game.date)
				await ctx.send(embed=embed)

	@commands.command()
	async def start(self,ctx):
		for game in games:
			if game.channel == ctx.channel and ctx.author == game.creator:
				game.isplaying = True
				await play_note(ctx,game)

	@commands.command()
	async def stop(self,ctx):
		for game in games:
			if game.channel == ctx.channel and ctx.author == game.creator:
				await stop_game(ctx,game)

	@commands.command(name="current-round")
	async def current_round(self,ctx):
		for game in games:
			if game.channel == ctx.channel:
				await ctx.send(embed=discord.Embed(title=f"current round : {game.round}",color = discord.Color(0xFFCC00)))

def setup(client):
	client.add_cog(perfect_pitch(client))