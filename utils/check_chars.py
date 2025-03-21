import json

# 加载参考字符
with open('FontData/chn/ref_chars.json', 'r', encoding='utf-8') as f:
    ref_chars = json.load(f)

# 加载字体中的字符
with open('FontData/chn/ttfs/infer_unseen_font/M5.txt', 'r', encoding='utf-8') as f:
    font_chars = f.read()

# 检查参考字符是否在字体中
print('参考字符:', ref_chars)
print('这些字符是否在M5.txt中:')
for char in ref_chars:
    print(f'{char}: {char in font_chars}')

# 如果有缺失的字符，创建一个新的M5.txt，添加这些字符
missing_chars = [char for char in ref_chars if char not in font_chars]
if missing_chars:
    print(f'\n缺失的字符: {missing_chars}')
    print('将这些字符添加到M5.txt中...')
    with open('FontData/chn/ttfs/infer_unseen_font/M5.txt', 'w', encoding='utf-8') as f:
        f.write(font_chars + ''.join(missing_chars))
    print('已更新M5.txt文件')
