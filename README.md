# Zcode - file encryption

A simple file encryption tool.

## Installation

Install the needed modules
`$ pip install -r requirements.txt`

Then you can add the script to your enviroment variables to use it anywhere.


## Usage

`python zcode.py <operation> <targets> -r`

- operation parameter:
  - `encode` or `e` to encrypt files.
  - `decode` or `d` to decrypt files.
- targets parameter:
  - you can use the wildcard syntax, you also can type in mutiple targets, you can understand more by the examples.
- recursive parameter:
  - the default behavior is ignoring directories, so if you want to recurse through directories and operate on them,you can provide this optional parameter by typing `-r` anywhere after the operation parameter, it recurses throught directories if found.
- encryption key
  - on usage it asks you to fill in with your prefered key string, which can be treated as regular passwords, then this password is converted to a valid key.

## Examples

1. encrypt all images in folder
`zcode e *.jpg *.png`

2. decrypt all pdf files in current direcroty recursively
`zcode d *.pdf -r`

3. encrypt specific files
`zcode e private.txt secret.txt`
