import argparse
import sys
from pathlib import Path

def parse_args():
    #setup argparse
    parser = argparse.ArgumentParser(prog="writeup-converter.py", description="Takes a folder of Obsidian markdown files and copies them across to a new location, automatically copying any attachments. Options available include converting to a new set of Markdown files, removing and adding prefixes to attachments, and converting for use on a website")

    #positional arguments
    parser.add_argument("source_folder", help="The folder of markdown files to copy from.")
    parser.add_argument("source_attachments", help="The attachments folder in your Obsidian Vault that holds attachments in the notes.")
    parser.add_argument("target_folder", help="The place to drop your converted markdown files")
    parser.add_argument("target_attachments", help="The place to drop your converted attachments. Must be set as your attachments folder in Obsidian (or just drop them in the root of your vault if you hate yourself)")

    #optional flags
    parser.add_argument("-a", "--add-prefix", help="Prefix to add to all your attachment file paths.")
    parser.add_argument("-r", "--remove-prefix", help="Prefix to remove from all your attachment file paths.")

    #parse arguments
    args = parser.parse_args()

    #output arguments for debugging
    for arg in vars(args):
        argval = getattr(args, arg)
        if argval is not None:
            print(str(arg) + ": " + str(argval))

    return args

def find_files(source_folder, source_attachments):
    """finds files within the target directory"""

    #create an OS-independent Path object for source folder and attachments folder
    sf_path = Path(source_folder)
    sa_path = Path(source_attachments)

    #check directories exist
    if not sf_path.is_dir():
        print("Source folder path (" + str(sf_path) + ") is not a directory. Exiting")
        sys.exit(1)

    if not sa_path.is_dir():
        print("Source attachments folder path (" + str(sa_path) + ") is not a directory. Exiting")
        sys.exit(1)

def main():
    args = parse_args()

    find_files(args.source_folder, args.source_attachments)

if __name__ == '__main__':
    main()