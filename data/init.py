import os
dirs = ['data/metadata']
for d in dirs:
	if not os.path.isdir(d):
		os.mkdir(d)