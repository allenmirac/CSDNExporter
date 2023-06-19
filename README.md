# CSDNExporter
## 介绍
CSDN 博客导出工具, 用于将 CSDN 博客导出为 Markdown / PDF 格式. 比较赞的地方在于, 它
不仅支持一篇博文的导出, 还支持将某个类目下的博文批量导出, 以及将导出的多篇博文汇总为
一篇, 以便用于全局搜索, 具体效果可以查看 .

## 运行脚本
- Linux系统运行
启动脚本为 `./run.sh`, 使用 `chmod +x run.sh` 增加其可执行权限;(并没有测试)
- Windows系统启动
启动脚本为`run.bat`, 双击打开或者在cmd中运行`run.bat`。

## 修改的地方

1、将下载的博客的图片分开保存在title..assets文件中，博客中有图片的时候才会创建图片目录，只会创建一次

utils.py 增加了一个参数title

```python
def __init__(self, html, title, is_win=False):
    self.html = html
    self.soup = BeautifulSoup(html, 'html.parser')
    self.outputs = []
    self.fig_dir = f'./figures/{title}'+'.assets'
    self.pre = False
    self.equ_inline = False
    self.is_win = is_win

    self.recursive(self.soup)
```

recursive(self, soup):

```python
def recursive(self, soup):
    …………
    elif tag == 'img':
        if not exists(self.fig_dir): # 博客中有图片的时候才会创建图片目录，只会创建一次
            os.makedirs(self.fig_dir)
    …………
```

2、输入用户名就可以直接找到的用户的博客专栏，拿到所有专栏下面的文章

run.bat 先将所有的categories保存在userName.txt中

```bash
if %download_category% == "true" (
  echo "Obtain blog directory link: save in userName.txt........"
  python -u link.py %userName%
)
```

再读取userName.txt文件的链接

```bash
for /f "tokens=* delims=" %%a in (m0_67623521.txt) do (
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
```

link.py

```python
user = sys.argv[1] # 拿到命令行下的用户名参数
```

将连接写入文件

```python
for li in lis:
    # print("####")
    url = li.find("a").attrs['href']
    title = li.find("span").attrs['title']
    titles.append(title)
    infos[title] = {"url":url}

    # print("[+]"+title+url)
    with open(user+'.txt','a+') as f:    #设置文件对象
        f.write(url)
        f.write('\n')
```

## 补充

另外要说明的是:

0. 安装必要的 Python 库, 如 `httpx`, `requests`, `BeautifulSoup`, `bs4`;
1. 为了解析图片链接, 需要安装 [aria2](https://aria2.github.io/), 并保证能在命令行启动;
2. 为了转换为 PDF, 需要安装 [Pandoc](https://pandoc.org/)，(博主该功能我并没有测试)。
3. 该博客导出工具再我的需求下就是拿到md文件，现在的功能我还是比较满意

## 对于安装aria2的问题

我参考了以下博文：

[电脑Windows安装Aria2配置详细教程全能的下载神器](https://blog.csdn.net/weizuer123/article/details/127411328)

[Aria2小白入门级部署](https://www.bilibili.com/read/cv21314846?from=search)

[超简单的Aria2使用教程](https://tomford1986.blogspot.com/2018/01/aria2.html)

[Aria2傻瓜安装部署指南](https://controlnet.space/2021/06/08/note/aria2-setup/)

[Aria2 & YAAW 使用说明](http://aria2c.com/usage.html)

如果想要下载配置好的aria2，可以在CSDN私聊[我的博客](https://blog.csdn.net/m0_67623521?type=blog) 。

## Author

[allenmirac-CSDNExporter](https://github.com/allenmirac/CSDNExporter)

# 巨人的肩膀

[axzml-CSDNExporter](https://github.com/axzml/CSDNExporter)

[导出 CSDN 博客至 Markdown 或 PDF 格式 (近乎完美)](https://blog.csdn.net/Eric_1993/article/details/104772437)

[获取指定博主所有专栏链接及博文链接](https://blog.csdn.net/qq_53381910/article/details/130816856)
