import os
import unicodedata

# 检查生成的图像文件
gen_dir = 'results/infer_result/genimgs/M5/'
if os.path.exists(gen_dir):
    print("生成图像目录中的文件:")
    for filename in os.listdir(gen_dir):
        # 尝试将文件名解析为Unicode字符
        try:
            unicode_name = filename.encode('latin1').decode('utf-8')
            # 获取字符的Unicode编码点
            if unicode_name.endswith('.png'):
                char = unicode_name[:-4]  # 移除.png后缀
                unicode_points = []
                for c in char:
                    unicode_points.append(f"U+{ord(c):04X}")
                print(f"文件: {filename}")
                print(f"实际字符: {char}")
                print(f"Unicode编码点: {', '.join(unicode_points)}")
                print(f"字符名称: {unicodedata.name(char, '未知')}")
                print("---")
        except Exception as e:
            print(f"无法解析文件名 {filename}: {e}")

# 检查参考图像文件
gt_dir = 'results/infer_result/gtimgs/M5/'
if os.path.exists(gt_dir):
    print("\n参考图像目录中的文件:")
    for filename in os.listdir(gt_dir):
        try:
            unicode_name = filename.encode('latin1').decode('utf-8')
            if unicode_name.endswith('.png'):
                char = unicode_name[:-4]
                unicode_points = []
                for c in char:
                    unicode_points.append(f"U+{ord(c):04X}")
                print(f"文件: {filename}")
                print(f"实际字符: {char}")
                print(f"Unicode编码点: {', '.join(unicode_points)}")
                print(f"字符名称: {unicodedata.name(char, '未知')}")
                print("---")
        except Exception as e:
            print(f"无法解析文件名 {filename}: {e}")
