from email import contentmanager
import os
import re

'''"E:\Edge-coordinates\Book\网文\恐怖\深夜书屋.txt"'''
print("""小说分章器 V0.0.1
                by Edge-coordinates
- 输入 Q或q 退出
""")
while 1:
    filepath = input("请输入小说存放处的完整目录：")
    if filepath == 'Q' or filepath == 'q':
        break
    filepath = filepath.strip("'\"")
    if not os.path.isfile(filepath):
        print(filepath + "不是一个有效路径，请输入有效路径")
        os.system('pause')
    novelname = os.path.splitext(os.path.basename(filepath))[0]
    folderpath = filepath.split(".")[0]
    # print(folderpath)
    if not os.path.isdir(folderpath):
        os.mkdir(folderpath)
    f = open(filepath, 'r')
    content = f.readlines() # 按行读取
    l = 0 # 上一章的开始
    r = 0 # 本章的开始
    cnt = 0
    tn = ''
    for i in range(len(content)):
        line = content[i]
        if re.search(r'第[一二两三四五六七八九十○零百千0-9１２３４５６７８９０]{1,12}(章|节|節)', line):
            r = i
            tf = open(folderpath + '\\' + str(cnt).rjust(5,'0') + '_' + novelname + str(tn) + '.txt', 'w', encoding='utf-8')
            tf.writelines(content[l:r])
            tn = re.search(r'第[一二两三四五六七八九十○零百千0-9１２３４５６７８９０]{1,12}(章|节|節)', line).group()
            cnt += 1
            l = r

