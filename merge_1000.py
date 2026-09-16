import os
import shutil
import random
from tqdm import tqdm

# ======== 配置区（修改这几个路径） ========
root_dir = "/home/just/dataset/jll/selected_1000"   # 根目录，包含 train/ 和 test/
train_dir = os.path.join(root_dir, "train_3D")
test_dir = os.path.join(root_dir, "test_3D")
output_dir = os.path.join(root_dir, "merged_preserve")  # 输出目录

# 划分比例（class 级别）
split_ratio = {'base': 0.8, 'val': 0.1, 'novel': 0.1}

# ========== 辅助函数 ==========
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def safe_copy_with_suffix(src_file, dst_file):
    """
    复制 src_file 到 dst_file，若 dst_file 已存在：
      - 若大小相同，则认为相同文件，跳过复制（返回 False 表示未复制）
      - 否则在文件名后加 _dup1/_dup2 ... 直到没有冲突
    返回复制是否发生（True/False）以及最终目标路径
    """
    if not os.path.exists(dst_file):
        shutil.copy2(src_file, dst_file)
        return True, dst_file

    # 如果存在且大小相同，跳过
    try:
        if os.path.getsize(src_file) == os.path.getsize(dst_file):
            return False, dst_file
    except OSError:
        pass

    base, ext = os.path.splitext(dst_file)
    idx = 1
    new_dst = f"{base}_dup{idx}{ext}"
    while os.path.exists(new_dst):
        # 如果存在并且大小相同，认为相同，跳过
        try:
            if os.path.getsize(src_file) == os.path.getsize(new_dst):
                return False, new_dst
        except OSError:
            pass
        idx += 1
        new_dst = f"{base}_dup{idx}{ext}"

    shutil.copy2(src_file, new_dst)
    return True, new_dst

# ========== 主逻辑 ==========
def merge_and_split_preserve_subdirs(train_dir, test_dir, output_dir, split_ratio, seed=42):
    random.seed(seed)
    ensure_dir(output_dir)

    train_classes = set([d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))])
    test_classes = set([d for d in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, d))])
    common_classes = sorted(list(train_classes & test_classes))
    if not common_classes:
        raise ValueError("找不到 train 和 test 中共同的 class 文件夹，请检查路径。")

    print(f"检测到共同 class 数量: {len(common_classes)}")

    # 创建 split 目录
    for s in split_ratio.keys():
        ensure_dir(os.path.join(output_dir, s))

    # 随机划分 class
    random.shuffle(common_classes)
    n_total = len(common_classes)
    n_base = int(n_total * split_ratio['base'])
    n_val = int(n_total * split_ratio['val'])
    n_novel = n_total - n_base - n_val

    base_classes = common_classes[:n_base]
    val_classes = common_classes[n_base:n_base + n_val]
    novel_classes = common_classes[n_base + n_val:]

    split_dict = {'base': base_classes, 'val': val_classes, 'novel': novel_classes}

    # 处理每个 split 的每个 class：从 train/class 和 test/class 递归复制结构与文件
    for split_name, class_list in split_dict.items():
        print(f"开始处理 split={split_name}，包含 {len(class_list)} 个 class")
        for cls_name in tqdm(class_list, desc=f"Processing {split_name}"):
            src_train_cls = os.path.join(train_dir, cls_name)
            src_test_cls = os.path.join(test_dir, cls_name)
            dst_class_dir = os.path.join(output_dir, split_name, cls_name)
            ensure_dir(dst_class_dir)

            # 遍历两个来源目录（保留子目录结构）
            for src_root in (src_train_cls, src_test_cls):
                # 如果源不存在（理论上不应发生，因为我们取了交集），则跳过
                if not os.path.exists(src_root):
                    continue

                for root, dirs, files in os.walk(src_root):
                    # 相对路径（相对于 class 目录）
                    rel_path = os.path.relpath(root, src_root)
                    if rel_path == ".":
                        rel_path = ""  # class 根目录
                    dst_subdir = os.path.join(dst_class_dir, rel_path)
                    ensure_dir(dst_subdir)

                    for fname in files:
                        src_file = os.path.join(root, fname)
                        dst_file = os.path.join(dst_subdir, fname)
                        try:
                            copied, final_dst = safe_copy_with_suffix(src_file, dst_file)
                        except Exception as e:
                            print(f"复制文件失败: {src_file} -> {dst_file} ; 错误: {e}")

    print("✅ 合并并划分完成。")
    print(f"Base: {len(base_classes)} 类, Val: {len(val_classes)} 类, Novel: {len(novel_classes)} 类")
    print(f"输出目录: {output_dir}")

if __name__ == "__main__":
    merge_and_split_preserve_subdirs(train_dir, test_dir, output_dir, split_ratio)