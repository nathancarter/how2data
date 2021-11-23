
--- Start new pages for each section header:

function Header (h)
  if h.level == 1 then
    return { pandoc.RawBlock('tex', '\\newpage'), h }
  else
    return h
  end
end

--- Put nice borders around each code section (thanks to tarleb on SO):
--- https://stackoverflow.com/questions/63525377/how-to-add-a-border-to-code-blocks-in-pandoc/63527166#63527166

function raw_tex (t)
  return pandoc.RawBlock('tex', t)
end

--- Wrap code blocks in longfbox environments
function CodeBlock (cb)
  return {raw_tex '\\begin{tcolorbox}', cb, raw_tex '\\end{tcolorbox}'}
end
