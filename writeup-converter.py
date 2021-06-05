import argparse
import sys
from pathlib import Path
import os
import re
import itertools
from shutil import copy

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

def find_files(source_folder):
    """finds files within the target directory
    even if the whole directory is being copied, this step is necessary
    as files need to be passed to the find_attachments() method"""

    #create an OS-independent Path object for source folder
    sf_path = Path(source_folder)
    print("Source Folder path: " + str(sf_path))

    #check directories exist
    if not sf_path.is_dir():
        print("Source folder path (" + str(sf_path) + ") is not a directory. Exiting")
        sys.exit(1)

    #compose list of filepaths
    files = [os.path.join(source_folder, file) for file in os.listdir(sf_path) if not Path(os.path.join(source_folder, file)).is_dir()]

    for file in files:
        print(file)

    #TODO: in future add option to recursively search, for example with os.walk()
    #TODO: also add option for whitelisting/blacklisting file extensions

    return files

def copy_files(files, target):
    """copy given files from the source directory"""
    for file in files:
        copy(file, target)

def copy_directory():
    """if user specifies whole directory should be specified"""
    print("Copy directory")

def find_attachments(files, source_attachments):
    """find all paths of attachments in a list of files"""

    #create an OS-independent Path object for source attachments folder
    sa_path = Path(source_attachments)

    if not sa_path.is_dir():
        print("Source attachments folder path (" + str(sa_path) + ") is not a directory. Exiting")
        sys.exit(1)

    attachments = []
    
    for file in files:
        #extract attachment names
        attachments.append(list(map(lambda x: Path(os.path.join(source_attachments, x[0])), filter(None, map(lambda y: re.findall(r'\!\[\[(.*)\]\]', y), open(file))))))

    #combine lists
    attachments = itertools.chain.from_iterable(attachments)
    # print(list(attachments))

    return attachments

def copy_attachments(attachments, target):
    """copy all attachments to a new location"""

    for attachment in attachments:
        print("Copy " + str(attachment) + " to " + str(target))
        copy(attachment, target)

def remove_prefixes():
    """remove prefixes from all attachments in new folder"""
    print("Remove prefixes")

def website_format():
    """combine all files in a directory into one markdown folder
    turn backlinks into header links
    turn attachment links into image links (if they have an image file extension)"""

    print("Reformat to go on a website")

def main():
    args = parse_args()

    #create target folders if they don't exist
    target_path = Path(args.target_folder)
    if not target_path.is_dir():
        print("Creating target folder")
        target_path.mkdir()

    target_attachments = Path(args.target_attachments)
    if not target_attachments.is_dir():
        print("Creating target attachments folder")
        target_attachments.mkdir()

    #get file paths
    files = find_files(args.source_folder)

    copy_files(files, target_path)

    #get all attachments from each file
    attachments = find_attachments(files, args.source_attachments)

    # weirdly, calling this clears the attachments variable...
    # print(list(attachments))

    copy_attachments(attachments, target_attachments)

if __name__ == '__main__':
    main()