# -*-coding:utf-8-*-
from pathlib import Path

def save_subfolder_names(folder_path, output_txt="file_name_1000.txt"):
    folder = Path(folder_path)
    subfolders = [f.name for f in folder.iterdir() if f.is_dir()]

    output_path = folder / output_txt
    with open(output_path, "w", encoding="utf-8") as f:
        for name in subfolders:
            f.write(name + "\n")

    print(f"✅ 已保存 {len(subfolders)} 个子文件夹名称到：{output_path}")

# ===== 使用示例 =====
folder_path = r"/home/just/dataset/jll/selected_1000/output_3D/test"  # 替换为你的文件夹路径
save_subfolder_names(folder_path)