" Title goes here
" Language:     nftables configuration file
" Maintainer:   egberts <egberts@github.com>
" Revision:     1.1
" Initial Date: 2020-04-24
" Last Change:  2025-01-19
" Filenames:    nftables.conf, *.nft
" Location:     https://github.com/egberts/vim-nftables
" License:      MIT license
" Remarks:
" Bug Report:   https://github.com/egberts/vim-nftables/issues
"

if exists('nft_debug') && nft_debug == 1
  echomsg 'syntax/nftables-new.vim: called.'
  echomsg printf('&background: \'%s\'', &background)
  echomsg printf('colorscheme: \'%s\'', execute(':colorscheme')[1:])
endif

" quit if terminal is a black and white
if &t_Co <= 1
  finish
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
if v:version < 600
  syntax clear
elseif exists('b:current_syntax')
 " Quit when a (custom) syntax file was already loaded
  finish
endif

syn case match

" `iskeyword` severely impacts '\<' and '\>' atoms,
" don't use 'iskeyword' anywhere, it is useless against fully-deterministic pathway designs

let s:cpo_save = &cpoptions
set cpoptions&vim  " Line continuation '\' at EOL is used here
set cpoptions-=C

syn sync clear
syn sync maxlines=1000

" do 'syntax sync match' in app-specific Vim script file, not here

" one-syntax/content/vim/header.vim ends here
