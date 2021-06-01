# writeup-converter

A Python script for grabbing markdown files and Obsidian attachments from one folder and copying them to another.

Also contains a quick and dirty bash script for grabbing attachments from one Obsidian folder and copying them to another

## Why did I make this?

I got sick of manually copying the images and attachments I'd used in a writeup when I moved from my private vault to my public one. There seems to be no official way of exporting a folder in Obsidian, so I made one myself.

I use this to copy a writeup across to another folder, but you could in theory use it for copying any folder with attachments in it to any location.

I may in future turn this into an Obsidian plugin (but no promises).

## Install

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
$ python3 writeup-converter.py 
usage: writeup-converter.py [-h] [-a ADD_PREFIX] [-r REMOVE_PREFIX]
                            source-folder source-attachments target-folder
                            target-attachments
writeup-converter.py: error: the following arguments are required: source-folder, source-attachments, target-folder, target-attachments
```

For example:



### Bash Script

```bash
$ ./writeup-converter [OPTIONS] [SOURCE_FOLDER] [SOURCE_ATTACHMENTS] [TARGET_FOLDER] [TARGET_ATTACHMENTS]
```

Options:
- `--help` displays usage

It's easiest to specify full paths. There is no need to wrap paths in quotation marks (it will actually break `grep` if you do), but you must escape spaces in paths with a backslash `\`

Prefix is not supported (it was easier to do it all in python at this point).