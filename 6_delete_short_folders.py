import os
import shutil

def delete_small_folders(root_dir, min_file_count=5):
    # 遍历一级分类目录
    for class_dir in os.listdir(root_dir):
        class_path = os.path.join(root_dir, class_dir)
        if not os.path.isdir(class_path):
            continue

        # 遍历每个分类目录下的子文件夹
        for sub_dir in os.listdir(class_path):
            sub_path = os.path.join(class_path, sub_dir)
            if not os.path.isdir(sub_path):
                continue

            # 统计子文件夹内的文件数量（忽略子目录）
            file_count = sum([1 for f in os.listdir(sub_path) if os.path.isfile(os.path.join(sub_path, f))])

            # 如果文件数小于设定值，则删除整个子文件夹
            if file_count < min_file_count:
                print(f"删除文件夹：{sub_path}（文件数：{file_count}）")
                shutil.rmtree(sub_path)

# 示例使用：替换为你的实际路径
root_folder = '*/test_3D'  # 修改为你的主目录路径
delete_small_folders(root_folder)
