import discord
import sys

args = sys.argv[1:]
lines = []
for arg in args:
	arg = "".join(arg)
	lines.append(arg)
lines = " ".join(lines)
user_id = 354992856609325058

client = discord.Client()

@client.event
async def on_ready():
	print("Logged in as {0.user}".format(client))
	channel = client.get_channel(776350436634394624)
	await channel.send(lines)
	
	activity = discord.Activity(name="Ian's Plex Server", type=discord.ActivityType.watching)
	await client.change_presence(activity=activity)
	quit()

client.run("BOT_TOKEN_HERE")
quit()