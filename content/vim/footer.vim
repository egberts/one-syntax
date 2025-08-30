
" one-syntax/content/vim/footer.vim begins here
if v:version >= 508
  delcommand HiLink
endif


let &cpoptions = s:cpo_save
unlet s:cpo_save


" syntax_on is passed only inside Vim's shell command for 2nd Vim to observe current syntax scenarios
let g:syntax_on = 1

" Google Vimscript style guide
" vim: et ts=2 sts=2 sw=2
scriptencoding iso-8859-5

" one-syntax/content/vim/footer.vim ends here
