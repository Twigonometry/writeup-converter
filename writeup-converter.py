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
    # parser.add_argument("-a", "--add_prefix", help="Prefix to add to all your attachment file paths.")
    parser.add_argument("-r", "--remove_prefix", help="Prefix to remove from all your attachment file paths.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode. Gives details of which files are being copied. Disabled by default in case of large directories")
    parser.add_argument("-w", "--website", help="Use website formatting when files are copied. Files combined into one markdown file with HTML elements, specify the name of this file after the flag")
    parser.add_argument("-l", "--asset_rel_path", help="Relative path for site assets e.g. /assets/images/blogs/..., include this or full system path will be added to links")

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
    filenames = [file for file in os.listdir(sf_path) if not Path(os.path.join(source_folder, file)).is_dir() and file.lower().endswith('.md')]
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
    attachments = list(itertools.chain.from_iterable(attachments))

    print(str(len(attachments)) + " attachments found")

    if verbose:
        for a in attachments:
            print(str(a))

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

def combine_files(files, target_path, filename, verbose):
    "combine all found files into a single markdown file"

    combined_path = os.path.join(target_path, filename)

    with open(combined_path, 'w') as outfile:
        for f in files:
            with open(f) as infile:
                if verbose:
                    print("Integrating file: " + str(f))
                for line in infile:
                    outfile.write(line)
                outfile.write("\n\n")

    return combined_path

def create_contents(text):
    """create a contents table from parsed headers"""

    contents = "# Contents"

    headers = re.findall(r'(\#+ .*)', text)

    for header in headers:
        level = header.count('#')

        #get index of header name in string
        name_index = header.index("# ")
        header_content = header[name_index + 2:]

        #make header link
        header_link = "[" + header_content + "](#" + header_content.lower().replace(" ", "-") + ")"

        contents += "\n"
        contents += "  " * (level - 1)
        contents += "- "
        contents += header_link

    return contents

def website_format(files, target_path, attachments_rel, filename, verbose):
    """combine all files in a directory into one markdown folder
    turn backlinks into header links
    turn attachment links into image links (if they have an image file extension)
    create a contents page"""

    print("Reformatting file to go on a website")

    combined_path = combine_files(files, target_path, filename, verbose)

    # below code adapted from:
    # https://stackoverflow.com/questions/48409527/multiple-regex-string-replace-on-large-text-file-using-python
    # and https://stackoverflow.com/questions/2763750/how-to-replace-only-part-of-the-match-with-python-re-sub

    # open the source file and read it
    fh = open(combined_path, 'r')
    text = fh.read()
    fh.close()

    #create patterns

    #match attachments of form ![[a.png]]
    p_a = re.compile(r'\!\[\[(.*)\]\]')

    #match links of form [[x#y|z]]
    p_xyz = re.compile(r'\[\[(.*)\#(.*)\|(.*)\]\]')

    p_xz = re.compile(r'\[\[(.*)\|(.*)\]\]')

    p_xy = re.compile(r'\[\[(.*)\#(.*)\]\]')

    p_x = re.compile(r'\[\[(.*)\]\]')

    p_final_xy = re.compile(r'\[(.*)\]\(\#(.*)\)')

    #replace stuff

    #create lambda for lowercasing and hyphenating links
    #cannot create one lambda as each group is numbered differently
    # replacement = lambda pat: pat.group(1)

    #![[a.png]] -> ![](/path/to/attachments/a.png)
    result = re.sub(p_a, r"![]({}/\1)".format(attachments_rel), text)

    #[[x#y|z]] -> [z](#y)
    result = re.sub(p_xyz, r"[\3](#\2)", result)

    #[[x|z]] -> <a href="#x">z</a>
    result = re.sub(p_xz, r"[\2](#\1)", result)

    #[[x#y]] -> <a href="#y">y</a>
    result = re.sub(p_xy, r"[\2](#\2)", result)

    #[[x]] -> <a href="#x">x</a>
    result = re.sub(p_x, r"[\1](#\1)", result)

    #finally, turn reformatted links into lowercase and hyphenated
    replacement = lambda pat: "[" + pat.group(1) + "](#" + pat.group(2).lower().replace(" ", "-") + ")"
    result = re.sub(p_final_xy, replacement, result)

    result = create_contents(result) + "\n\n" + result

    # # write the file
    f_out = open(combined_path, 'w')
    f_out.write(result)
    f_out.close()

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

    #if user wants website formatting, do that - otherwise, just copy files
    #TODO: this isn't skipped if no -w flag
    if args.website:
        website_format(files, target_path, args.asset_rel_path, args.website, args.verbose)
    else:
        copy_files(files, target_path, args.verbose)

        new_filepaths = [os.path.join(str(target_path), file) for file in filenames]

        #remove prefixes
        if args.remove_prefix is not None:
            remove_prefixes(args.remove_prefix, new_filepaths, args.verbose)

    #get all attachments from each file and copy across
    attachments = find_attachments(files, args.source_attachments, args.verbose)

    copy_attachments(attachments, target_attachments, args.verbose)

if __name__ == '__main__':
    main()