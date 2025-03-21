import json
import random

# 加载字体中的字符（原始提取，不包含后来添加的参考字符）
with open('FontData/chn/ttfs/infer_unseen_font/M5.txt', 'r', encoding='utf-8') as f:
    font_chars = f.read()
    # 移除我们后来添加的参考字符
    for char in ['侯', '候', '借']:
        if char in font_chars:
            font_chars = font_chars.replace(char, '')

# 从字体中随机选择3个字符作为新的参考字符
font_chars_list = list(font_chars)
if len(font_chars_list) >= 3:
    new_ref_chars = random.sample(font_chars_list, 3)
    
    # 保存新的参考字符集
    with open('FontData/chn/new_ref_chars.json', 'w', encoding='utf-8') as f:
        json.dump(new_ref_chars, f, ensure_ascii=False)
    
    print(f'已创建新的参考字符集: {new_ref_chars}')
    
    # 创建新的未见字符集（只包含"上"和"世"）
    new_unseen_chars = ['上', '世']
    with open('FontData/chn/new_eval_unseen_chars.json', 'w', encoding='utf-8') as f:
        json.dump(new_unseen_chars, f, ensure_ascii=False)
    
    print(f'已创建新的未见字符集: {new_unseen_chars}')
else:
    print('字体中的字符不足，无法创建新的参考字符集')
