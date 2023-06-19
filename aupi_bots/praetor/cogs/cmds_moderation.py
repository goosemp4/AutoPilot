import discord, json, discord.utils
from discord.ext import commands
from datetime import date
from praetor_utility import PraetorUtility


class Moderation(commands.Cog):
	def __init__(self, client):
		self.client = client



	#######################################################
	# VERIFY
	#######################################################
	@commands.slash_command(
		name="verify",
		description="Verify member and grant them access to the server"
	)
	@commands.has_role(PraetorUtility().staff_role_id)
	async def verify(self, ctx, member:discord.Member):
		for i in ctx.author.roles:
			if i.id == PraetorUtility().staff_role_id: # Staff role ID

				# Add divider roles and such
				await member.add_roles(member.guild.get_role(862811433662545940))
				await member.add_roles(member.guild.get_role(862813454812971088))
				await member.add_roles(member.guild.get_role(862829754779303956))
				await member.add_roles(member.guild.get_role(862813524870299668))
				await member.remove_roles(member.guild.get_role(871477918369468416))

				# Reply to staff letting them know the verification worked
				await ctx.reply(f"Successfully verified <@{member.id}>", ephemeral=True)
			else:
				pass



	#######################################################
	# KICK
	#######################################################
	@commands.slash_command(
		name="kick",
		description="Kicks a member from the server"
	)
	@commands.has_role(PraetorUtility().staff_role_id)
	async def kick(self, ctx, member : discord.Member, *, reason=None):
		kickMessage = discord.Embed(
			title="Kicked",
			description=f"<@{member.id}> has been kicked from the server",
			color=0x0000FF
		)
		kickMessage.add_field(
			name="Reason",
			value=reason,
			inline=True
		)
		kickMessage.set_footer(
			text=f"kicked by {ctx.author.display_name}",
			icon_url=ctx.author.avatar_url
		)

		try:
			await member.send(f"You have been kicked from Aisle #7 for: **{reason}**")
		except discord.Forbidden:
			pass

		await member.kick(reason=reason)
		await ctx.reply(embed=kickMessage)



	#######################################################
	# BAN
	#######################################################	
	@commands.slash_command(
		name="ban",
		description="Bans a member from the server"
	)
	@commands.has_role(PraetorUtility().staff_role_id)
	async def ban(self, ctx, member : discord.Member, *, reason=None):
		banMessage = discord.Embed(
			title="Banned",
			description=f"<@{member.id}> has been banned from the server",
			color=0x0000FF
		)
		banMessage.add_field(
			name="Reason",
			value=reason,
			inline=False
		)
		banMessage.set_footer(
			text=f"banned by {ctx.author.display_name}",
			icon_url=ctx.author.avatar_url
		)

		try:
			await member.send(f"You have been banned from Aisle #7 for: **{reason}**")
		except discord.Forbidden:
			pass

		await member.ban(reason=reason)
		await ctx.reply(embed=banMessage)

	

	#######################################################
	# PURGE
	#######################################################
	@commands.slash_command(
		name="purge",
		description="Deletes a set amount of messages in channel"
	)
	#@commands.has_permissions(manage_messages=True)
	@commands.has_role(PraetorUtility().staff_role_id)
	async def purge(self, ctx, amount):
		purgeMessage = discord.Embed(
			title=f"{amount} messages have been deleted",
			color=0xFF0000
		)
		purgeMessage.set_footer(
			text=f"purged by {ctx.author.display_name}",
			icon_url=ctx.author.avatar_url
		)
		amount = int(amount)
		await ctx.channel.purge(limit=amount+1)
		await ctx.reply(embed=purgeMessage, delete_after=10)



	#######################################################
	# INFO
	#######################################################	
	@commands.slash_command(
		name="info",
		description="Gets info on specified member"
	)
	#@commands.has_permissions(administrator=True)
	@commands.has_role(PraetorUtility().staff_role_id)
	async def info(self, ctx, member : discord.Member):
		roleList = []
		memberRoles = []
		for role in ctx.guild.roles:
			if role.name == "@everyone":
				pass

			else:
				roleList.append(role.id)

		for roles in member.roles:
			if roles.id in roleList:
				memberRoles.append(roles.id)
			else:
				pass
		memberRoles.reverse()
		
		rolesStr = ""
		for i in memberRoles:
			rolesStr += f"<@&{i}>\n"

		roleEmbed = discord.Embed(
			title=f"{member}",
			description=f"<@{member.id}>"
		)

		roleEmbed.add_field(
			name="Roles",
			value=rolesStr,
			inline=False
		)

		roleEmbed.add_field(
			name="Server Nickname",
			value=member.display_name
		)

		roleEmbed.add_field(
			name="Created On",
			value=member.created_at,			
		)

		roleEmbed.add_field(
			name="Joined Server On",
			value=member.joined_at
		)

		roleEmbed.add_field(
			name="User ID",
			value=member.id
		)

		if member.bot:
			botStr = "Yes"
		elif not member.bot:
			botStr = "No"
		roleEmbed.add_field(
			name="Bot",
			value=botStr
		)

		if member.guild_permissions.administrator is True:
			adminStr = "Yes"
		else:
			adminStr = "No"
		roleEmbed.add_field(
			name="Admin",
			value=adminStr
		)

		roleEmbed.set_thumbnail(
			url=member.avatar_url
		)

		await ctx.reply(embed=roleEmbed)
			


	#######################################################
	# REACTION ROLE EMOJI ADD
	#######################################################
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.member.bot is True:
			pass
		
		else:
			with open('cogs/reactrole.json') as rrFile:
				dataStuff = json.load(rrFile)
				for x in dataStuff:
					if x['emoji'] == str(payload.emoji) and x['messageID'] == str(payload.message_id):
	
						role = discord.utils.get(self.client.get_guild(payload.guild_id).roles, id = x['roleID'])

						await payload.member.add_roles(role)


		
	#######################################################
	# REACTION ROLE EMOJI REMOVE
	#######################################################
	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		with open('cogs/reactrole.json') as rrFile:
			dataStuff = json.load(rrFile)
			for x in dataStuff:
				if x['emoji'] == str(payload.emoji) and x['messageID'] == str(payload.message_id):

					role = discord.utils.get(self.client.get_guild(payload.guild_id).roles, id = x['roleID'])

					await self.client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)



	#######################################################
	# REACTION ROLE
	#######################################################
	@commands.slash_command(
		name="reactrole",
		description="Specifies a message to have a reaction role attached to it"
	)
	#@commands.has_permissions(administrator=True)
	@commands.has_role(PraetorUtility().staff_role_id)
	async def rr(self, ctx, channel, msg_id, emoji, role: discord.Role):
		channelid = ""

		for i in channel:
			try:
				i = int(i)
				i = str(i)
				channelid += i

			except ValueError or TypeError:
				pass


		await self.client.wait_until_ready()
		channel = self.client.get_channel(int(channelid))
		try:
			message = await channel.fetch_message(int(msg_id))
		except discord.Forbidden:
			await ctx.reply("I can't react to that post! Check my permissions.")
		await message.add_reaction(emoji)

		with open("cogs/reactrole.json") as jfile:
			data = json.load(jfile)

			new_reactrole = {
				'roleName':role.name,
				'roleID':role.id,
				'emoji':emoji,
				'messageID':msg_id
			}

			data.append(new_reactrole)
		
		with open("cogs/reactrole.json", "w") as f:
			json.dump(data, f, indent=4)
		
		await ctx.respond("<a:check:871473852465709146> Reaction role successfully added!")



async def setup(client):
	await client.add_cog(Moderation(client))