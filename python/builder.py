#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join

# Run CLI commands
from subprocess import call

# Global stuff --------------------------------------------------------
recipe_directory = "../recipes/"
latex_directory = "../latex/"

nome_section = "nome"
dc_section = "dc"
index_section = "index"
serve_section = "serve"
kcal_section = "kcal"
ingredientes_section = "ingredientes"
modo_section = "modo"
comentarios_section = "comentarios"
historia_section = "historia"

recipe_files = [join(recipe_directory, f) for f in listdir(recipe_directory) if isfile(join(recipe_directory, f))]
recipes = {}

# Recipes handling ----------------------------------------------------
print ">> Found {0} recipe files. Will proceed to interpret them.".format(len(recipe_files))

for recipe_file in recipe_files:
	with open(recipe_file) as f:
		content = [x.rstrip('\n') for x in f.readlines()]
		
		recipe = {}
		recipe["path"] = recipe_file

		for index, line in enumerate(content):
			if line.startswith("\\"):
				section = line[1:line.index(":")]
				if section == index_section:
					recipe[index_section] = int(content[index + 1])
				if section == serve_section:
					recipe[serve_section] = int(content[index + 1])
				if section == kcal_section:
					recipe[kcal_section] = int(content[index + 1])
				if section == nome_section:
					recipe[nome_section] = content[index + 1]
				if section == dc_section:
					recipe[dc_section] = content[index + 1]	
				if section == ingredientes_section:
					i = index + 1
					while i < len(content) and not content[i].startswith("\\"):
						i = i + 1
					recipe[ingredientes_section] = content[index + 1:i]
				if section == modo_section:
					i = index + 1
					while i < len(content) and not content[i].startswith("\\"):
						i = i + 1
					recipe[modo_section] = content[index + 1:i]
				if section == comentarios_section:
					i = index + 1
					while i < len(content) and not content[i].startswith("\\"):
						i = i + 1
					recipe[comentarios_section] = content[index + 1:i]
				if section == historia_section:
					recipe[historia_section] = content[index + 1]

		# f = open('teste.txt','w')
		# f.write("".join(recipe[ingredientes_section]))
		# f.close()

		recipes[recipe[index_section]] = recipe

# LaTeX Template handling ---------------------------------------------
# Read Template File
with open("template_bottom.tex") as f:
    content = f.readlines()

# Filter Template File
for index, item in enumerate(content):
	if item.endswith("\n"):
		new_item = item[0:len(item) - 1]
		content[index] = new_item

# for item in content:
	# print item

# LaTeX Template filling ----------------------------------------------

# LaTeX Project handling ----------------------------------------------

# Make the LaTeX project
print ">> Templates filled successfully."
print ">> Now building the LaTeX project..."
call(["make", latex_directory])
