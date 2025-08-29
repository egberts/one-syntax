import os

def list_files(directory):
    for root, dirs, files in os.walk(directory):
        print(f"Directory: {root}")
        for file in files:
            print(f"  File: {file}")

list_files("..")