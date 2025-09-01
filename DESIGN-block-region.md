This DESIGN-block-region.md document details the incorporation of
block/region denoted by a pair of delimiters into the One-Syntax design.

A region/block is surrounded by a delimiter of '{', '[', '(' or '<' symbol and its corresponding end delimiter.

As a result, the directory/file structure needs to deal with this 'off-shoot' of
keyword pathways.  The ordinary syntax pathway follows the directory nesting down
to the last keyword of a line.

The block/region needs additional tracking of delimiters (and all its first-order keywords found within its block/region) added on top of this One-Syntax directory/file structure.

To handle the addition of this orthogonal offshoot of directory nesting, a special filename prefix `block.` is deployed and used here.  A token 'define' residing in a block has a filename `block.define` inside the block delimiter directory (i.e., '[').

This makes it possible to distinguish between continuation after a block versus handling all keywords within a block.

Continuation after a block will be covered by directory names not having a `block.` prefix.

Now, we have left are tracking the delimiter-pair.  Some methods are:

1. Explicit via a `[` delimiter file, use `.config.ini` to track each `block.` pathway for its end-node; driven by start delimiters' `.config.ini` containing all subdirectory names.
2. Explicit via a `[` delimiter file, use `]` delimiter file as its end-node; driven by end delimiters' `.config.ini`.  Rest of pathway after ']' are clearly delineated.
3. Implicit via `.config.ini` in last keyword before its block region; driven by last keyword before region.
4. Implicit via `.config.ini` in each `block.`-prefixed keyword directory. Driven by `block.`-prefix directory name.

# Start Delimiter Directory, config-driven, End delimiter also in start directory

The config file contains the subdirectory names that it wish to tuck inside the region/block.  Rest of the tokens in that directory are traversed as normally after the end of its region block (not common, but still required).

Start delimiter `[` directory contains TWO sets of pathways:

1. things that goes inside the region block
2. things that follows after the end delimiter part of region block

End delimiter `]` subdirectory would reside under `[` directory.  

    CLI:  table chain [ ]
    Path: TABLE/CHAIN/[/]
    Name: TABLE_CHAIN_lbracket_rbracket

Special hook must monitor for `]` in traversal tree.  OR special hook must monitor for end-node terminal and THEN artificially-traverse resume at the `]` non-terminal node.   Only place for funkiness of traversal is this region-block handling.

End delimiter `]` directory contains THE follow-on keyword(s)/token(s) in continuation of pathway in normal fashion.

Uses `]` exactly ONCE, and always inside `[` directory.  Never sym-linked.  Excellent maintainability.

Terminal end-node somewhere inside blocks are denoted as link to nothing further (no child subdirectory) and do not need to add `]`subdirectory.

Pro: no need for `block.`-prefix notation; AST looks correct; traversal needs tweaking for corresponding end delimiter directory then resume at same-level to `]` directory; a simple block processing function inserted into the existing traversal tree coding.
Cons: renaming directory breaks synchronization with config

# End Delimiter Directory, config-driven, End delimiter as end-node

Same as start delimiter directory above, but the `]` is placed at each of each pathway found entirely within its region-block making its syntax tree a true deterministic but explosive AST pathway.

    CLI:  table chain [ define A = 1 ];
    Path: TABLE/CHAIN/[/define/KEYWORD/=/VALUE/]/;
    Name: TABLE_CHAIN_lbracket_define_KEYWORD_equal_VALUE_rbracket_endOfStatement

Pros: easiest to maintain AST (directory/file), especially if soft symlink is leverage to redeploy common semantic action (or symbolic state transition) such as `family_spec` in nftables.  Simplifies `]` maintenance if symlinked to end of each pathway inside its block: any changes to `]` impacts all.
Cons: "Millions" of pathway defined; practically impossible to maintain after generation. If a block cannot be empty, then `]` cannot reside in `[` directory, leaves a dilemma of where to maintain centralized `]` before soft-linking.

This lack of centralized `]` terminal end-node may be a deal killer here, if ease-of-programming is its design priority.


# Implicit via leading token/keyword (keyword before block)

    Path: TABLE/CHAIN/block.KEYWORD/=/VALUE/;
    Name: TABLE_CHAIN_lbracket_define_KEYWORD_equal_VALUE_rbracket_endOfStatement
    Config:     ^^^^^

# Implicit via start delimiter directory name (before block-keyword)

    Path: TABLE/CHAIN/[/block.KEYWORD/=/VALUE/;
    Name: TABLE_CHAIN_lbracket_define_KEYWORD_equal_VALUE_rbracket_endOfStatement
    Config:           ^^^^^
# Implicit via `block.`-prefixed directory name (post keyword)

    Path: TABLE/CHAIN/[/block.KEYWORD/=/VALUE/;
    Name: TABLE_CHAIN_lbracket_define_KEYWORD_equal_VALUE_rbracket_endOfStatement
    Config:           ^^^^^

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
There are two ways to denote an end-region, thus accommodating this orthogonal offshoot from various directory points in the abstract syntax tree.

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

Also, it would help delineate the `start=`/`end=` delimiter sooner.


