import writeup_converter
import argparse
from pathlib import Path
from shutil import copy
import os
import sys
import re

def parse_args():
    #setup argparse
    parser = argparse.ArgumentParser(prog="file_converter.py", description="Takes an Obsidian markdown file and copies it across to a new location, automatically copying any attachments. Options available include converting to a new set of Markdown files, removing and adding prefixes to attachments, and converting for use on a website")

    #positional arguments
    parser.add_argument("source_file", help="The markdown file to copy from.")
    parser.add_argument("source_attachments", help="The attachments folder in your Obsidian Vault that holds attachments in the notes.")
    parser.add_argument("target_folder", help="The place to drop your converted markdown files")
    parser.add_argument("target_attachments", help="The place to drop your converted attachments. Must be set as your attachments folder in Obsidian (or just drop them in the root of your vault if you hate yourself)")

    #optional flags
    parser.add_argument("-r", "--remove_prefix", help="Prefix to remove from all your attachment file paths.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode. Gives details of which files are being copied. Disabled by default in case of large directories")
    parser.add_argument("-w", "--website", action="store_true", help="Use website formatting when files are copied.")
    # parser.add_argument("-l", "--asset_rel_path", help="Relative path for site assets e.g. /assets/images/blogs/..., include this or full system path will be added to links")
    parser.add_argument("-u", "--url_prefix", help="Prefix to add to URLs when converting internal links to website format")
    parser.add_argument("-n", "--no_attachments", action="store_true", help="Don't copy attachments, just the file.")

    #parse arguments
    args = parser.parse_args()

    return args

def copy_file(file_name, target_dir):
    """make directory if it doesn't exist and copy the file
    return the new filepath"""
    print("\n=== Copying file ===\n")

    target_path = Path(target_dir)
    if not target_path.is_dir():
        print("Creating target folder")
        target_path.mkdir()

    source_path = Path(file_name)

    copy(source_path, target_path)

    new_path = os.path.join(target_dir, os.path.basename(source_path))

    return new_path

def find_attachments(file_name, source_attachments):
    """find all paths of attachments in the file"""
    print("\n=== Finding attachments referenced in file ===\n")

    #create an OS-independent Path object for source attachments folder
    sa_path = Path(source_attachments)
    print("Source Attachments path: " + str(sa_path))

    if not sa_path.is_dir():
        print("Source attachments folder path (" + str(sa_path) + ") is not a directory. Exiting")
        sys.exit(1)

    #create list of attachments with source folder prepended
    attachments = map(lambda fname: source_attachments + fname, re.findall(r'\!\[\[(.*)\]\]', open(file_name, 'r').read()))

    for a in attachments:
        print(a)

    return attachments

# def edit_prefixes():
#     """edit the prefixes of internal links"""
#     print("Editing prefixes")

def pdf_format(filepath, internal_prefix):
    """reformats file so it's ready to be exported into a PDF
    change internal backlinks to markdown URL links
    if --url_prefix set, add that to links
    attachments_rel is relative path for assets on website"""

    print("Formatting for a website")

    f = open(filepath, 'r')
    text = f.read()
    f.close()

    #create patterns
    # (?!\!.*$) indicates not starting with !, to exclude attachments

    #match links of form [[x#y|z]]
    p_xyz = re.compile(r'(([^!]|^)\[\[(.*)\#(.*)\|(.*)\]\])')

    #match links of form [[x|z]]
    p_xz = re.compile(r'(([^!]|^)\[\[(.*)\|(.*)\]\])')

    #match links of form [[x#y]]
    p_xy = re.compile(r'(([^!]|^)\[\[(.*)\#(.*)\]\])')

    #match links of form [[x]]
    p_x = re.compile(r'(([^!]|^)\[\[(.*)\]\])')

    #match links of form [[#x]]
    p_hx = re.compile(r'(([^!]|^)\[\[\#(.*)\]\])')

    #match links of form [x](y)
    p_final_xy = re.compile(r'(([^!]|^)\[(.*)\]\(\#(.*)\))')

    #set prefix

    if internal_prefix is None:
        internal_prefix = ""

    #replace stuff
    #string replacementcomplete marks the link to not be caught by regex a second time

    #[[#x]] -> [x](#x)
    result = re.sub(p_hx, r"[\1](#\1)", text)

    # #![[a.png]] -> ![](/path/to/attachments/a.png)
    # result = re.sub(p_a, r"![]({}/\1)".format(attachments_rel), result)

    #[[x#y|z]] -> [z](prefix/x#y)
    result = re.sub(p_xyz, r"[\3]({}/\1#\2)".format(internal_prefix), result)

    #[[x|z]] -> [z](prefix/x)
    result = re.sub(p_xz, r"[\2]({}/\1)".format(internal_prefix), result)

    #[[x#y]] -> [y](prefix/x#y)
    result = re.sub(p_xy, r"[\2]({}/\1#\2)".format(internal_prefix), result)

    #[[x]] -> [x](prefix/x)
    result = re.sub(p_x, r"[\1]({}/#\1)".format(internal_prefix), result)

    # #finally, turn reformatted links into lowercase and hyphenated
    # replacement = lambda pat: "[" + pat.group(1) + "](#" + pat.group(2).lower().replace(" ", "-") + ")"
    # result = re.sub(p_final_xy, replacement, result)

    result = writeup_converter.create_contents(result) + "\n\n" + result

    # overwrite the file
    f_out = open(filepath, 'w')
    f_out.write(result)
    f_out.close()

def main():
    """take a specific file and copy the attachments from it into a new folder"""

    args = parse_args()

    filename = copy_file(args.source_file, args.target_folder)

    if not args.no_attachments:
        attachments = find_attachments(filename, args.source_attachments)
        writeup_converter.copy_attachments(attachments, args.target_attachments, args.verbose)

    if args.website:
        pdf_format(filename, args.url_prefix)

if __name__ == '__main__':
    main()