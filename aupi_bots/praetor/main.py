import discord, random, os, json
from discord.ext import commands
from discord.ext import commands
from ...utility import Utility


#######################################################
# % DEFINE INTENTS AND CLIENT
#######################################################
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='7', intents=intents)
client.remove_command('help')



#######################################################
# % LOAD COMMANDS
#######################################################
client.load_extension('cogs.cmds_general')
client.load_extension('cogs.cmds_moderation')
client.load_extension('cogs.gateway')


#######################################################
# GIVE NOTIFICATION IN CONSOLE THAT BOT IS ONLINE
#######################################################
@client.event
async def on_ready():
	print("\n\n-------------------------\nBOT IS ONLINE\n-------------------------\n\n")

	# Remove all temp files
	for filename in os.listdir("temp"):
		try:
			os.remove(os.path.join("temp", filename))
		except:
			pass



#######################################################
# COMMAND USAGE LOGGING
#######################################################
@client.event
async def on_command_completion(command):
	with open("docs/json/command_statistics.json", "r") as f:
		data = json.load(f)
		
		command_name = command.command.name
		for i in data:
			for x in i:
				if x == command_name:
					i[command_name] = i[command_name] + 1
					with open("docs/json/command_statistics.json", "w") as nf:
						json.dump(data, nf, indent=4)
						nf.close()
						return
		new_command = {f"{command_name}":1}
		with open("docs/json/command_statistics.json", "w") as nf:
			data.append(new_command)
			json.dump(data, nf, indent=4)
			nf.close()
			f.close()



#######################################################
# MEMBER LEAVES SERVER
#######################################################
@client.event
async def on_member_remove(member):
	"""Sends a goodbye message to a specific channel"""

	await client.wait_until_ready()
	channel = client.get_channel(862857766804520971)

	leaveEmbed = discord.Embed(
		#title=f"{member} has joined",
		description=f"** **\n** **\n**<@{member.id}> has left**",
		color=0xFF0000
	)
	leaveEmbed.set_thumbnail(
		url=member.avatar_url
	)
	leaveEmbed.set_footer(
		text=f"{member} | {member.id}"
	)

	await channel.send(embed=leaveEmbed)



#######################################################
# ERROR HANDLING
#######################################################
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("You're missing some arguements for this command. Try again.")
		return

	if isinstance(error, commands.BotMissingPermissions):
		await ctx.send("I'm missing permissions to do this!")

	if isinstance(error, commands.ChannelNotFound):
		await ctx.send("Channel not found.")

	if isinstance(error, commands.CommandNotFound):
		return

	if isinstance(error, commands.CommandOnCooldown):
		await ctx.reply("Command on cooldown!")
		return

	if isinstance(error, commands.NotOwner):
		await ctx.send("Sorry! You're not the owner, you can't do that.")

	if isinstance(error, commands.MemberNotFound):
		await ctx.send("The member you mentioned couldn't be found... try again.")
		return

	if isinstance(error, commands.MissingRole):
		return

	if isinstance(error, commands.TooManyArguments):
		await ctx.send("That's too many arguements!")
		return

	if isinstance(error, commands.RoleNotFound):
		await ctx.send("I can't find that role! Check your spelling.")

	if isinstance(error, commands.UserNotFound):
		await ctx.send("I can't find that user.")

	if isinstance(error, commands.UserInputError):
		await ctx.send("Something you input caused an error.")
		return

	if isinstance(error, commands.ArgumentParsingError):
		return

	if isinstance(error, commands.BadArgument):
		return

	if isinstance(error, commands.BadBoolArgument):
		return

	if isinstance(error, commands.BadColourArgument):
		return

	if isinstance(error, commands.BadInviteArgument):
		return

	if isinstance(error, commands.BadUnionArgument):
		return

	if isinstance(error, commands.CommandError):
		return

	if isinstance(error, commands.CommandRegistrationError):
		return

	if isinstance(error, commands.ConversionError):
		return

	if isinstance(error, commands.EmojiNotFound):
		await ctx.send("I can't find that emoji.")
		return

	if isinstance(error, commands.ExtensionError):
		return

	if isinstance(error, commands.ExtensionAlreadyLoaded):
		return

	if isinstance(error, commands.ExtensionFailed):
		return

	if isinstance(error, commands.ExtensionNotFound):
		return

	if isinstance(error, commands.ExtensionNotLoaded):
		return

	if isinstance(error, commands.NoEntryPointError):
		return

	if isinstance(error, commands.NoPrivateMessage):
		await ctx.send("Private messages not allowed!")
		return

	if isinstance(error, commands.NSFWChannelRequired):
		await ctx.send("NSFW channel required.")
		return

	if isinstance(error, commands.PrivateChannel):
		await ctx.send("That's a private channel.")
		return

	else:
		print("Error")
		return



#######################################################
# HELP COMMANDS
#######################################################
@client.command()
async def help(ctx):
	help_embed = discord.Embed(
		title="Help",
		description = "Here is a list of all commands I have to offer"
	)
	help_embed.add_field(
		name = "7team <team>",
		value = "This command shows you a list of all staff/support on the entire server. Please replace the <team> with either the `staff` or `support` to see either list.",
		inline = False
	)
	help_embed.add_field(
		name = "7howtoask",
		value = "This command sends a message in chat with an explanation on how to properly ask questions in Aisle #7. Please use this command to show others how to properly ask a question or for you to know how to properly ask.",
		inline = False
	)

	help_embed.add_field(
		name = "7suggest <suggestion>",
		value = "This command sends a suggestion in <#865992973204193280>. It will be publically displayed to everyone, including staff. (We recommend you use this command as much as you can! Improvements are a key to a good community!)",
		inline = False
	)

	help_embed.add_field(
		name = "7ping",
		value = "This command sends a reply to you letting you know if the bot is up or not",
		inline = False
	)


	await ctx.author.send(embed=help_embed)



#######################################################
# START BOT
#######################################################
#keep_alive()
client.run(Utility.get_token("praetor")) # Available tokens: token, dev_token1, dev_token2