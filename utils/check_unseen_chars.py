import json

# 加载未见字符
with open('FontData/chn/eval_unseen_chars.json', 'r', encoding='utf-8') as f:
    unseen_chars = json.load(f)

# 加载字体中的字符（从我们之前提取的M5.txt，不包含后来添加的参考字符）
with open('FontData/chn/ttfs/infer_unseen_font/M5.txt', 'r', encoding='utf-8') as f:
    font_chars = f.read()
    # 移除我们后来添加的参考字符
    for char in ['侯', '候', '借']:
        if char in font_chars:
            font_chars = font_chars.replace(char, '')

# 检查未见字符是否在字体中
print('未见字符:', unseen_chars)
print('这些字符是否在M5.ttf中:')
for char in unseen_chars:
    print(f'{char}: {char in font_chars}')
