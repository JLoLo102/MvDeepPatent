import os
import shutil
from tqdm import tqdm

# 源文件夹路径
for i in range(0,1):
    source_folder = '/home/wangfei/dataset/jll/PatFigCLS/uspc/val/'+f"shard-{i:06d}"
    # 目标文件夹路径（你想要存放整理后文件的地方）
    target_folder = '/home/wangfei/dataset/jll/patentUspcNet/patent_object_val'

    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 筛选所有 .label.txt 文件
    files = [f for f in os.listdir(source_folder) if f.endswith('.label.txt')]

    for file in tqdm(files, desc="正在整理文件"):
        # 提取前缀，如 F0000036402
        prefix = file.replace('.label.txt', '')
        txt_path = os.path.join(source_folder, file)
        png_filename = prefix + '.image.png'
        png_path = os.path.join(source_folder, png_filename)

        # 读取 label 内容
        with open(txt_path, 'r', encoding='utf-8') as f:
            label = f.read().strip()

        # 在目标文件夹中创建分类文件夹
        label_folder = os.path.join(target_folder, label)
        os.makedirs(label_folder, exist_ok=True)

        # 移动 PNG 文件
        if os.path.exists(png_path):
            shutil.move(png_path, os.path.join(label_folder, png_filename))
        else:
            print(f"⚠️ 未找到图像：{png_filename}")