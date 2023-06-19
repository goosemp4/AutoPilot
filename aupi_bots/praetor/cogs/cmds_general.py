import discord, discord.utils
from discord.ext import commands
from datetime import date
from praetor_utility import PraetorUtility


class Commands(commands.Cog):
	def __init__(self, client):
		self.client = client



	#######################################################
	# PING PONG
	#######################################################
	@commands.slash_command(
		name="ping",
		description="Check if the bot is online and working"
	)
	async def ping(self, ctx):
		await ctx.respond(
			embed = discord.Embed(
			title 		= "Pong",
			description = "Online and working, if there are any issues please contact the owner",
			color 		= 0xFFFFFF
			),
			ephemeral=True
		)

	

	#######################################################
	# SUGGEST
	#######################################################
	@commands.slash_command(
		name="suggest",
		description="Suggest an idea to the server staff"
	)
	async def suggest(self, ctx, *, suggestion=None):

		if suggestion is None:
			
			# Reply with error embed
			await ctx.respond(
				embed = discord.Embed(
					title = ":x: You didn't suggest anything! Try again.",
					color = 0xFF0000
				),
				mention_author=False
			)
			return


		# Create the suggestion embed
		suggest_embed = discord.Embed(
			title 		= f"Suggestion",
			description = suggestion,
			color 		= 0xa9a9a9 
		)
		suggest_embed.set_author(
			name 	 = f"{ctx.author}",
			icon_url = ctx.author.avatar_url
		)
		suggest_embed.add_field(
			name  = "Suggested by",
			value = f"<@{ctx.author.id}>"
		)
		suggest_embed.set_footer(
			text = f"Suggested on {date.today()}"
		)
		suggest_embed.set_thumbnail(
			url = "attachment://image.png"
		)

		suggest_thumbnail_file = discord.File(f"images/gears.png", filename="image.png")
		suggestion_channel 	   = self.client.get_channel(865992973204193280)
		suggestion_message 	   = await suggestion_channel.send(file=suggest_thumbnail_file, embed=suggest_embed)

		# Reaciton emojis
		yes = "\N{WHITE HEAVY CHECK MARK}"
		no  = "\N{CROSS MARK}"

		success_embed = discord.Embed(
			title 		= f":white_check_mark: Your suggestion has been successfully recorded!",
			description = "Check <#865992973204193280>.",
			color 		= 0x77dd77
		)

		await ctx.respond(embed=success_embed, mention_author=False, ephemeral=True)
		await suggestion_message.add_reaction(yes)
		await suggestion_message.add_reaction(no)
			


	#######################################################
	# HOW TO ASK
	#######################################################
	@commands.slash_command(
		name 		= "howtoask",
		description = "Provides an explanation on how to properly ask a question in Aisle #7"
	)
	async def howtoask(self, ctx):

		howtoask = discord.Embed(
			title 		= "Asking for Support",
			description = "When asking for support in any of the support channels, you want to make the job of the support as easy as possible. This is so you can get help faster and so there is less questions being thrown around. What you can do is read all of the sections of this message, to confirm that you have the most proper and contextual question making it easy to help you.\n\nPlease use the `/callsupport` command to request help from our dedicated support team.",
			color 		= 0xa94bf0
		)
		howtoask.add_field(
			name  = "Describe the Problem",
			value = "When you are going to ask for help, please describe the problem. Be specific. If you need help with something, please lay out the entire problem in the message, even if it's so long it's a short story! It's much easier for someone to help you when they don't have to play 20 questions with you."
		)
		howtoask.add_field(
			name  = "Show Your Work",
			value = "You need to provide what you have so far code-wise. Please provide this code in your post via screenshot or copy-paste (preferrably copy-paste). This allows someone to get an understanding of what you were doing and how you got to the issue. You are expected to provide code when you post in any coding support channel."
		)
		howtoask.add_field(
			name  = "Be Patient and Polite",
			value = "While it may be an obvious thing to say, it is true. The person who is helping you is a volunteer. They are not getting paid to do this and are helping you out of their own free will. Do not disrespect anyone who is helping you out. You can and will be kicked for this behavior. Also, try to not use terms like \"k\" or anything that's off-putting/condescending."
		)
		howtoask.add_field(
			name  = "Don't ask to ask",
			value = "https://dontasktoask.com"
		)

		await ctx.respond(embed=howtoask, ephemeral=True)



	#######################################################
	# TEAM
	#######################################################
	@commands.slash_command(
		name="staff",
		 description="View all our team members on the server"
	)
	async def team(self, ctx, team=None):

		if team is None:
			await ctx.respond("Please supply what team you are looking for. `staff` or `support`")
		
		elif team.lower() == "staff":
			staff_list = ""
			for member in ctx.guild.members:
				for role in member.roles:
					if role.id == PraetorUtility().staff_role_id:
						staff_list = staff_list + f"<@{member.id}> ({member})\n"
			staff_embed = discord.Embed(
				title="Staff Team",
				description=staff_list,
				color=0x801755
			)
			await ctx.send(embed=staff_embed)

		elif team.lower() == "support":
			support_list = ""
			for member in ctx.guild.members:
				for role in member.roles:
					if role.id == PraetorUtility().support_role_id:
						support_list = support_list + f"<@{member.id}> ({member})\n"
			support_embed = discord.Embed(
				title="Support Team",
				description=support_list,
				color=0x81eb98
			)
			support_embed.set_footer(
				text="Click on the user to see what they are specifically support for (will be in their roles)"
			)
			await ctx.send(embed=support_embed)
				


async def setup(client):
	await client.add_cog(Commands(client))