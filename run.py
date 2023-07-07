import os
import subprocess
import time

# Zero___0_0
# java_t_t
download_category = True
download_article = False
userName = "java_t_t"
start_page = 1
page_num = 100
markdown_dir = "markdown"
pdf_dir = "pdf"
article_url = "https://blog.csdn.net/weixin_57165154/article/details/124131932"

time_start = time.time()
if download_category:
    print("Obtain blog directory link: save in userName.txt........")
    subprocess.call(["python", "-u", "link.py", userName])

with open(f"{userName}_categoty_link.txt", "r") as file:
    for line in file:
        category_url = line.strip()
        if download_category:
            print("Download a category")
            subprocess.call(["python", "-u", "main.py",
                             "--category_url", category_url,
                             "--start_page", str(start_page),
                             "--page_num", str(page_num),
                             "--markdown_dir", markdown_dir,
                             "--pdf_dir", pdf_dir,
                             "--combine_together",
                             "--is_win", "1"])

if download_article:
    print("Download an article")
    subprocess.call(["python", "-u", "main.py",
                     "--article_url", article_url,
                     "--markdown_dir", markdown_dir,
                     "--with_title",
                     "--rm_cache",
                     "--is_win", "1"])
print()
print("----------------------------")
time_end = time.time()
print("Total time spent:", time_end-time_start, " !")
input("Press any key to continue...")

