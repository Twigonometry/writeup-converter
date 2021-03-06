# writeup-converter

A Python script for grabbing markdown files and Obsidian attachments from one folder and copying them to another. Also contains a 'website formatter' that uses regex to parse markdown headers and links and reformat them to create Jekyll-friendly links and contents tables.

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

**Python**

To use the Python script (recommended) you also need to [install Python 3.x](https://www.python.org/downloads/). For example, on Ubuntu:

```bash
$ sudo apt install python3.8
```

There are no dependencies to install as of writing this, as only core packages are used. But in future if your program will not run you can use pipreqs to generate a `requirements.txt` file locally and then install from it:

```bash
$ python3 -m pip install pipreqs
$ pipreqs /path/to/writeup-converter
$ python3 -m pip install -r /path/to/writeup-converter/requirements.txt
```

(I've mostly included this in the README because I thought it was cool and didn't want to forget it)

**Bash Script**

If you're using the bash script, make it executable:

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
- `-r REMOVE_PREFIX` specifies a prefix to remove from the attachment links that are copied across - e.g. if writeups in source folder live in a subdirectory `/Cybersecurity`, internal links to `[[Cybersecurity/Writeups/...]]` will become `[[Writeups/...]]`
- `-v VERBOSE` enables verbose mode, where all file names are outputted while copying. Can make the screen quite busy for a large directory
- `-w` tells the script to format your files for a website. This will combine them all into a single markdown file and reformat links, as well as adding a contents section to replace the obsidian index
- `-l` tells the script the relative path of your site's assets folder to use when creating image links when website formatting

### Python

Using any command line tool that has Python installed with it:

```bash
$ python3 writeup-converter.py -h
usage: writeup-converter.py [-h] [-a ADD_PREFIX] [-r REMOVE_PREFIX] [-v]
                            source_folder source_attachments target_folder
                            target_attachments

Takes a folder of Obsidian markdown files and copies them across to a new
location, automatically copying any attachments. Options available include
converting to a new set of Markdown files, removing and adding prefixes to
attachments, and converting for use on a website

positional arguments:
  source_folder         The folder of markdown files to copy from.
  source_attachments    The attachments folder in your Obsidian Vault that
                        holds attachments in the notes.
  target_folder         The place to drop your converted markdown files
  target_attachments    The place to drop your converted attachments. Must be
                        set as your attachments folder in Obsidian (or just
                        drop them in the root of your vault if you hate
                        yourself)

optional arguments:
  -h, --help            show this help message and exit
  -a ADD_PREFIX, --add_prefix ADD_PREFIX
                        Prefix to add to all your attachment file paths.
  -v, --verbose         Verbose mode. Gives details of which files are being
                        copied. Disabled by default in case of large
                        directories
```

For example, when I copied my Cereal writeup:

```bash
$ python3 writeup-converter.py -r Cybersecurity "/mnt/d/path/to/vault/Cybersecurity/Writeups/Hack the Box/Boxes/Cereal" /mnt/d/path/to/vault/Attachments/ "/mnt/d/OneDrive/OneDrive/Documents/Cybersecurity-Notes/Writeups/Hack the Box/Boxes/Cereal" /mnt/d/OneDrive/OneDrive/Documents/Cybersecurity-Notes/Attachments/
```

File paths with spaces in them must be wrapped in quotes. The program checks the source files exist before running, but it will create directories for targets if they don't exist:

```bash
$ python3 writeup-converter.py "/home/user/file with a space" /home/user/notreal /home/user/target/ /home/user/target-attachments/
Source folder path (/home/user/file with a space) is not a directory. Exiting
```

There's no need to also escape the quotes with `\` characters - some terminals will do this automatically if you autocomplete, but these extra backslashes should be removed if they're added.

#### Website Formatter

To copy a writeup but format it for a website, use the `--website` or `-w` flag. You must provide the name of the file to be outputted, but you can leave the rest of the options the same (where attachments folder here is an images directory etc rather than an obsidian attachments folder).

I use this after my initial conversion - i.e. I use the normal script to copy from a private vault to a public one and editing out anything I don't want, then use the `-w` flag to send it to my website repository.

The formatter will perform the following operations:
- concatenate all `.md` files it finds in the folder
- turn links of form `[[x]]` into `<a href="#x">x</a>`
- turn links of form `[[x#y]]` into `<a href="#y">y</a>`
- turn links of form `[[x|z]]` into `<a href="#x">z</a>`
- turn links of form `[[x#y|z]]` into `<a href="#y">z</a>`
- turn links of form `![[a.png]]` into `<img src="/path/to/attachments/a.png">`
- any links to obsidian notes not part of the folder being copied will just have the `[[` and `]]` strings stripped (TODO)

Example usage:

```bash
python3 writeup-converter.py -w 2021-06-12-htb-cereal.md -l /assets/images/blogs "/path/to/Cybersecurity-Notes/Writeups/Hack the Box/Boxes/Cereal/" "/path/to/Cybersecurity-Notes/Attachments/" "/path/to/Personal Site/mac-goodwin.com/mac-goodwin/blog/HTB/_posts/" "/path/to/Personal Site/mac-goodwin.com/mac-goodwin/assets/images/blogs/"
```

IMPORTANT NOTE: Sometimes copying large amount of files over to Jekyll folder while the server is running will crash the server and make it unresponsive to Ctrl+C, `pkill -9` etc. It's worth stopping serving before running the converter.

You may have to do a bit of manual work each time:
- Add an initial title to the markdown file
- Depending on how you number your files, the sections may be out of order (I commonly have `5 - Enumeration` and `10 - Website`, so Enumeration often ends up at the bottom)
- Remove any markdown files you *don't* want to include (for example, I often have an index file for linking the obsidian notes which is unnecessary on a website)
- Some links may not be turned into markdown links if they're just plain `http://...` links - this may be added as a feature in future
- You may need to add an initial yaml if using a templating engine like Jekyll
- Add/remove tags from the writeup as you see fit
- Add image captions/alt text (i.e. inside the square brackets in a `![]()` tag)
- Check all the links in the contents page work - it does a decent job, but can't always predict how element IDs will be generated, especially for ones with special characters
- If you're using a templating engine like Liquid, you may have to escape certain characters (for example, using a `{% raw %}` and `{% endraw %}` tag around occurrences of `{{}}`)

### Bash Script

```bash
$ ./writeup-converter [OPTIONS] [SOURCE_FOLDER] [SOURCE_ATTACHMENTS] [TARGET_FOLDER] [TARGET_ATTACHMENTS]
```

Options:
- `--help` displays usage

It's easiest to specify full paths. There is no need to wrap paths in quotation marks (it will actually break `grep` if you do), but you must escape spaces in paths with a backslash `\`

Prefix is not supported (it was easier to do it all in python at this point).