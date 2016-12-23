# Run CLI commands
from subprocess import call

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

# Make the LaTeX project
print ">> Templates filled successfully."
print ">> Now building the LaTeX project..."
call(["make", "../latex/"])
