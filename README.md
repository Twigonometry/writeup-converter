# writeup-converter
Quick and dirty bash script for grabbing attachments from one Obsidian folder and copying them to another

I got sick of manually copying the images and attachments I'd used in a writeup when I moved from my private vault to my public one. There seems to be no official way of exporting a folder in Obsidian, so I made one myself

I use this to copy a writeup across to another folder, but you could in theory use it for copying any folder with attachments in it to any location

I may in future turn this into an Obsidian plugin

## Install

```
$ git@github.com:Twigonometry/writeup-converter.git
$ cd writeup-converter
$ chmod +x writeup-converter
```

## Usage

```
$ ./writeup-converter [OPTIONS] [SOURCE_FOLDER] [SOURCE_ATTACHMENTS] [TARGET_FOLDER] [TARGET_ATTACHMENTS]
```

Options:
- `--help` displays usage
- `-p PREFIX` specifies a prefix to remove from the attachment links that are copied across - e.g. if writeups in source folder live in a subdirectory `/Cybersecurity`, internal links to `[[Cybersecurity/Writeups/...]]` will become `[[Writeups/...]]`

Arguments:
- Source Folder: The writeup you want to copy. Copies the entire directory
- Source Attachments: The path to the obsidian attachments folder where attachments are saved in your writeup
- Target Folder: Where you want to copy the writeup to. No need to make the folder beforehand - copying `/path/to/source/Writeups/Hack\ the\ Box/Boxes/Blue/` to `/path/to/target/Writeups/Hack\ the\ Box/Boxes/` will create the `Blue` directory for you
- Target Attachments: The path to the obsidian attachments folder in your new location

It's easiest to specify full paths. There is no need to wrap paths in quotation marks (it will actually break `grep` if you do), but you must escape spaces in paths with a backslash `\`