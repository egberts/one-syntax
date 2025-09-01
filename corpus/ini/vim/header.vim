
" Begin File: one-syntax/corpus/ini/vim/header.vim
" Description:
"    Add INI-specific vim here
"    Like:
"        highlight labels
"        some error handling

"  Highlights found
"   Highlight 'nftHL_String' referenced by nft_KEYWORD_equal_VALUE
highlight link nftHL_String String
"   Highlight 'nftHL_Operator' referenced by nft_KEYWORD_equal
highlight link nftHL_Operator Operator
"   Highlight 'nftHL_Identifier' referenced by nft_KEYWORD
highlight link nftHL_Identifier Identifier
"   Highlight 'nftHL_Statement' referenced by nft_lbracket_SECTION
highlight link nftHL_Statement Statement
"   Highlight 'nftHL_Delimiter' referenced by nft_lbracket
highlight link nftHL_Delimiter Delimiter
"   Highlight 'nftHL_Comment' referenced by nft_hash
highlight link nftHL_Comment Comment
"  Error Handlers encountered
syntax match nft_Error_equal_not_found '\v[^=]' contained


hi link   nft_Error nftHL_Error
syn match nft_Error /\v.{1,15}/ skipwhite contained " uncontained, on purpose


" End of File: one-syntax/corpus/ini/vim/header.vim
