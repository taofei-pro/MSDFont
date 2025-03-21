import json
import random
import argparse

def create_ref_chars(num_chars=None, random_seed=42):
    """
    从M5.txt中创建参考字符集
    
    参数:
    num_chars: 要选择的字符数量，如果为None则使用全部字符
    random_seed: 随机种子，用于随机选择字符时保持一致性
    """
    # 设置随机种子以保证结果可重现
    random.seed(random_seed)
    
    # 读取M5.txt中的所有字符
    with open('FontData/chn/ttfs/infer_unseen_font/M5.txt', 'r', encoding='utf-8') as f:
        all_chars = f.read()
    
    total_chars = len(all_chars)
    print(f"M5.txt中共有{total_chars}个字符")
    
    # 如果num_chars为None或大于总字符数，使用所有字符
    if num_chars is None or num_chars >= total_chars:
        selected_chars = list(all_chars)
        print(f"使用全部{total_chars}个字符作为参考字符")
    else:
        # 随机选择指定数量的字符
        selected_chars = random.sample(list(all_chars), num_chars)
        print(f"从{total_chars}个字符中随机选择了{num_chars}个字符作为参考字符")
    
    # 保存到ref_chars.json
    with open('FontData/chn/ref_chars.json', 'w', encoding='utf-8') as f:
        json.dump(selected_chars, f, ensure_ascii=False)
    
    print(f"已将选定的字符保存到ref_chars.json")
    
    # 如果字符数量较少，打印出来供参考
    if len(selected_chars) <= 20:
        print(f"选定的字符: {''.join(selected_chars)}")
    else:
        print(f"选定的前20个字符: {''.join(selected_chars[:20])}...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='从M5.txt创建参考字符集')
    parser.add_argument('--num_chars', type=int, default=None, 
                        help='要选择的字符数量，默认使用全部字符')
    parser.add_argument('--random_seed', type=int, default=42,
                        help='随机种子，用于随机选择字符时保持一致性')
    
    args = parser.parse_args()
    create_ref_chars(args.num_chars, args.random_seed)
