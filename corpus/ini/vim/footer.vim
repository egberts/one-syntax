
"  Highlights found
"   Highlight 'String' referenced by nft_KEYWORD_equal_VALUE
highlight def link nftHL_String String
highlight def link nftHL_Statement Statement
"   Highlight 'Operator' referenced by nft_KEYWORD_equal
highlight def link nftHL_Operator Define
highlight def link nftHL_Comment  Comment
highlight def link nftHL_Identifier  Identifier
highlight def link nftHL_Delimiter  Delimiter
highlight def link nftHL_Error  Error

"   Highlight 'Command' referenced by nft_KEYWORD
"  Error Handlers encountered
hi link   nft_Error_identifier_not_found nftHL_Error
syn match nft_Error_identifier_not_found '\v[^ a-zA-Z0-9_\-\.\$]' contained

hi link   nft_Error_equal_not_found nftHL_Error
syn match nft_Error_equal_not_found '\v[^=]' contained

hi link   nft_Error nftHL_Error
syn match nft_Error /\v[\s\wa-zA-Z0-9_]{1,64}/ skipwhite " uncontained, on purpose
