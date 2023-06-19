@echo off
@title CSDNExporter

set download_category="false"
set download_article="false"
set userName="你的用户名"
set start_page=1
set page_num=100
set markdown_dir=markdown
set pdf_dir=pdf
set article_url="一篇文章的链接"

if %download_category% == "true" (
  echo "Obtain blog directory link: save in userName.txt........"
  python -u link.py %userName%
)

for /f "tokens=* delims=" %%a in (userName.txt) do (
  echo %%a
  if %download_category% == "true" (
      echo "Download a category"
      python -u main.py ^
          --category_url %%a ^
          --start_page %start_page% ^
          --page_num %page_num% ^
          --markdown_dir %markdown_dir% ^
          --pdf_dir %pdf_dir% ^
          --combine_together ^
          --to_pdf ^
          --is_win 1
          @REM --with_title ^
          @REM --rm_cache
   )
)

if %download_article% == "true" (
  echo "Download an article"
  python -u main.py ^
      --article_url %article_url% ^
      --markdown_dir %markdown_dir% ^
      --pdf_dir %pdf_dir% 
      --to_pdf ^
      --with_title ^
      --rm_cache ^
      --combine_together
      --is_win 1
)
pause