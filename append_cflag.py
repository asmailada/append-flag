#########################################################################################
# Read in json. 																		#
# Read in toolchain.ninja. 																#
#	Create new rules for every opt files. 												#
#																						#
# Traverse all ninja files. 															#
#	Find the tartget opt files. 														#
#	Substitude the compiling rules. 													#
#																						#
# Change the flag only won't affect the ninja build checking							#
#																						#
#########################################################################################
from __future__ import print_function

import sys
import os
import string
import json


#################
#				#
#	funcitons	#
#				#
#################

"""Print error message"""
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


"""Print input json files"""
def json_print(json_data):
	for j_path in json_data:
		print(j_path)
		for j_head in json_data[j_path]:
			print("	"+j_head)
			if( not(type(json_data[j_path][j_head]) is str) ):
				for j_file in json_data[j_path][j_head]:
					print("		"+j_file)
					print("			"+json_data[j_path][j_head][j_file])
			else:
				print("			"+json_data[j_path][j_head])


"""dict[ filename ] = cflags"""
def json_to_dict(json_data,dict):
	for j_path in json_data:
		for j_head in json_data[j_path]:
			if( not(type(json_data[j_path][j_head]) is str) ):
				"""TODO: instance"""
				for j_file in json_data[j_path][j_head]:
					this_path = j_path + "/" + j_file
					cflag = json_data[j_path][j_head][j_file]
					dict[this_path] = cflag
			else:
				print("			"+json_data[j_path][j_head])
				cflag = json_data[j_path][j_head]
				dict["default"] = cflag
	for x in dict:
		print(x,'\n\t',dict[x]) #TODO: '{a} {b}'.format(a=x, b=y)


"""Constrcut rule[toolchain][rule_name]=[rules], target_file[file]=rule_name"""
def checkFile(filename,opt_flag,rule,target_file):
	print("Checking file ... ",filename)
	with open(filename,"r") as f:
		lines = f.read().splitlines()
		i = 0
		cur_rule = {}
		while i < len(lines):
			if lines[i].startswith("#") :
				i+=1
				continue

			if lines[i].startswith("rule "):
				"""Rules should be cache by rule_name, rule_name is specific."""
				rule_list = []
				rule_name = lines[i][5:]

				while not(lines[i+1].startswith("rule ") or lines[i+1].startswith("build ") or lines[i+1].startswith("pool ") or lines[i+1].startswith("subninja ")):
					rule_list.append(lines[i+1])
					i+=1
				
				cur_rule[rule_name] = rule_list

			elif lines[i].startswith("build "):
				for target in opt_flag:
					"""Path should be relative to the -C dir"""
					if target in lines[i]:
						target_rule = lines[i].split()[2]
						target_file[target] = target_rule
			i+=1
		rule[filename] = cur_rule
def createRuleName(filename,rule_name):
	new_filename = filename.replace("/","_")
	new_filename = new_filename.replace(".","_")
	return rule_name + "_" + new_filename

"""Add rules for each file to each toolchain"""
def addRule(opt_flag,rule,target_file):
	for toolchain in rule:
		"""Open the target toolchain and add specific rule"""
		filename = toolchain
		filename_temp = filename.split(".ninja")[0]+"_temp.ninja"
		print("Adding rule ...",filename," ",filename_temp)
		with open(filename,"r") as f:
			fw = open(filename_temp,"w")
			lines = f.read().splitlines()
			isRule = False
			i = 0
			while i < len(lines):
				if lines[i].startswith("#") :
					print(lines[i],file=fw)
					i+=1
					continue

				if lines[i].startswith("rule "):
					"""Add rule"""
					if isRule == False:
						for file in target_file:
							if target_file[file] in rule[toolchain]:
								cur_rule = target_file[file]
								new_rule = createRuleName(file,cur_rule)
								print("change rule... ")
								cur_command = rule[toolchain][cur_rule]
								new_command = cur_command[0].split("-c")[0] + " " +opt_flag[file] + " -c " + cur_command[0].split("-c")[1]
								print("rule "+new_rule,file=fw)
								print(new_command,file=fw)
								print("\trule "+new_rule)
								print("\t",new_command)

								j = 1
								while j < len(cur_command):
									print(cur_command[j],file=fw)
									j+=1
						isRule = True
					print(lines[i],file=fw)

					while not(lines[i+1].startswith("rule ") or lines[i+1].startswith("build ") or lines[i+1].startswith("pool ") or lines[i+1].startswith("subninja ")):
						print(lines[i+1],file=fw)
						i+=1

				elif lines[i].startswith("build "):
					"""Change build statement"""
					isBuild = False
					for file in target_file:
						if file in lines[i]:
							"""assume the rule already exists"""
							cur_rule = target_file[file]
							new_rule = createRuleName(file,cur_rule)
							idx = lines[i].find(cur_rule)
							if idx > -1:
								print("change build... "+file)
								new_build = lines[i][0:idx] + new_rule + lines[i][(idx+len(cur_rule)):]
								print(new_build,file=fw)
								print("\t",new_build)
								isBuild = True
					if not(isBuild):
						print(lines[i],file=fw)
				else:
					print(lines[i],file=fw)
				i+=1
			fw.close()
		print("\n")
		"""rm `original.ninja` && mv `_temp.ninja` to `original.ninja`"""
		"""
		idx1 = filename.find("/")
		idx2 = 0
		while idx1 > -1:
			print(idx1," ",idx2)
			idx2 = idx1
			idx1 = filename.find("/",idx2+1)
		"""
		"""print("The dir is: ",os.listdir(filename[0:idx2]),"\n")"""
		#os.remove(filename)
		#print("Remove ",filename)
		#os.rename(filename_temp,filename)
		#print("Rename ",filename_temp," ",filename)
		"""print("The dir after removal of path : %s" %os.listdir(filename[0:idx2]),"\n")"""



#################
#				#
#	  main		#
#				#
#################
"""TODO:Change working directory not funtionable"""

workingDir = "./"
if len(sys.argv) < 2:
	eprint("No input argument.")
	eprint('Usage:')
	eprint('-C\tdesired working directory')
	eprint('-in\tinput json file, which path is relative to -C')
	sys.exit()
else:
	i = 1
	while i < len(sys.argv):
		option = sys.argv[i]
		print(option)
		if option == '-in':
			if sys.argv[i+1].endswith(".json"):
				json_file_name = sys.argv[i+1]
			else:
				eprint('Please enter a valid json file.')
		elif option == '-C':
			"""changing working directory"""
			workingDir = sys.argv[i+1]
			os.chdir(workingDir)
			eprint("Changnig working directory to:\t",os.getcwd())
		else:
			eprint('Usage:')
			eprint('-C\tdesired working directory')
			eprint('-in\tinput json file, which path is relative to -C')
			sys.exit()
		i+=2

print("\n")	

"""Read in json."""
opt_flag = {}
rule = {}
toolchain = {}
target_file = {}
with open(json_file_name) as json_file:
    json_data = json.load(json_file)
    #print(json.dumps(json_data, sort_keys=True, indent=4))
    #json_print(json_data)
    json_to_dict(json_data,opt_flag)

    """
	Now, json file had stored in json_data. 
	Check json_print to see how to access json_data.
	"""
print("\n")
"""
Traseverse all ninja files to find rules contain target opt files.
cache rules to `rule`. 
cache target files in `target_file`.
"""

for root, dirs, files in os.walk(os.getcwd(), topdown=False):
	for name in files:
		if name.endswith('.ninja'):
			checkFile(os.path.join(root, name),opt_flag,rule,target_file)
	for name in dirs:
		os.path.join(root, name)
addRule(opt_flag,rule,target_file)

"""
for x in rule:
	print(x,"\n\t",rule[x])
"""
for x in target_file:
	print(x,"\n\t",target_file[x])


"""Create rules in toolchain.ninja."""
"""Change the rules."""


