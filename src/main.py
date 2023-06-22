from json import load, dump
from subprocess import Popen

from os import system
from os.path import exists
from datetime import datetime

_program_name = "AutoPilot"
_author       = "goose.mp4"
_desc         = "Multi-token discord bot control panel and manager"


"""
TODO:

-  : incomplete or to be added
i- : currently being worked on by 'i' (initial)

- Add logging

- Have user enter commands

g- If bot is defaulted to online include it in the loading print screen and actually do the start function for those bots.

- When user enters in the command to start/stop a bot, run that command that does that for that process

- If user asks for info about a bot, clear the terminal and load the information via JSON and display it on screen, type 'back' to go back to the main menu

- ONLY ADD DYNAMIC BOT ADDING IN QT DESIGNER VERSION, THIS IS JUST FOR PRODUCTION PURPOSES

g/ Decided making the configuration for the actual control panel itself to be a txt file. Essentially the user opens the file and there will be things like '*USER_DISPLAY_NAME=your-name-here' so that we don't have to implement a specialized way to handle console commands that configure to control panel itself (plus I feel as if it's more user friendly as it seperates everything into seperate pieces/modules :-] )
"""

# i am here -martin
# epic 😎 -goose



def get_json(json_file_name:str):
	"""Returns a specified JSON file"""
	return load(open(f"src/storage/json/{json_file_name}.json"))



def set_json(json_file_name, new_json):
	"""Sets a specified JSON file to be different dictionary"""
	with open(f"AutoPilotsrc/storage/json/{json_file_name}.json", "w") as json_file:
		try:
			dump(new_json, json_file, indent=4)
			return
		except Exception as e:
			print(f"[!] {e}")



def set_bot_online():
	pass



def aupi_process_command(console_command:str):
	"""Processes commands from the AutoPilot console control panel"""
	system('cls') # clear the console!!!

	# Process command
	console_command = console_command.lower().split()
	all_bot_configs = get_json("bot_config")

	# Have preset list of valid keys
	all_command_keys = [
		"set",    # Sets the value of an attribute for a bot
		"copy",   # Copies the value of an attribute for a bot
		"toggle", # Toggles a bot on or off
	]

	# Attempt to get each required segment
	try:
		cmd_key 	  = console_command[0] # Which command the user is trying to use
		bot_key 	  = console_command[1] # The index of where the bot is on the list
		bot_attribute = console_command[2] # The attribute in which the user is changing
		bot_value 	  = console_command[3] # The new value the selected attribute is being changed to

	except IndexError as e:
		# re-word all of this better, im really high when writing this
		# All 4 parts should be present so in the case any are missing via IndexError you know the user is a moron
		return ValueError(f"Insufficient amount of commands passed through! Error: {e}") 


	# Determine what bot to get off the list
	for bot_index in range(len(all_bot_configs)):
		if bot_index == cmd_key:
			requested_bot = all_bot_configs[bot_index]


	if cmd_key == "online":
		pass
					
	set_json("bot_config", all_bot_configs)
	return



def aupi_main():
	"""Start the AutoPilot console control panel"""

	bot_list = get_json("bot_config")

	while True:
		console_display = f"# {_program_name} | by {_author} #\n\n"

		# Load each bot's indvidual information for the console display
		display_number = 0
		for bot in bot_list:
			
			# Get bot information
			display_name = bot["display_name"]
			online       = bot["online"]
			key          = bot["key"]
			debug        = bot["debug"]
			show_token 	 = bot["show_token"]
			token 		 = bot["token"] if show_token else "N/A"
			online_display = "online" if online else "offline"
			
			# Add bot info to the console display
			console_display += "############################################################\n"
			console_display += f"[ {display_number} ]  {display_name} | {online_display}\n"
			console_display += f"token:  {token}\n"
			console_display += f"key:    {key}\n"
			console_display += f"debug:  {debug}\n"
			console_display += f"show_token: {show_token}\n"
			console_display += "############################################################\n\n\n"

			display_number += 1

		# Show console display in console
		console_display += "enter 'help' for all cmds"
		print(console_display)

	# Get user commands
		try:
			# Have user enter in a command
			aupi_process_command(input("command >: "))
		except Exception as e:
			print(f"[!] An error has occurred while processing your command...\n{e}")



# ---------------------------------------------------------------
# Start the AutoPilot console control panel on the file being ran
if __name__ == "__main__":
	aupi_main() # AutoPilot main func
