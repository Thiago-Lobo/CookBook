#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir, makedirs
from os.path import isfile, join, exists
import collections
import copy
from shutil import copyfile
from shutil import rmtree

# Run CLI commands
from subprocess import call

# Global stuff --------------------------------------------------------
recipe_directory = "../recipes/"
latex_directory = "../tex/"
pictures_directory = "../tex/pictures/"

bottom_recipe_template = "template_bottom.tex"
top_recipe_template = "template_top.tex"
cookbook_template = "template_cookbook.tex"

nome_section = "nome"
dc_section = "dc"
index_section = "index"
serve_section = "serve"
kcal_section = "kcal"
ingredientes_section = "ingredientes"
modo_section = "modo"
dicas_section = "dicas"
historia_section = "historia"
spot_section = "spot"
pic_section = "pic"

recipe_files = [join(recipe_directory, f) for f in listdir(recipe_directory) if isfile(join(recipe_directory, f)) and "txt" in f]
recipe_pics = [f for f in listdir(recipe_directory) if isfile(join(recipe_directory, f)) and not "txt" in f]
recipes = {}

if not exists(latex_directory):
    makedirs(latex_directory)

if not exists(pictures_directory):
	makedirs(pictures_directory)

print ">> Copying makefile."
copyfile("./makefile", '{0}{1}'.format(latex_directory, "makefile"))

print ">> Copying cover picture."
copyfile("./cover.jpg", '{0}{1}'.format(pictures_directory, "cover.jpg"))

# Recipes handling ----------------------------------------------------
print ">> Found {0} recipe files. Will proceed to interpret them.".format(len(recipe_files))

for count, recipe_file in enumerate(recipe_files):
	with open(recipe_file) as f:
		content = [x.rstrip('\n') for x in f.readlines() if len(x.rstrip('\n')) > 0]
		
		recipe = {}
		recipe["path"] = recipe_file
		recipe[pic_section] = recipe_pics[count]

		error = 0

		for index, line in enumerate(content):
			if line.startswith("\\"):
				section = line[1:line.index(":")]
				if section == index_section: # mandatory field
					if index + 1 >= len(content) or content[index + 1].startswith("\\") or len(content[index + 1]) == 0:
						print "Invalid recipe. Error detected in line {0}.".format(index + 2)
						error = 1
						break
					recipe[index_section] = int(content[index + 1])
				if section == serve_section:
					recipe[serve_section] = int(content[index + 1])
				if section == kcal_section:
					recipe[kcal_section] = int(content[index + 1])
				if section == nome_section: # mandatory field
					if index + 1 >= len(content) or content[index + 1].startswith("\\") or len(content[index + 1]) == 0:
						print "Invalid recipe. Error detected in line {0}.".format(index + 2)
						error = 1
						break
					recipe[nome_section] = content[index + 1]
				if section == dc_section:
					recipe[dc_section] = content[index + 1]	
				if section == ingredientes_section: # mandatory field
					if index + 1 >= len(content) or content[index + 1].startswith("\\") or len(content[index + 1]) == 0:
						print "Invalid recipe. Error detected in line {0}.".format(index + 2)
						error = 1
						break
					i = index + 1
					while i < len(content) and not content[i].startswith("\\"):
						i = i + 1
					recipe[ingredientes_section] = content[index + 1:i]
				if section == modo_section: # mandatory field
					if index + 1 >= len(content) or content[index + 1].startswith("\\") or len(content[index + 1]) == 0:
						print "Invalid recipe. Error detected in line {0}.".format(index + 2)
						error = 1
						break
					i = index + 1
					while i < len(content) and not content[i].startswith("\\"):
						i = i + 1
					recipe[modo_section] = content[index + 1:i]
				if section == dicas_section:
					i = index + 1
					while i < len(content) and not content[i].startswith("\\"):
						i = i + 1
					recipe[dicas_section] = content[index + 1:i]
				if section == historia_section:
					recipe[historia_section] = content[index + 1]

		if error == 1:
			continue

		recipes[recipe[index_section]] = recipe
		
# LaTeX Template handling ---------------------------------------------
# Read Template File
template_bottom_lines = []
template_top_lines = []
template_cookbook = []

with open(bottom_recipe_template) as f:
    template_bottom_lines = [x.rstrip('\n') for x in f.readlines() if len(x.rstrip('\n')) > 1]

with open(top_recipe_template) as f:
    template_top_lines = [x.rstrip('\n') for x in f.readlines() if len(x.rstrip('\n')) > 1]

with open(cookbook_template) as f:
    template_cookbook = f.readlines()

# LaTeX Template filling ----------------------------------------------

sorted_recipes = collections.OrderedDict(sorted(recipes.items()))

for index in sorted_recipes:
	ignore_lines = []
	lines_to_write = []
	target_list = []

	if index % 2 == 0:
		lines_to_write = copy.deepcopy(template_top_lines)
		target_list = template_top_lines
	else:
		lines_to_write = copy.deepcopy(template_bottom_lines)
		target_list = template_bottom_lines
	
	for counter, line in enumerate(target_list):
		if "<<{0}>>".format(nome_section) in line:
			line = line.replace("<<{0}>>".format(nome_section), sorted_recipes[index][nome_section])
		if "<<{0}>>".format(serve_section) in line:
			if serve_section in sorted_recipes[index]:
				line = line.replace("<<{0}>>".format(serve_section), "{0}".format(sorted_recipes[index][serve_section]))		
			else:
				line = line.replace("<<{0}>>".format(serve_section), "-")			
		if "<<{0}>>".format(kcal_section) in line:
			if kcal_section in sorted_recipes[index]:
				line = line.replace("<<{0}>>".format(kcal_section), "{0}".format(sorted_recipes[index][kcal_section]))
			else:
				line = line.replace("<<{0}>>".format(kcal_section), "-")			
		if "<<{0}>>".format(ingredientes_section) in line:
			ingredientes = sorted_recipes[index][ingredientes_section]
			new_line = ""
			for id, ingrediente in enumerate(ingredientes):
				if id % 2 == 0:					
					new_line = new_line + "$\\bullet$ {0} & ".format(ingrediente)
					if (id + 1 >= len(ingredientes)):
						new_line = new_line[0:len(new_line) - 3]
				else:
					new_line = new_line + "$\\bullet$ {0}\\\\".format(ingrediente)
					if (id + 1 >= len(ingredientes)):
						new_line = new_line[0:len(new_line) - 2]
			line = line.replace("<<{0}>>".format(ingredientes_section), new_line + "\n")			
		if "<<{0}>>".format(modo_section) in line:
			modo = sorted_recipes[index][modo_section]
			new_line = ""
			for id, etapa in enumerate(modo):
				new_line = new_line + "{0}. ".format(id + 1) + etapa
				if not id + 1 >= len(modo):
					new_line = new_line + "\\\\"
				new_line = new_line + "\n"
			line = line.replace("<<{0}>>".format(modo_section), new_line)		
		if "<<{0}>>".format(dicas_section) in line:
			if dicas_section in sorted_recipes[index]:				
				dicas = sorted_recipes[index][dicas_section]
				new_line = ""
				for id, dica in enumerate(dicas):
					new_line = new_line + "$\\bullet$ " + dica
					if not id + 1 >= len(dicas):
						new_line = new_line + "\\\\"
					new_line = new_line + "\n"
				line = line.replace("<<{0}>>".format(dicas_section), new_line)
			else:
				ignore_lines = [ignore_lines, counter, counter - 1, counter - 2, counter - 3]			
		if "<<{0}>>".format(historia_section) in line:
			if historia_section in sorted_recipes[index]:
				line = line.replace("<<{0}>>".format(historia_section), "\\textit{{{0}}}".format(sorted_recipes[index][historia_section]))
			else:
				ignore_lines = [ignore_lines, counter, counter - 1, counter - 2, counter - 3]
		if "<<{0}>>".format(pic_section) in line:
			line = line.replace("<<{0}>>".format(pic_section), sorted_recipes[index][pic_section])
		lines_to_write[counter] = line	

	print ">> Writing {0}{1}.tex".format(latex_directory, index)
	f = open('{0}{1}.tex'.format(latex_directory, index), 'w')
	for id, line in enumerate(lines_to_write):
		if id not in ignore_lines:
			f.write(line)			
			f.write("\n")
	f.close()

	print ">> Copying {0}{1} to {2}{3}".format(recipe_directory, sorted_recipes[index]["pic"], pictures_directory, sorted_recipes[index]["pic"])
	copyfile('{0}{1}'.format(recipe_directory, sorted_recipes[index]["pic"]), '{0}{1}'.format(pictures_directory, sorted_recipes[index]["pic"]))

for count, line in enumerate(template_cookbook):
	if "<<{0}>>".format(spot_section) in line:
		new_line = ""
		for index in sorted_recipes:
			new_line = new_line + "\\input{{{0}}}".format(index) + "\n"
		template_cookbook[count] = line.replace("<<{0}>>".format(spot_section), new_line)	

f = open('{0}cookbook.tex'.format(latex_directory), 'w')
for line in template_cookbook:
	f.write(line)
f.close()

# LaTeX Project handling ----------------------------------------------

# Make the LaTeX project
print ">> Templates filled successfully."
print ">> Now building the LaTeX project..."
call(["make", "-C", latex_directory])

copyfile('{0}cookbook.pdf'.format(latex_directory), "./cookbook.pdf")
rmtree(latex_directory)
