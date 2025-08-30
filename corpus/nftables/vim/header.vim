" one-syntax/corpus/nftables/vim/header.vim begins here
"
"  ~/.vimrc flags used:
"
"      g:nftables_syntax_disabled, if exist then entirety of this file gets skipped
"      g:nftables_debug, extra outputs
"      g:nftables_colorscheme, if exist, then 'nftables.vim' colorscheme is used
""
"  This syntax supports both ANSI 256color and ANSI TrueColor (16M colors)
"
"  For ANSI 16M TrueColor:
"  - ensure that `$COLORTERM=truecolor` (or `=24bit`) at command prompt
"  - ensure that `$TERM=xterm-256color` (or `xterm+256color` in macos) at command prompt
"  - ensure that `$TERM=screen-256color` (or `screen+256color` in macos) at command prompt
"  For ANSI 256-color, before starting terminal emulated app (vim/gvim):
"  - ensure that `$TERM=xterm-256color` (or `xterm+256color` in macos) at command prompt
"  - ensure that `$COLORTERM` is set to `color`, empty or undefined
"
" Vimscript Limitation:
" - background setting does not change here, but if left undefined ... it's unchanged.
" - colorscheme setting does not change here, but if left undefined ... it's unchanged.
" - Vim 7+ attempts to guess the `background` based on term-emulation of ASNI OSC52 behavior
" - If background remains indeterminate, we guess 'light' here, unless pre-declared in ~/.vimrc
" - nftables variable name can go to 256 characters,
"       but in vim-nftables here, the variable name however is 64 chars maximum.
" - nftables time_spec have no limit to its string length,
"       but in vim-nftables here, time_spec limit is 11 (should be at least 23)
"       because '365d52w24h60m60s1000ms'.  Might shoot for 32.

" TIPS:
" - always add '\v' to any OR-combo list like '\v(opt1|opt2|opt3)' in `syntax match`
" - always add '\v' to any OR-combo list like '\v[a-zA-Z0-9_]' in `syntax match`
" - place any 'contained' keyword at end of line (EOL)
" - never use '?' in `match` statements
" - 'contains=' ordering MATTERS in `cluster` statements
" - 'region' seems to enjoy the 'keepend' option
" - ordering between 'contains=' and 'nextgroup=' statements, first one wins (but not in region)
" - ordering between 'contains=' statements amongst themselves, first one wins
" - ordering within 'contains=' statements, last one wins
" - ordering within 'nextgroup=' statements, last one wins
" - last comma must not exist on statement between 'contains='/'nextgroup' and vice versa
"
" Developer Notes:
"  - relocate inner_inet_expr to after th_hdr_expr?
"
" syntax/nftables.vim is called before colors/nftables.vim
" syntax/nftables.vim is called before ftdetect/nftables.vim
" syntax/nftables.vim is called before ftplugin/nftables.vim
" syntax/nftables.vim is called before indent/nftables.vim

if exists('nft_debug') && nft_debug == 1
  echomsg 'syntax/nftables-new.vim: called.'
  echomsg printf('&background: \'%s\'', &background)
  echomsg printf('colorscheme: \'%s\'', execute(':colorscheme')[1:])
endif

"if exists('g:loaded_syntax_nftables')
"    finish
"endif
"let g:loaded_syntax_nftables = 1

" .vimrc variable to disable html highlighting
if exists('g:nftables_syntax_disabled')
  finish
endif

" This syntax does not change background setting
" BUT it may later ASSUME a specific background setting

if exists('g:nft_debug') && g:nft_debug == 1
  echo 'Use `:messages` for log details'
endif

" experiment with loading companion colorscheme
if exists('nft_colorscheme') && g:nft_colorscheme == 1
  try
    if exists('g:nft_debug') && g:nft_debug == 1
      echomsg 'Loaded \'nftables\' colorscheme.'
    endif
    colorscheme nftables
  catch /^Vim\%((\a\+)\)\=:E185/
    echomsg 'WARNING: nftables colorscheme is missing'
    " deal with it
  endtry
else
  if exists('g:nft_debug') && nft_debug == 1
    echomsg 'No nftables colorscheme loaded.'
  endif
endif


if !exists('&background') || empty(&background)
  " if you want to get value of background, use `&background ==# dark` example
  let nft_obtained_background = 'no'
else
  let nft_obtained_background = 'yes'
endif

let nft_truecolor = 'no'
if !empty($TERM)
  if $TERM ==# 'xterm-256color' || $TERM ==# 'xterm+256color'
    if !empty($COLORTERM)
      if $COLORTERM ==# 'truecolor' || $COLORTERM ==# '24bit'
        let nft_truecolor = 'yes'
        if exists('g:nft_debug') && g:nft_debug == v:true
          echomsg '$COLORTERM is \'truecolor\''
        endif
      else
        if exists('g:nft_debug') && g:nft_debug == v:true
          echomsg '$COLORTERM is not truecolor'
        endif
      endif
    else
      if exists('g:nft_debug') && g:nft_debug == v:true
        echomsg $COLORTERM ' is empty'
      endif
    endif
  else
    if exists('g:nft_debug') && nft_debug == v:true
      echomsg $TERM ' does not have xterm-256color'
    endif
  endif
else
  echomsg $TERM is empty
endif

if exists(&background)
  let nft_obtained_background=execute(':set &background')
endif

" For version 6.x: Quit when a syntax file was already loaded
if !exists('main_syntax')
  let main_syntax = 'nftables'
endif

if exists('nft_debug') && nft_debug == 1
  echomsg printf('nft_obtained_background: %s', nft_obtained_background)
  echomsg printf('nft_truecolor: %s', nft_truecolor)
  if exists('g:saved_nft_t_Co')
    echomsg printf('saved t_Co %d', g:saved_nft_t_Co)
  else
    echomsg printf('t_Co %d', &t_Co)
  endif
"  if has('termguicolors')
"    if &termguicolors == v:true
"      echom('Using guifg= and guibg=')
"    else
"      echom('Using ctermfg= and ctermbg=')
"    endif
"  endif
endif

" Define the default highlighting.
" For version 5.7 and earlier: only when not done already
" For version 5.8 and later: only when an item doesn't have highlighting yet
if v:version >= 508 || !exists('did_nftables_syn_inits')
  if v:version < 508
    let did_nftables_syn_inits = 1
    command -nargs=+ HiLink hi link <args>
  else
    command -nargs=+ HiLink hi def link <args>
  endif

  HiLink nftHL_Type         Type
  HiLink nftHL_Command      Command
  HiLink nftHL_Statement    Statement
  HiLink nftHL_Number       Number
  HiLink nftHL_Comment      Comment
  HiLink nftHL_String       String
  HiLink nftHL_Label        Label
  HiLink nftHL_Keyword      Tag
  HiLink nftHL_Boolean      Boolean
  HiLink nftHL_Float        Float
  HiLink nftHL_Identifier   Identifier
  HiLink nftHL_Constant     Constant
  HiLink nftHL_SpecialComment SpecialComment
  HiLink nftHL_Error        Error
  HiLink nftHL_Separator    Delimiter
  HiLink nftHL_Define       Define
endif


" iskeyword severely impacts '\<' and '\>' atoms
" setlocal iskeyword=.,48-58,A-Z,a-z,\_,\/,-
setlocal isident=.,48-58,A-Z,a-z,\_

syn sync match nftablesSync grouphere NONE '^(rule|add {1,15}rule|table|chain|set)'
" syn sync fromstart '^(monitor|table|set)'
" syn sync fromstart


"hi link Variable              String
hi link Command               Statement

hi def link nftHL_String      String
hi def link nftHL_Variable    Variable
hi def link nftHL_Comment     Uncomment

hi def link nftHL_Include     Include
hi def link nftHL_ToDo        Todo
hi def link nftHL_Identifier  Identifier
hi def link nftHL_Number      Number
hi def link nftHL_Option      Label     " could use a 2nd color here
hi def link nftHL_Operator    Conditional
hi def link nftHL_Underlined  Underlined
hi def link nftHL_Error       Error
hi def link nftHL_Constant    Constant

hi def link nftHL_Command     Command
hi def link nftHL_Statement   Statement
hi def link nftHL_Expression  Conditional
hi def link nftHL_Type        Type

hi def link nftHL_Family      Underlined   " doesn't work, stuck on dark cyan
hi def link nftHL_Table       Identifier
hi def link nftHL_Chain       Identifier
hi def link nftHL_Rule        Identifier
hi def link nftHL_Map         Identifier
hi def link nftHL_Set         Identifier
hi def link nftHL_Element     Identifier
hi def link nftHL_Quota       Identifier
hi def link nftHL_Position    Number
hi def link nftHL_Limit       Number
hi def link nftHL_Handle      Number
hi def link nftHL_Flowtable   Identifier
hi def link nftHL_Device      Identifier
hi def link nftHL_Member      Identifier

hi def link nftHL_Verdict     Underlined
hi def link nftHL_Hook        Type
hi def link nftHL_Action      Special
hi def link nftHL_Delimiters  Normal
hi def link nftHL_BlockDelimiters  Normal

"hi link nftHL_BlockDelimitersTable  Delimiter
"hi link nftHL_BlockDelimitersChain  Delimiter
"hi link nftHL_BlockDelimitersSet    Delimiter
"hi link nftHL_BlockDelimitersMap    Delimiter
"hi link nftHL_BlockDelimitersFlowTable    Delimiter
"hi link nftHL_BlockDelimitersCounter Delimiter
"hi link nftHL_BlockDelimitersQuota  Delimiter
"hi link nftHL_BlockDelimitersCT     Delimiter
"hi link nftHL_BlockDelimitersLimit  Delimiter
"hi link nftHL_BlockDelimitersSecMark Delimiter
"hi link nftHL_BlockDelimitersSynProxy Delimiter
"hi link nftHL_BlockDelimitersMeter  Delimiter
"hi link nftHL_BlockDelimitersDevices Delimiter

if exists('g:nft_colorscheme')
  if exists('g:nft_debug') && g:nft_debug == v:true
    echom 'nft_colorscheme detected'
  endif
  hi def nftHL_BlockDelimitersTable  guifg=LightBlue ctermfg=LightRed ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersChain  guifg=LightGreen ctermfg=LightGreen ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersSet  ctermfg=17 guifg=#0087af ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersMap  ctermfg=17 guifg=#2097af ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersFlowTable  ctermfg=LightMagenta guifg=#950000 ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersCounter  ctermfg=LightYellow guifg=#109100 ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersQuota  ctermfg=DarkGrey ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersCT  ctermfg=Red guifg=#c09000 ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersLimit  ctermfg=LightMagenta ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersSecMark  ctermfg=LightYellow ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersSynProxy  ctermfg=DarkGrey guifg=#118100 ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersMeter  ctermfg=Red guifg=#720000 ctermbg=Black cterm=NONE
  hi def nftHL_BlockDelimitersDevices  ctermfg=Blue guifg=#303030 ctermbg=Black cterm=NONE
endif

"********* Leaf tokens (NOT-contained only)
hi link   nft_EOS nftHL_Error
syn match nft_EOS /\v[^ \t]{1,6}[\n\r\#]{1,3}/ skipempty skipnl skipwhite contained

"********* Leaf tokens (contained only)
hi link   nft_ToDo nftHL_ToDo
syn keyword nft_ToDo xxx contained XXX FIXME TODO TODO: FIXME: TBS TBD TBA
\ containedby=
\    nft_InlineComment

hi link   nft_Number nftHL_Number
syn match nft_Number /\<\d\+\>/ contained

hi link   nft_IP nftHL_Constant
syn match nft_IP '\v[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' contained

hi link   nft_String nftHL_String
syn match nft_String /"\([^"]\|\\."\)*"/ contained

hi link   nft_Comma nftHL_BlockDelimiters
syn match nft_Comma /,/ contained

hi link   nft_InlineComment nftHL_Comment
syn match nft_InlineComment '\v\# ' skipwhite contained

" **** BEGIN of ERROR CONDITIONS ****
hi link   nft_UnexpectedSymbol nftHL_Error
syn match nft_UnexpectedSymbol '\v\s{1,5}\zs[^a-zA-Z0-9]{1,64}' skipwhite contained

hi link   nft_UnexpectedSemicolon nftHL_Error
syn match nft_UnexpectedSemicolon '\v;{1,7}' skipwhite contained

hi link   nft_UnexpectedNewLine nftHL_Error
syn match nft_UnexpectedNewLine '\v\s{1,30}${1,7}' display contained

hi link   nft_UnexpectedHash nftHL_Error
syn match nft_UnexpectedNewLine '\v\s{1,30}${1,7}' display contained

hi link   nft_UnexpectedAtSymbol nftHL_Error
syn match nft_UnexpectedAtSymbol '\v\@' skipwhite contained

hi link   nft_UnexpectedQuote nftHL_Error
syn match nft_UnexpectedQuote '\v["\']' skipwhite contained

hi link   nft_UnexpectedVariableName nftHL_Error
syn match nft_UnexpectedVariableName '\v\$[a-zA-Z][a-zA-Z0-9\-_]{0,63}' skipwhite contained

hi link   nft_UnexpectedIdentifier nftHL_Error
syn match nft_UnexpectedIdentifier '\v[a-zA-Z][a-zA-Z0-9\-_]{0,63}' skipwhite contained

hi link   nft_UnexpectedNonIdentifier nftHL_Error
syn match nft_UnexpectedNonIdentifier '\v[a-zA-Z\/\.][\/\.a-zA-Z0-9\-_]{0,63}' skipwhite contained
" **** END of ERROR CONDITIONS ****

" === For map entries like 1 : 'value' ===
hi link   nft_MapEntry nftHL_Identifier
syn match nft_MapEntry '\v[0-9]{1,10}\s{1,32}:\s{1,32}\".{1,64}\"' contained

" === Clustered list elements ===
syn cluster nft_c_SetElements
\ contains=
\    nft_Number,
\    nft_IP,
\    nft_String,
\    nft_Comma

syn cluster nft_c_MapElements
\ contains=
\    nft_MapEntry,
\    nft_Comma

syn cluster nft_c_GenericElements
\ contains=
\    nft_Number,
\    nft_String,
\    nft_Comma

" === For map entries like '1 : "value"' ===
syn match nft_MapEntry /\d\+\s*:\s*".*"/ contained

" === Clustered list elements ===
syntax cluster nft_c_SetElements
\ contains=
\    nft_Number,
\    nft_IP,
\    nft_String,
\    nft_Comma

syntax cluster nft_c_MapElements
\ contains=
\    nft_MapEntry,
\    nft_Comma

syntax cluster nft_c_GenericElements
\ contains=
\    nft_Number,
\    nft_String,
\    nft_Comma

" === Curly blocks for set/map/elements (each with own element cluster) ===
syn region nft_SetBlock start=/{/ end=/}/ contained
\ contains=
\    @nft_c_SetElements

syn region nft_MapBlock start=/{/ end=/}/ contained
\ contains=
\    @nft_c_MapElements

syn region nft_ElementsBlock start=/{/ end=/}/ contained
\ contains=
\    @nft_c_GenericElements

" === Entry point rules ===
syn match nft_RhsExprForSet     /\<set\>\s\+\k\+\s*=\s*{[^}]*}/ contained
\ contains=
\    nft_SetBlock

syn match nft_RhsExprForMap /\<map\>\s\+\k\+\s*=\s*{[^}]*}/ contained
\ contains=
\    nft_MapBlock

syn match nft_RhsExprForElements /\<elements\>\s*=\s*{[^}]*}/ contained
\ contains=
\    nft_ElementsBlock



" stmt_separator (via nft_chain_block, nft_chain_stmt, @nft_c_common_block,
"                     counter_block, ct_expect_block, ct_expect_config,
"                     ct_helper_block, ct_helper_config, ct_timeout_block,
"                     ct_timeout_config, flowtable_block, limit_block,
"                     nft_line, nft_map_block, nft_quota_block,
"                     nft_secmark_block, nft_set_block, nft_synproxy_block,
"                     nft_synproxy_config, table_block )
hi link   nft_stmt_separator nftHL_Normal
syn match nft_stmt_separator '\v(\n|;)' skipwhite contained

" hi link   nft_hash_comment nftHL_Error
" syn match nft_hash_comment '\v#.{15,65}$' skipwhite contained

" syn match nft_Set contained /{.*}/ contains=nft_SetEntry contained
" syn match nft_SetEntry contained /[a-zA-Z0-9]\+/ contained
" hi def link nft_Set nftHL_Keyword
" hi def link nft_SetEntry nftHL_Operator

"syn match nft_Number '\<[0-9A-Fa-f./:]\+\>' contained contains=nft_Mask,nft_Delimiter
" syn match nft_Hex '\<0x[0-9A-Fa-f]\+\>' contained
" syn match nft_Delimiter '[./:]' contained
" syn match nft_Mask '/[0-9.]\+' contains=nft_Delimiter contained
" hi def link nft_Number nftHL_Number
" hi def link nft_Hex nftHL_Number
" hi def link nft_Delimiter nftHL_Operator
" hi def link nft_Mask nftHL_Operator

" Uncontained, unrestricted statement goes here
"
hi link   nft_MissingDeviceVariable nftHL_Error
syn match nft_MissingDeviceVariable '\v[^ \t\$\{]{1,5}' skipwhite contained " do not use 'keepend' here

hi link   nft_MissingCurlyBrace nftHL_Error
syn match nft_MissingCurlyBrace '\v[ \t]\ze[^\{]{1,1}' skipwhite contained " do not use 'keepend' here

hi link   nft_MissingSemicolon nftHL_Error
syn match nft_MissingSemicolon '\v\s{1,5}\zs[^;]{1,5}' skipwhite contained " do not use 'keepend' here

hi link   nft_UnexpectedCurlyBrace nftHL_Error
syn match nft_UnexpectedCurlyBrace '\v\s{0,7}[\{\}]' skipwhite contained " do not use 'keepend' here

hi link   nft_UnexpectedEmptyCurlyBraces nftHL_Error
syn match nft_UnexpectedEmptyCurlyBraces '\v\{\s*\}' skipwhite contained " do not use 'keepend' here

hi link   nft_UnexpectedEmptyBrackets nftHL_Error
syn match nft_UnexpectedEmptyBrackets '\v\[\s*\]' skipwhite contained " do not use 'keepend' here

hi link   nft_UnexpectedIdentifierChar nftHL_Error
syn match nft_UnexpectedIdentifierChar '\v(^[a-zA-Z0-9_\n]{1,3})' contained

hi link   nft_UnexpectedNumber nftHL_Error
syn match nft_UnexpectedNumber '\v[0-9\-\+]{1,4}' skipwhite contained

" We'll do error RED highlighting on all statement firstly, then later on
" all the options, then all the clauses.
" Uncomment following two lines for RED highlight of typos (still Beta here)
hi link   nft_UnexpectedEOS nftHL_Error
syn match nft_UnexpectedEOS contained '\v[\t ]{0,2}[\#;\n]{1,2}.{0,1}' contained

hi link   nft_Error_Always nftHL_Error
syn match nft_Error_Always /[^(\n|\r)\.]\{1,15}/ skipwhite contained

hi link   nft_rule_cluster_Error nftHL_Error
syn match nft_rule_cluster_Error /\v[\s\wa-zA-Z0-9_]{1,64}/ skipwhite contained  " uncontained, on purpose

hi link   nft_Error nftHL_Error
syn match nft_Error /\v[\s\wa-zA-Z0-9_]{1,64}/ skipwhite contained  " uncontained, on purpose

hi link   nft_expected_identifier nftHL_Error
syn match nft_expected_identifier /\v[^a-zA-Z]/ contained

hi link   nft_expected_equal_sign nftHL_Error
syn match nft_expected_equal_sign /\v[^=\s]/ contained

hi link   nft_expected_quote nftHL_Error
syn match nft_expected_quote /\v[^\"]/ skipwhite contained

hi link   nft_expected_dash nftHL_Error
syn match nft_expected_dash /\v[^\-]/ skipwhite contained

" Error if unexpected token appears after 'last'
hi link   nft_common_block_undefine_error nftHL_Error
syn match nft_common_block_undefine_error '\v[A-Za-z_][A-Za-z0-9_]{0,63}' contained

" Error if unexpected token appears after 'last'
hi link   nft_line_nonidentifier_error nftHL_Error
syn match nft_line_nonidentifier_error '\v[^ ]{1,35}[^A-Za-z_]{1}' contained

hi link   nft_line_nonvariable_error nftHL_Error
syn match nft_line_nonvariable_error '\v\$[^A-Za-z][^A-Za-z0-9_\-]{0,1}' skipwhite contained


" expected end-of-line (iterator capped for speed)
syn match nft_EOL /[\n\r]\{1,16}/ skipwhite contained

" syntax keyword nft_CounterKeyword last contained

" nft_Semicolon commented out to make way for syntax-specific semicolons
" hi link   nft_Semicolon nftHL_Operator
" syn match nft_Semicolon contained /\v\s{0,8}[;]{1,15}/  skipwhite contained

" Match the comment region (containing the entire line)
hi link   nft_comment_inline nftHL_Comment
syntax region nft_comment_inline start='\s*#' end='$' contained

hi link   nft_identifier_exact nftHL_Identifier
syn match nft_identifier_exact '\v[a-zA-Z][a-zA-Z0-9_\.]{0,63}' contained

" We limit to 63-char maximum for identifier name (for Vim session speed)
hi link   nft_identifier nftHL_Identifier
syn match nft_identifier '\v\w{0,63}' skipwhite contained
\ contains=
\    nft_identifier_exact,
\    nft_Error

hi link   nft_variable_identifier nftHL_Variable
syn match nft_variable_identifier '\v\$[a-zA-Z][a-zA-Z0-9_]{0,63}' skipwhite contained


syn match nft_datatype_arp_op '\v((request|reply|rrequest|rreply|inrequest|inreplyh|nak)|((0x)?[0-9a-fA-F]{4})|([0-9]{1,2}))' skipwhite contained
syn match nft_datatype_ct_dir '\v((original|reply)|([0-1]{1,1}))' skipwhite contained
syn match nft_datatype_ct_event '\v((new|related|destroy|reply|assured|protoinfo|helper|mark|seqadj|secmark|label)|([0-9]{1,10}))' skipwhite contained
syn match nft_datatype_ct_label '\v[0-9]{1,40}' skipwhite contained
syn match nft_datatype_ct_state '\v((invalid|established|related|new|untracked)|([0-9]{1,10}))' skipwhite contained
syn match nft_datatype_ct_status '\v((expected|seen-reply|assured|confirmed|snat|dnat|dying)|([0-9]{1,10}))' skipwhite contained
syn match nft_datatype_ether_addr '\v((8021ad|8021q|arp|ip6|ip|vlan)|((0x)?[0-9a-fA-F]{4}))' skipwhite contained
syn match nft_datatype_ether_type '\v[0-9]{1,10}' skipwhite contained
syn match nft_datatype_gid '\v[0-9]{1,10}' skipwhite contained
syn match nft_datatype_mark '\v[0-9]{1,10}' skipwhite contained
syn match nft_datatype_ip_protocol '\v((tcp|udp|udplite|esp|ah|icmpv6|icmp|comp|dccp|sctp)|([0-9]{1,3}))' skipwhite contained
syn match nft_datatype_ip_service_port '\v[0-9]{1,5}' skipwhite contained
syn match nft_datatype_ipv4_addr '\v[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' skipwhite contained
syn match nft_datatype_ipv6_addr /\v((([0-9a-fA-F]{1,4}:){1,7}:)|(::([0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4})|(([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}))/ skipwhite contained
syn match nft_datatype_packet_type '\v((host|unicast|broadcast|multicast|other)|([0-9]{1,5}))' skipwhite contained
syn match nft_datatype_realm '\v((default)|([0-9]{1,10}))' skipwhite contained
syn match nft_datatype_uid '\v(([a-z_][a-z0-9A-Z\._\-]{0,31})|([0-9]{1,10}))' skipwhite contained
syn match nft_meta_expr_datatype_devgroup '\v[0-9]{1,10}' skipwhite contained
syn match nft_meta_expr_datatype_iface_index '\v[0-9]{1,10}' skipwhite contained
syn match nft_meta_expr_datatype_ifkind '\v[a-zA-Z][a-zA-Z0-9]{1,16}' skipwhite contained
syn match nft_meta_expr_datatype_ifname '\v[a-zA-Z][a-zA-Z0-9]{1,16}' skipwhite contained
syn match nft_meta_expr_datatype_iface_type '\v((ether|ppp|ipip6|ipip|loopback|sit|ipgre)|([0-9]{1,5}))' skipwhite contained
syn match nft_meta_expr_datatype_day '\v([0-8]|Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)' skipwhite contained
syn match nft_meta_expr_datatype_hour '\v[0-2][0-9]:[0-5][0-9](:[0-5][0-9])?' skipwhite contained
syn match nft_meta_expr_datatype_time '\v(([0-9]{1,20})|iso_format)' skipwhite contained
syn match nft_payload_expr_datatype_ifname '\v[a-zA-Z][a-zA-Z0-9]{1,16}' skipwhite contained
syn match nft_payload_expr_datatype_tcp_flag '\v((fin|syn|rst|psh|ack|urg|ecn|cwr)|([0-9]{1,3}))' skipwhite contained

hi link   nft_line_separator nftHL_Define
syn match nft_line_separator  '\v[;\n]{1,16}' skipwhite contained

hi link   nft_line_stmt_separator nftHL_Separator
syn match nft_line_stmt_separator  '\v[;\n]{1,16}' skipwhite contained
