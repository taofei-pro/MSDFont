from fontTools import ttLib

# 打开字体文件
font = ttLib.TTFont('FontData/chn/ttfs/infer_unseen_font/M5.ttf')

# 获取字符映射
cmap = font.getBestCmap()

# 提取有效字符（排除控制字符和特殊字符）
chars = [chr(c) for c in cmap.keys() if c > 0x20 and c < 0x10000]

# 将字符写入文件
with open('FontData/chn/ttfs/infer_unseen_font/M5.txt', 'w', encoding='utf-8') as f:
    f.write(''.join(chars))

print(f"已成功提取 {len(chars)} 个字符到 M5.txt 文件中")
