import argparse

def main():
    #setup argparse
    parser = argparse.ArgumentParser(prog="writeup-converter.py", description="Takes a folder of Obsidian markdown files and copies them across to a new location, automatically copying any attachments. Options available include converting to a new set of Markdown files, removing and adding prefixes to attachments, and converting for use on a website")

    #positional arguments
    parser.add_argument("source-folder", help="The folder of markdown files to copy from.")
    parser.add_argument("source-attachments", help="The attachments folder in your Obsidian Vault that holds attachments in the notes.")
    parser.add_argument("target-folder", help="The place to drop your converted markdown files")
    parser.add_argument("target-attachments", help="The place to drop your converted attachments. Must be set as your attachments folder in Obsidian (or just drop them in the root of your vault if you hate yourself)")

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

if __name__ == '__main__':
    main()