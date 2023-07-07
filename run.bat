@echo off
@title CSDNExporter

set download_category="true"
set download_article="false"
set userName="Zero___0_0"
set start_page=1
set page_num=100
set markdown_dir=markdown
set pdf_dir=pdf
set article_url="https://blog.csdn.net/weixin_57165154/article/details/124131932"

if %download_category% == "true" (
  echo "Obtain blog directory link: save in userName.txt........"
  python -u link.py %userName%
)

for /f "tokens=* delims=" %%a in (Zero___0_0_categoty_link.txt) do (
  @REM echo %%a
  if %download_category% == "true" (
      echo "Download a category"
      python -u main.py ^
          --category_url %%a ^
          --start_page %start_page% ^
          --page_num %page_num% ^
          --markdown_dir %markdown_dir% ^
          --pdf_dir %pdf_dir% ^
          --combine_together ^
          --is_win 1
          @REM --to_pdf ^
          @REM --with_title ^
          @REM --rm_cache
   )
)

@REM if %download_article% == "true" (
@REM   echo "Download an article"
@REM   python -u main.py ^
@REM       --article_url %article_url% ^
@REM       --markdown_dir %markdown_dir% ^
@REM       --pdf_dir %pdf_dir% 
@REM       --to_pdf ^
@REM       --with_title ^
@REM       --rm_cache ^
@REM       --combine_together
@REM       --is_win 1
@REM )

if %download_article% == "true" (
  echo "Download an article"
  python -u main.py ^
      --article_url %article_url% ^
      --markdown_dir %markdown_dir% ^
      --with_title ^
      --rm_cache ^
      --is_win 1
)
pause