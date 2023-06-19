import discord, random, os, string, asyncio, threading
from discord.ext import commands
from praetor_utility import PraetorUtility
from discord import ui

# Pillow Framework
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image



#######################################################
# CAPTCHA VERIFICATION MODAL
#######################################################
class CaptchaModal(ui.Modal,):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

		# ---- Creating InputText Modal ----
		self.add_item(
			ui.InputText(
				label 	   = "Enter Captcha Here (CaSe SeNsiTivE)",
				style 	   = discord.InputTextStyle.short,
				required   = True,
				min_length = 7,
				max_length = 7
			)
		)

	async def callback(self, interaction:discord.Interaction):
		# Get user's captcha JSON info
		all_captchas = PraetorUtility.praetor_get_json("captcha") # Get all captches for unverified members
		for user in all_captchas: # Get all user captchas
			if user["id"] == interaction.user.id:
				user_json = user
				break
		

		# ---- If captcha is correct ----
		captcha 	  = user["captcha"] 	   # Get user's captcha
		input_captcha = self.children[0].value # User captcha entry
		
		if input_captcha == captcha:


			# ---- Remove user from captcha JSON
			user = None
			for i in range(len(all_captchas)):
				try:
					if all_captchas[i]["id"] == interaction.user.id:
						del all_captchas[i]
						PraetorUtility.get_json("captcha", all_captchas)
				except:
					break	


			# ---- Variables ----
			server 		 = interaction.client.get_guild(PraetorUtility().guild_id) 		# Server obj
			user_obj 	 = server.get_member(interaction.user.id) 				# Member object
			user_channel = server.get_channel(user_json["captcha_channel_id"])  # User's channel obj
			join_channel = server.get_channel(862815252964966421) 				# Join channel


			# ---- Delete channel ----
			try:
				await interaction.response.send_message("**Captcha Complete**") # So the interaction got a 'response'
				await user_channel.delete()
			except:
				pass


			# ---- Add/remove roles ----
			await user_obj.remove_roles(server.get_role(PraetorUtility().unverified_role_id)) # Remove unverified role
			await user_obj.add_roles(server.get_role(PraetorUtility().member_role_id)) 		 # Add member role
			await user_obj.add_roles(server.get_role(862813454812971088)) 			 # Add divider role
			await user_obj.add_roles(server.get_role(862829754779303956)) 			 # Add second divider role

	
			# ---- Join channel message ----
			join_embed = discord.Embed(
				description = f"** **\n** **\n**<@{interaction.user.id}> has joined**",
				color 		= 0x77dd77,
			)
			join_embed.set_footer(
				text = interaction.user
			)
			join_embed.set_thumbnail(
				url = interaction.user.avatar.url
			)


			# ---- Attempt to send user a welcome message
			try:

				# Welcome message
				welcome_user_embed = discord.Embed(
					description = "Analog is a server that offers programming support, server-wide projects, discussions, and a dedicated support team. We welcome programmers of all levels, with systems for beginners to prevent them from feeling overwhelmed and encourage high-level questions for experienced programmers.",
					colour 		= 0x000000
				)
				welcome_user_embed.set_author(
					name = f"Welcome to Analog, {interaction.user.name}",
					icon_url = interaction.client.user.avatar.url
				)
				welcome_user_embed.set_footer(
					text = f"If you don't have access to the server, please contact staff"
				)

				# How get help message
				welcome_help_embed = discord.Embed(
					title 		= "How do I get help?",
					description = "To get help with any programming related problems, use the channel <#1026208984702664704> in the server. There are other channels that provide support with other problems, but this is the main go-to place. Use the `/help` slash command to request for help with your problem",
					colour 		= 0x000000
				)

				# Server bot message
				welcome_bot_embed = discord.Embed(
					title 		= "Server Bot",
					description = f"We have a dedicated bot for  Analog (<@{PraetorUtility().bot_id}>), which has core functionality with all aspects from the server.\n\nIt also has many fun commands that enhance the community aspect of the server. Try using the `/cmds` slash command to see all of the available commands.",
					colour 		= 0x000000
				)
				welcome_bot_embed.set_thumbnail(
					url = interaction.client.user.avatar.url
				)

				# ---- Send user welcome messages ----
				await interaction.user.send(embed=welcome_user_embed)
				await interaction.user.send(embed=welcome_help_embed)
				await interaction.user.send(embed=welcome_bot_embed)


			# ---- Bot cannot DM user ----
			except discord.errors.Forbidden:
				pass

		
		elif input_captcha != captcha: # If the captchas DO NOT match
			
			# ---- Incorrect captcha message ----
			# Embed
			incorrect_captcha_embed = discord.Embed(
				title = ":x: Incorrect Captcha",
				description = "Your answer to the captcha was incorrect, please try again",
				colour = 0xFF0000
			)
			incorrect_captcha_embed.set_footer(
				text = "If this issue persist, please contact a Staff member"
			)
			
			await interaction.response.send_message(embed=incorrect_captcha_embed, delete_after=15)

		
		# ---- Notify server user has joined ----
		# Small join embed
		small_join_embed = discord.Embed(
			colour = 0x98FB98
		)
		small_join_embed.set_author(
			name 	 = f"{interaction.user} has joined",
			icon_url = interaction.user.avatar.url
		)

		# Send messages
		await join_channel.send(embed=join_embed)
		await server.get_channel(862849812311703563).send(f"<@&{1092556267484090418}>")
		await server.get_channel(862849812311703563).send(embed=small_join_embed)



#######################################################
# SERVER JOIN/LEAVE HANDLING
#######################################################
class Gateway(commands.Cog):

	def __init__(self, client):
		self.client = client


	@commands.Cog.listener()
	async def on_member_join(self, member):

		# Add 'Unverified' role
		await member.add_roles(member.guild.get_role(PraetorUtility().unverified_role_id))


		# ---- Create captcha ----
		# Captcha configuration
		captcha_message  = ''.join(random.choices(string.ascii_uppercase+string.ascii_lowercase+string.digits,k=7)) # The captcha
		captcha_background_rbga  = (0,0,0,0) 	 # Background colour
		captcha_font_rgb 		 = (0, 191, 255) # Font colour
		captcha_save_dir = "src/temp/" 			 # Save dir

		# Create captcha image
		captcha_image = Image.new("RGBA", (200,70), captcha_background_rbga) 			  # Create image
		captcha_draw  = ImageDraw.Draw(captcha_image) 									  # Enable drawing for image or sum (idk i dont use this lib)
		captcha_font  = ImageFont.truetype("src/docs/font.ttf", 31) 							  # Create the font for the text
		captcha_draw. text((10,10), captcha_message, captcha_font_rgb, font=captcha_font) # Add the captcha text to the image with the applied font
		captcha_image.save(f"src/temp/captcha_{captcha_message}.png") 					  # Save the image to temp

		# Create user uverified channel
		unverified_category 	= discord.utils.get(member.guild.categories, name="Unverified")
		unverified_user_channel = await member.guild.create_text_channel(f"{member.name}-captcha", category=unverified_category)

		# Get role objects
		unverified_role_obj = member.guild.get_role(PraetorUtility().unverified_role_id) # Unverified
		staff_role_obj   	= member.guild.get_role(PraetorUtility().staff_role_id) 		# Staff
		member_role_obj  	= member.guild.get_role(PraetorUtility().member_role_id) 	# Member

		everyone_perms 			= unverified_user_channel.overwrites_for(member.guild.default_role) # @everyone
		user_perms 			    = unverified_user_channel.overwrites_for(member) 					# User
		unverified_member_perms = unverified_user_channel.overwrites_for(unverified_role_obj) 		# Unverified
		staff_member_perms      = unverified_user_channel.overwrites_for(staff_role_obj) 			# Staff
		regular_member_perms    = unverified_user_channel.overwrites_for(member_role_obj) 			# Member

		# Set permissions
		user_perms.view_channel  = True
		user_perms.send_messages = True
		
		everyone_perms.view_channel = False

		staff_member_perms.view_channel = True

		regular_member_perms.view_channel  = False
		regular_member_perms.send_messages = False

		# Set channel permissions
		await unverified_user_channel.set_permissions(member, overwrite=everyone_perms) 			   # @everyone
		await unverified_user_channel.set_permissions(member, overwrite=user_perms) 				   # User
		await unverified_user_channel.set_permissions(staff_role_obj, overwrite=staff_member_perms)    # Staff
		await unverified_user_channel.set_permissions(member_role_obj, overwrite=regular_member_perms) # Member



		# ---- Add new member to captcha JSON ----
		# Create user's captcha JSON
		user_captcha_json = {
			"id": 				  int(member.id), 		# User's Discord ID
			"captcha": 			  str(captcha_message), # Captcha
			"captcha_msg_id": 	  None, 				# Captcha message ID
			"captcha_channel_id": None, 				# Captcha channel ID
		}

		# Add user to JSON
		json_file = PraetorUtility.get_json("captcha") # Get user captchas JSON file
		json_file.append(user_captcha_json) 	 # Add user to JSON file
		PraetorUtility.set_json("captcha", json_file)  # Set JSON file to updated one



		# ---- Captcha embed ----
		# Captcha message
		captcha_message_embed = discord.Embed(
			title 		= "Captcha Verification",
			description = "Welcome to Analog, please complete the following captcha to gain access to the server and to verify yourself as human",
			color 		= 0x5865F2
		)
		captcha_message_embed.set_image(
			url = "attachment://captcha.png"
		)
		captcha_message_embed.set_thumbnail(
			url = self.client.user.avatar.url
		)
		captcha_message_embed.set_footer(
			text = "Click the 'Verify' button below to start"
		)
		captcha_file  = discord.File((captcha_save_dir + f"captcha_{captcha_message}.png"), filename="captcha.png")


		# ---- Button configuration ----
		# Verify captcha button callback
		async def captacha_callback(interaction:discord.Interaction):
			"""Give user a InputText modal for their captcha entry"""
			await interaction.response.send_modal(CaptchaModal(title="Captcha Verification"))


		# Info button callback
		async def info_callback(interaction:discord.Interaction):
			"""Send user message with info on why they have to verify with captcha to join the server"""
			info_message_embed = discord.Embed(
				title = "Why do I have to verify?",
				description = "Captcha verification is required to prevent bot accounts from joining the server.\nThis requires an actual human to complete therefore preventing mass bot accounts joining.",
				colour = 0xFFFFFF
			)
			info_message_embed.add_field(
				name = "Why are bot accounts harmful?",
				value = "These bot accounts are made to spread something, that being Discord server invites, YouTube promotions, or mainly, scams. These accounts will either send messages in all the channels of a server with phishing links or directly DM you. Having a captcha verification will prevent 90% \of these accounts from joining our server and protects our members."
				)
			await interaction.response.send_message(embed=info_message_embed)


		# Buttons
		captcha_btn = ui.Button(
			label = "Verify",
			style = discord.ButtonStyle.blurple,
			emoji = "🛡" # Shield
		)
		info_btn = ui.Button(
			label = "",
			style = discord.ButtonStyle.grey,
			emoji = "❔"
		)

		# Set button callbacks
		captcha_btn.callback = captacha_callback
		info_btn.callback 	 = info_callback

		# View
		captcha_view = ui.View(timeout=300)
		captcha_view.add_item(captcha_btn)
		captcha_view.add_item(info_btn)



		# ---- Send captcha ----
		# Send captcha embed into unverified user's channel with a ping
		await unverified_user_channel.send(f"<@{member.id}>")
		captcha_message_obj = await unverified_user_channel.send(file=captcha_file, embed=captcha_message_embed, view=captcha_view, delete_after=300)

		# Update
		index = 0
		captcha_json = PraetorUtility.get_json("captcha.json")
		for user in captcha_json:
			if user["id"] == member.id:
				captcha_json[index]["captcha_msg_id"] 	  = captcha_message_obj.id     # Set channel ID
				captcha_json[index]["captcha_channel_id"] = unverified_user_channel.id # Set message ID
				PraetorUtility.set_json("captcha.json", captcha_json)
				break
			index += 1


async def setup(client):
	await client.add_cog(Gateway(client))
