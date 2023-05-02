#!/usr/bin/python3
import shutil

template = "foo.ai"

f = open("names.txt")
for line in f.readlines():
    print(f"Copying {template} to {line.strip()}")
    # line holds each single line in "names.txt" we call strip() to remove
    # newlines and crap
    shutil.copyfile(template, line.strip())
