# 为内容添加Front-matter

"""
功能
- 根据文件名生成标题
- 根据文件目录生成分类和标签
- 如果文章以`转载`, `zhuanzai`开头，自动加上转载标识
- 保留所有 ===分割号后的自定义分类和标签
- 不为生成过的文件重新生成 & 自定义排除文件夹or文件
"""

"""
---
title: Hello World
categories:
- Diary
tags:
- PS3
- Games
---
"""

import os

def fm_dev(rpath, tname, oldf = []): # 生成Front-matter
    rpath = rpath.split(os.path.sep)
    tit = "title: " + tname + "\n"
    tmpl = ["---\n", tit, "categories:\n", "tags:\n"]
    tmpl = tmpl + oldf + ["---\n"]

    if rpath[0] == '.': tmpl.insert(tmpl.index("categories:\n") + 1, "- Life\n") # 根目录下所有文件处于 Life 分类
    else: tmpl.insert(tmpl.index("categories:\n") + 1,"- " + rpath[0] + "\n")

    """路径中剩下的部分作为标签"""
    if len(rpath) > 1 :
        for i in range(1, len(rpath)):
            tmpl.insert(tmpl.index("tags:\n") + 1,"- " + rpath[i] + "\n")

    if rpath[0] == 'Net-excerpt': tmpl.insert(len(tmpl) - 1, "reprint: true\n") # 主题内自定义设置，转载文章标记

    return tmpl


fapath = os.path.split(os.path.realpath(__file__))[0]

for folderName, subfolders, filenames in os.walk(fapath):
    for filename in filenames:
        # 获取前缀（文件名称）
        tname = os.path.splitext(filename)[0]
        if os.path.splitext(filename)[-1][1:] == "md" :

            rpath = os.path.relpath(folderName, fapath) # 获取相对路径
            filepath = rpath + "\\" + filename # 获取文件的相对路径
            # print(filepath) # 测试路径是否正确
            TFile = open(filepath, 'r', encoding='utf-8') # 打开文件(只读)
            conntent = TFile.readlines() # 按行读取
            TFile.close() # 关闭文件

            if(conntent[0] == "---\n"): # 处理过的
                continue
                # """找到Front-matter的位置"""
                # for i in range(1, len(conntent)):
                #     if(conntent[i] == "---\n"):
                #         break
                
                # """保留可能手动设置的信息"""
                # oldf = []
                # if "Flagold: true\n" in conntent : oldf = conntent[conntent.index("Flagold: true\n"): i]
                # if "reprint: true\n" in oldf: oldf.remove("reprint: true\n")

                # """生成Fornt-matter并写入文件"""
                # conntent = fm_dev(rpath, tname, oldf) + conntent[i+1:]
                # TFile = open(filepath, 'w', encoding='utf-8')
                # TFile.writelines(conntent)
                # TFile.close()

            else:
                conntent = fm_dev(rpath, tname) + ["\n\n"] + conntent
                TFile = open(filepath, 'w', encoding='utf-8')
                TFile.writelines(conntent)
                TFile.close()