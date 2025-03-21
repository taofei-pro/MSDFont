import json
import os

def get_gb2312_chars():
    """获取GB2312编码的所有汉字"""
    gb2312_chars = []
    # GB2312编码范围：区位码从1区到87区，每区94个字符
    # 一级汉字：16-55区
    # 二级汉字：56-87区
    for i in range(16, 88):  # 16-87区
        for j in range(1, 95):  # 1-94位
            # 区位码转换为GB2312编码
            try:
                gb_code = bytes([i + 0xA0, j + 0xA0])
                char = gb_code.decode('gb2312')
                gb2312_chars.append(char)
            except:
                # 某些区位码可能无法解码，跳过
                continue
    
    print(f"GB2312编码共有{len(gb2312_chars)}个汉字")
    return gb2312_chars

def create_unseen_chars():
    """创建未见字符集，包含GB2312中不在M5.txt中的所有字符"""
    # 获取GB2312所有汉字
    gb2312_chars = get_gb2312_chars()
    
    # 读取M5.txt中的字符
    m5_txt_path = 'FontData/chn/ttfs/infer_unseen_font/M5.txt'
    with open(m5_txt_path, 'r', encoding='utf-8') as f:
        m5_chars = f.read().strip()
    
    print(f"M5.txt中共有{len(m5_chars)}个字符")
    
    # 找出GB2312中不在M5.txt中的字符
    unseen_chars = [char for char in gb2312_chars if char not in m5_chars]
    print(f"GB2312中不在M5.txt中的字符共有{len(unseen_chars)}个")
    
    # 保存到eval_unseen_chars.json
    with open('FontData/chn/eval_unseen_chars.json', 'w', encoding='utf-8') as f:
        json.dump(unseen_chars, f, ensure_ascii=False)
    
    print(f"已将{len(unseen_chars)}个未见字符保存到eval_unseen_chars.json")
    
    # 打印前20个字符作为示例
    print(f"前20个未见字符: {''.join(unseen_chars[:20])}...")

if __name__ == "__main__":
    create_unseen_chars()
