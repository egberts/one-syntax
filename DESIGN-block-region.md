This DESIGN-block-region.md document details the incorporation of
block/region denoted by a pair of delimiters into the One-Syntax design.

A region/block is surrounded by a delimiter of '{', '[', '(' or '<' symbol and its corresponding end delimiter.

As a result, the directory/file structure needs to deal with this 'off-shoot' of
keyword pathways.  The ordinary syntax pathway follows the directory nestings down
to the last keyword of a line.

The block/region needs additional tracking of delimiters (and all its first-order keywords found within its block/region) added on top of this One-Syntax directory/file structure.

To handle the addition of this orthogonal offshot of directory nesting, a special filename prefix `block.` is deployed and used here.  A token 'define' residing in a block has a filename `block.define` inside the block delimiter directory (i.e., '[').

This makes it possible to distinguish between continuation after a block versus handling all keywords within a block.

Continuation after a block will be covered by directory names not having a `block.` prefix.

# Start and End delimiter

Question remains is how to denote the end delimiter?  Is it terminal-node-based (file-based) or `.config.ini`-based?

Do we let only the `.config.ini` determine if it is a block region or not?  This would make it harder to see in the directory tree which are blocked-in, or nest-blocked.

There are two pathways from a start-region block :

1. tokens that are found inside the block region
2. tokens that are followed after the end-part of a block region

Using a directory/file design for our AST-approach does not support for orthogonal
conjectures offshooting from a directory, other than a filename: hence the introduction of `block.` prefix to region-specific filenames.

## Start Delimiter Directory
Do we let `[` directory name dictate the start region?  What about the end region, do we make a `]` directory to denote the end of a block/region?

`[` directory would then hold all the tokens inside a region-block via `block.` prefix filename.  Nice a simple.

## End Delimiter Directory
There are two ways to denote an end-region, thus accomodating this orthogonal offshoot from various directory points in the abstract syntax tree.

1.  Implicit via end-node terminal file.
2.  Explicit via a `[` directory


With the `]` end-region, it becomes a must, due to continuation pathway required by `nextgroup=` in `syntax region start= end=`.



# Terminal-Node-Base End-Delimiter
An example of terminal-node-base end-delimiter would have a path like:

    config/syntax/ini/[/SECTION/] 

The ']' would be a directory, the terminal end-node.  It's 

If using an end-node/terminal file as the indicator of completion within that pathway inside a block, then recursion may resume with `contains=` then `nextgroup=`.

# `.config.ini`-based
If denoting a region/block by a parameter defined in its configuration file located inside the delimiter subdirectory, then delimiter name can be like a "start"/"end" as well as symbol-pair.

Also, it would help delineanate the `start=`/`end=` delimiter sooner.


