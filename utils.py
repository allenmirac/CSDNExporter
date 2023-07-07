#############################
# CopyRight ~~~~~~ ##########
# Author: allenmirac ########
# Date: 2023-06-19 ##########
#############################
from bs4 import BeautifulSoup, Tag, NavigableString, Comment
import os
from os.path import join, exists
import re
import subprocess
from download_img_queue import Download_img_queue

special_characters = {
    "&lt;": "<", "&gt;": ">", "&nbsp": " ",
    "&#8203": "",
}

class Parser(object):
    def __init__(self, html, title, img_queue_downloader, is_win=True):
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')
        self.outputs = []
        title = title.replace('.','').replace(':', ' ') # 文章标题中含有路径相关字符
        self.fig_dir = f'./figures/{title}'
        self.pre = False
        self.equ_inline = False
        self.is_win = is_win
        self.img_queue_downloader = img_queue_downloader
        self.recursive(self.soup)

    def remove_comment(self, soup):
        if not hasattr(soup, 'children'): return
        for c in soup.children:
            if isinstance(c, Comment):
                c.extract()
            self.remove_comment(c)

    def recursive(self, soup):
        if isinstance(soup, Comment): return
        elif isinstance(soup, NavigableString):
            for key, val in special_characters.items():
                soup.string = soup.string.replace(key, val)
            self.outputs.append(soup.string)
        elif isinstance(soup, Tag):
            tag = soup.name
            if tag in ['h1', 'h2', 'h3', 'h4', 'h5']:
                n = int(tag[1])
                soup.contents.insert(0, NavigableString('#'*n + ' '))
                soup.contents.append(NavigableString('\n'))
            elif tag == 'a' and 'href' in soup.attrs:
                soup.contents.insert(0, NavigableString('['))
                soup.contents.append(NavigableString("]({})".format(soup.attrs['href'])))
            elif tag in ['b', 'strong']:
                soup.contents.insert(0, NavigableString('**'))
                soup.contents.append(NavigableString('**'))
            elif tag in ['em']:
                soup.contents.insert(0, NavigableString('*'))
                soup.contents.append(NavigableString('*'))
            elif tag == 'pre':
                self.pre = True
            elif tag in ['code', 'tt']:
                if self.pre:
                    if not 'class' in soup.attrs:
                        language = 'bash'  # default language
                    else:
                        language = ''
                        for name in ['cpp', 'bash', 'python', 'java']:
                            if name in ' '.join(list(soup.attrs['class'])): # <code class="prism language-cpp">
                                language = name
                    soup.contents.insert(0, NavigableString('\n```{}\n'.format(language)))
                    soup.contents.append(NavigableString('\n```\n'))
                    self.pre = False  # assume the contents of <pre> contain only one <code>
                else:
                    soup.contents.insert(0, NavigableString('`'))
                    soup.contents.append(NavigableString('`'))
            elif tag == 'p':
                if soup.parent.name != 'li':
                    # print(soup.parent)
                    soup.contents.insert(0, NavigableString('\n'))
            elif tag == 'span':
                if 'class' in soup.attrs:
                    if ('katex--inline' in soup.attrs['class'] or
                       'katex--display' in soup.attrs['class']): ## inline math
                        self.equ_inline = True if 'katex--inline' in soup.attrs['class'] else False
                        math_start_sign = '$' if self.equ_inline else '\n\n$$'
                        math_end_sign = '$' if self.equ_inline else '$$\n\n'
                        # equation = soup.find_all('annotation', {'encoding': 'application/x-tex'})[0].string
                        equation = soup.find_all('span', {'class': 'katex-mathml'})[0].string
                        equation = equation.strip().split('\n')[-1].strip()
                        equation = math_start_sign + str(equation) + math_end_sign
                        self.outputs.append(equation)
                        self.equ_inline = False
                        return
            elif tag in ['ol', 'ul']:
                soup.contents.insert(0, NavigableString('\n'))
                soup.contents.append(NavigableString('\n'))
            elif tag in ['li']:
                soup.contents.insert(0, NavigableString('+ '))
                soup.contents.append(NavigableString('\n'))
            # elif tag == 'blockquote':
                # soup.contents.insert(0, NavigableString('> '))
            elif tag == 'img':
                
                src = soup.attrs['src']
                # print("src=", src)
                # pattern = r'.*\.png'

                # 使用本地下载的链接
                if not exists(self.fig_dir): # 博客中有图片的时候才会创建图片目录，只会创建一次
                    # print("makedir")
                    os.makedirs(self.fig_dir)
                pattern = r'(.*\..*\?)|(.*\.(png|jpeg|jpg|gif|ico))'
                # print(re.findall(pattern, src))
                result_tuple = re.findall(pattern, src)[0]
                # print(result_tuple)
                if result_tuple[0]:
                    img_file = result_tuple[0].split('/')[-1].rstrip('?')
                else:
                    img_file = result_tuple[1].split('/')[-1].rstrip('?')
                # img_file = re.findall(pattern, src)[0][0].split('/')[-1].rstrip('?') ## e.g. https://img-blog.csdnimg.cn/20200228210146931.png?
                
                img_file = os.path.join(self.fig_dir, img_file)
                img_file = img_file.replace("\\", "/")
                # img_file = img_file.replace(".", "")
                # print(img_file)
                
                # 单线程下载 图片
                # if self.is_win:
                #     # download_img_cmd = 'aria2c.exe --file-allocation=none -c -x 10 -s 10 -o {} {}'.format(img_file, src)
                #     download_img_cmd = ["aria2c.exe", "--file-allocation=none", "-c", "-x", "10", "-s", "10", "-o", save_path, url]
                # else:
                #     # download_img_cmd = 'aria2c --file-allocation=none -c -x 10 -s 10 -o {} {}'.format(img_file, src)
                #     download_img_cmd = ["aria2c", "--file-allocation=none", "-c", "-x", "10", "-s", "10", "-o", save_path, url]
                # if not exists(img_file):
                #     # os.system(download_img_cmd)
                #     subprocess.run(download_img_cmd)
                # soup.attrs['src'] = img_file
                # self.outputs.append('\n' + str(soup.parent) + '\n')

                # 多线程下载
                # 调用 download_images 函数，传入图片链接和保存路径的列表
                # download_img_queue.download_images(src, img_file, self.is_win)
                self.img_queue_downloader.add_task(src, img_file, self.is_win)

                img_name = os.path.basename(img_file)
                img_dir = '.'+img_file # 在上一级目录
                self.outputs.append('\n!['+img_name+']('+img_dir+')\n')

                # 图片直接使用CSDN的链接
                # code = f'![]({src})'
                # self.outputs.append('\n' + code + '\n')
                return
        if not hasattr(soup, 'children'): return
        for child in soup.children:
            self.recursive(child)


if __name__ == '__main__':
    # html = '<body><!-- cde --><h1>This is 1 &lt;= 2<!-- abc --> <b>title</b></h1><p><a href="www.hello.com">hello</a></p><b>test</b>'
    html = '<body><!-- cde --><h1>hello</h1><h2>world</h2></body>'
    parser = Parser(html)
    print(''.join(parser.outputs))
