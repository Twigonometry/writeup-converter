# writeup-converter

A Python script for grabbing markdown files and Obsidian attachments from one folder and copying them to another.

Also contains a quick and dirty bash script that does the same thing with less pizzazz.

## Why did I make this?

I got sick of manually copying the images and attachments I'd used in a writeup when I moved from my private vault to my public one. There seems to be no official way of exporting a folder in Obsidian, so I made one myself.

I use this to copy a writeup across to another folder, but you could in theory use it for copying any folder with attachments in it to any location.

I may in future turn this into an Obsidian plugin (but no promises).

## Installation

Using git:

```
$ git clone git@github.com:Twigonometry/writeup-converter.git
```

To use the Python script (recommended) you also need to [install Python 3.x](https://www.python.org/downloads/)

To prepare the bash script for use:

```bash
$ cd writeup-converter
$ chmod +x writeup-converter
```

## Usage

**General Notes on Arguments**

Positional Arguments:
- Source Folder: The writeup you want to copy. Copies the entire directory
- Source Attachments: The path to the obsidian attachments folder where attachments are saved in your writeup
- Target Folder: Where you want to copy the writeup to. No need to make the folder beforehand - copying `/path/to/source/Writeups/Hack\ the\ Box/Boxes/Blue/` to `/path/to/target/Writeups/Hack\ the\ Box/Boxes/` will create the `Blue` directory for you
- Target Attachments: The path to the obsidian attachments folder in your new location

Optional Arguments
- `-p PREFIX` specifies a prefix to remove from the attachment links that are copied across - e.g. if writeups in source folder live in a subdirectory `/Cybersecurity`, internal links to `[[Cybersecurity/Writeups/...]]` will become `[[Writeups/...]]`

### Python

Using any command line tool that has Python installed with it:

```bash
$ python3 writeup-converter.py -h
usage: writeup-converter.py [-h] [-a ADD_PREFIX] [-r REMOVE_PREFIX]
                            source-folder source-attachments target-folder
                            target-attachments

Takes a folder of Obsidian markdown files and copies them across to a new 
location, automatically copying any attachments. Options available include
converting to a new set of Markdown files, removing and adding prefixes to
attachments, and converting for use on a website

positional arguments:
  source-folder         The folder of markdown files to copy from.
  source-attachments    The attachments folder in your Obsidian Vault that
                        holds attachments in the notes.
  target-folder         The place to drop your converted markdown files
  target-attachments    The place to drop your converted attachments. Must be
                        set as your attachments folder in Obsidian (or just
                        drop them in the root of your vault if you hate
                        yourself)

optional arguments:
  -h, --help            show this help message and exit
  -a ADD_PREFIX, --add-prefix ADD_PREFIX
                        Prefix to add to all your attachment file paths.
  -r REMOVE_PREFIX, --remove-prefix REMOVE_PREFIX
                        Prefix to remove from all your attachment file paths.
```

For example:

```bash
$ python3 writeup-converter.py -r "Remove this prefix" /home/user/vault/writeup/ /home/user/vault/attachments/ /home/user/target/ /home/user/target/attachments/
```

File paths with spaces in them must be wrapped in quotes. The program checks the source files exist before running, but it will create directories for targets if they don't exist:

```bash
$ python3 writeup-converter.py "/home/user/file with a space" /home/user/notreal /home/user/target/ /home/user/target-attachments/
Source folder path (/home/user/file with a space) is not a directory. Exiting
```

### Bash Script

```bash
$ ./writeup-converter [OPTIONS] [SOURCE_FOLDER] [SOURCE_ATTACHMENTS] [TARGET_FOLDER] [TARGET_ATTACHMENTS]
```

Options:
- `--help` displays usage

It's easiest to specify full paths. There is no need to wrap paths in quotation marks (it will actually break `grep` if you do), but you must escape spaces in paths with a backslash `\`

Prefix is not supported (it was easier to do it all in python at this point).