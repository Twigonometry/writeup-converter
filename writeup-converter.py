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
    parser.add_argument("-a", "--add_prefix", help="Prefix to add to all your attachment file paths.")
    parser.add_argument("-r", "--remove_prefix", help="Prefix to remove from all your attachment file paths.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode. Gives details of which files are being copied. Disabled by default in case of large directories")

    #parse arguments
    args = parser.parse_args()

    return args

def find_files(source_folder, verbose):
    """finds files within the target directory
    even if the whole directory is being copied, this step is necessary
    as files need to be passed to the find_attachments() method"""

    print("\n=== Finding Files ===\n")

    #create an OS-independent Path object for source folder
    sf_path = Path(source_folder)
    print("Source Folder path: " + str(sf_path))

    #check directories exist
    if not sf_path.is_dir():
        print("Source folder path (" + str(sf_path) + ") is not a directory. Exiting")
        sys.exit(1)

    #compose list of filenames (on their own) and filepaths
    filenames = [file for file in os.listdir(sf_path) if not Path(os.path.join(source_folder, file)).is_dir()]
    files = list(map(lambda f: os.path.join(source_folder, f), filenames))

    print(str(len(files)) + " files found")

    if verbose:
        for file in files:
            print(file)

    #TODO: in future add option to recursively search, for example with os.walk()
    #TODO: also add option for whitelisting/blacklisting file extensions

    return filenames, files

def copy_files(files, target, verbose):
    """copy given files from the source directory"""
    print("\n=== Copying files ===\n")

    if verbose:
        for file in files:
            print("Copy " + str(file) + " to " + str(target))
            copy(file, target)

    print("Files successfully copied to " + str(target) + " directory")

def copy_directory():
    """if user specifies whole directory should be specified"""
    print("Copy directory")

def find_attachments(files, source_attachments, verbose):
    """find all paths of attachments in a list of files"""
    print("\n=== Finding attachments referenced in files ===\n")

    #create an OS-independent Path object for source attachments folder
    sa_path = Path(source_attachments)
    print("Source Attachments path: " + str(sa_path))

    if not sa_path.is_dir():
        print("Source attachments folder path (" + str(sa_path) + ") is not a directory. Exiting")
        sys.exit(1)

    attachments = []
    
    for file in files:
        #extract attachment names
        attachments.append(list(map(lambda x: Path(os.path.join(source_attachments, x[0])), filter(None, map(lambda y: re.findall(r'\!\[\[(.*)\]\]', y), open(file))))))

    #combine lists
    attachments = itertools.chain.from_iterable(attachments)

    print(str(len(list(attachments))) + " attachments found")

    if verbose:
        for a in attachments:
            print(a)

    return attachments

def copy_attachments(attachments, target, verbose):
    """copy all attachments to a new location"""
    print("\n=== Copying attachments ===\n")

    for attachment in attachments:
        if verbose:
            print("Copy " + str(attachment) + " to " + str(target))
        copy(attachment, target)
    
    print("Attachments successfully copied")

def remove_prefixes(prefix, files, verbose):
    """remove prefixes from all links in new folder"""
    print("\n=== Removing " + prefix + " from beginning of all links ===\n")

    prefix = "[[" + prefix + "/"
    
    for file in files:
        with open(file) as f:
            s = f.read()
            if prefix not in s:
                if verbose:
                    print('"{prefix}" not found in {file}.'.format(**locals()))
                f.close()
                continue

        # Safely write the changed content, if found in the file
        with open(file, 'w') as f:
            print('Removing "{prefix}"  in {file}'.format(**locals()))
            s = s.replace(prefix, "[[")
            f.write(s)
            f.close()
        
    print("All existing prefixes removed successfully")

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

    #get plain filenames, file paths and copy
    filenames, files = find_files(args.source_folder, args.verbose)

    copy_files(files, target_path, args.verbose)

    # print("Target path: " + str(target_path))

    new_filepaths = [os.path.join(str(target_path), file) for file in filenames]

    #get all attachments from each file and copy across
    attachments = find_attachments(files, args.source_attachments, args.verbose)

    copy_attachments(attachments, target_attachments, args.verbose)

    #remove prefixes
    if args.remove_prefix is not None:
        remove_prefixes(args.remove_prefix, new_filepaths, args.verbose)

if __name__ == '__main__':
    main()