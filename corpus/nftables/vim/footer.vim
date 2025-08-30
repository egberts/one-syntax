

" one-syntax/content/vim/footer.vim starts here
if !exists('did_nftables_syn_inits')
  delcommand HiLink
endif

if main_syntax ==# 'nftables'
  unlet main_syntax
endif

" syntax_on is passed only inside Vim's shell command for 2nd Vim to observe current syntax scenarios
let b:current_syntax = 'nftables'


" one-syntax/corpus/nftables/vim/footer.vim ends here
