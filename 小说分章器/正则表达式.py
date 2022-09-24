import re
line = "第1章"
if not re.search(r'第[一二两三四五六七八九十○零百千0-9１２３４５６７８９０]{1,12}(章|节|節)', line):
    print("Y")