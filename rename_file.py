import os
import shutil

def flatten_and_rename(base_dir):
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if os.path.isdir(folder_path) and folder_name.endswith(" "):
            print(f"Processing: {folder_path}")

            # 处理二级目录
            for subfolder_name in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder_name)
                if os.path.isdir(subfolder_path):
                    for item_name in os.listdir(subfolder_path):
                        item_path = os.path.join(subfolder_path, item_name)
                        if os.path.isdir(item_path):
                            dest_path = os.path.join(folder_path, item_name)
                            if os.path.exists(dest_path):
                                print(f"⚠️ 目标文件夹已存在，跳过或改名：{dest_path}")
                                dest_path = dest_path + "_dup"
                            print(f"Moving {item_path} -> {dest_path}")
                            shutil.move(item_path, dest_path)
                    print(f"Removing subfolder: {subfolder_path}")
                    shutil.rmtree(subfolder_path)

            # 重命名主目录
            new_folder_name = folder_name.rstrip()
            new_folder_path = os.path.join(base_dir, new_folder_name)

            if os.path.exists(new_folder_path):
                print(f"⚠️ 目标路径已存在，合并并删除旧目录: {new_folder_path}")
                # 将旧目录中的所有内容移动到新目录下
                for item_name in os.listdir(folder_path):
                    src_path = os.path.join(folder_path, item_name)
                    dst_path = os.path.join(new_folder_path, item_name)
                    if os.path.exists(dst_path):
                        dst_path = dst_path + "_dup"
                    shutil.move(src_path, dst_path)
                shutil.rmtree(folder_path)
            else:
                print(f"Renaming {folder_path} -> {new_folder_path}")
                os.rename(folder_path, new_folder_path)

if __name__ == "__main__":
    base_directory = "*/train_3D"
    flatten_and_rename(base_directory)
