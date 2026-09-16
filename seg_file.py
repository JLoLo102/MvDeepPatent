# -*-coding:utf-8-*-
import os
import shutil

def get_folder_size(path):
    """计算文件夹大小（字节）"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)
    return total


def select_top_folders_and_copy(folder1, folder2, out_root, top_k=1000):
    # 获取共同子文件夹名
    sub1 = {n for n in os.listdir(folder1) if os.path.isdir(os.path.join(folder1, n))}
    sub2 = {n for n in os.listdir(folder2) if os.path.isdir(os.path.join(folder2, n))}
    common = sorted(sub1 & sub2)
    print(f"共有 {len(common)} 个共同子文件夹")

    folder_sizes = []
    for name in common:
        size1 = get_folder_size(os.path.join(folder1, name))
        size2 = get_folder_size(os.path.join(folder2, name))
        total = size1 + size2
        folder_sizes.append((name, total))

    # 排序
    folder_sizes.sort(key=lambda x: x[1], reverse=True)
    selected = folder_sizes[:top_k]

    print(f"选出总大小最大的 {top_k} 个文件夹")

    # 创建输出目录
    out_folder1 = os.path.join(out_root, os.path.basename(folder1))
    out_folder2 = os.path.join(out_root, os.path.basename(folder2))
    os.makedirs(out_folder1, exist_ok=True)
    os.makedirs(out_folder2, exist_ok=True)

    # 复制文件夹
    for name, size in selected:
        src1 = os.path.join(folder1, name)
        src2 = os.path.join(folder2, name)
        dst1 = os.path.join(out_folder1, name)
        dst2 = os.path.join(out_folder2, name)

        print(f"📦 Copying {name} ... ({size/1024/1024:.2f} MB total)")
        if not os.path.exists(dst1):
            shutil.copytree(src1, dst1)
        if not os.path.exists(dst2):
            shutil.copytree(src2, dst2)

    # 保存列表
    list_file = os.path.join(out_root, "selected_top1000.txt")
    with open(list_file, "w") as f:
        for name, size in selected:
            f.write(f"{name}\t{size}\n")
    print(f"\n✅ 已完成复制，共 {top_k} 个文件夹，列表保存到 {list_file}")


if __name__ == "__main__":
    folder1 = "/home/just/dataset/jll/patent_3D_v2/train_3D"   # ← 修改为你的路径
    folder2 = "/home/just/dataset/jll/patent_3D_v2/test_3D"   # ← 修改为你的路径
    output_dir = "/home/just/dataset/jll/selected_1000"  # 输出目录
    select_top_folders_and_copy(folder1, folder2, output_dir, top_k=1000)