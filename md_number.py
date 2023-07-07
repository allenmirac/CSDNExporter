import os

# 目录路径
path = './markdown'

# 获取目录下所有文件及文件夹
all_files = os.listdir(path)

# 统计 .md 文件数量
md_file_count = 0
for file in all_files:
    if os.path.isfile(os.path.join(path, file)):
        if file.endswith('.md'):
            md_file_count += 1

print(f'目录 {path} 下有 {md_file_count} 个 .md 文件')
