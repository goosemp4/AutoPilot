import json

class PraetorUtility():
	def __init__(self):

		self.bot_id 			= 862836714727800883
		self.owner_id 			= 298577135952723969
		self.unverified_role_id = 871477918369468416
		self.staff_role_id 		= 862811341772423190
		self.support_role_id 	= 862813090675687455
		self.member_role_id 	= 862811433662545940
		self.guild_id 			= 862807791662923787
		self.logs_channel_id 	= 1092934440684113940


	#######################################################
	# GETTERS
	#######################################################
	def get_json(file_name):
		"""Returns a JSON file via file name"""
		return json.load(open(f"src_praetor/docs/{file_name}.json"))


	def set_json(file_name, new_file):
		"""Sets a specified JSON file to be different dictionary"""
		with open(f"src_praetor/docs/{file_name}.json", "w") as f:
			json.dump(new_file, f, indent=4)
			return print(f"JSON '{file_name}' has been updated")
