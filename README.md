# one-syntax
Put in your own file format and generate a syntax highlighter

At the moment, the following core functionality works:

1. Use UNIX directory/file as deterministic pathway to proper keyword sequences
2. Supports squishy keywords (keywords with no whitespace in between)
3. Supports lookahead deterministic error highlighting
4. Reverse transversal of pathways (to support various highlighters' need to put largest static pattern first before complex wildcards)
5. Sort child pathways of keywords by largest lexical string length firstly.
6. Sort child pathways of regex by largest static lexical pattern down to most complex regex down to simple '+'/'\*' wildcard.

# Plan

1. Take a EBNF-format file and spit out the directory/files of proper keyword sequences
2. Support Vimscript syntax.
3. Support TextMate.
4. Support JetBrains Lexer + Parser + PSI-based syntax highlighting (often referred to simply as a JetBrains Language Plugin).  (Oh boy, JetBrain needs a product name there, like badly.)
5. Profit?
6. Take over the world?
7. Nah. It's all in fun.

