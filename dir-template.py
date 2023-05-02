#!/usr/bin/python3
import os


f = open("names.txt")
for line in f.readlines():
    f = line.strip()
    print(f"Creating folder {f}")
    if not os.path.isdir(f):
        os.makedirs(f)
