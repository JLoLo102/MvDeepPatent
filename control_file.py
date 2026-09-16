# # -*-coding:utf-8-*-
import os
import shutil
import random
from tqdm import tqdm

# === 用户参数 ===
root_dir = "*/selected_1000/"   # 数据集根目录，包含 train_3D/ 和 test_3D/
train_dir = os.path.join(root_dir, "train_3D")
test_dir = os.path.join(root_dir, "test_3D")

output_train = os.path.join(root_dir, "new_train_3D")
output_test = os.path.join(root_dir, "new_test_3D")
log_path = os.path.join(root_dir, "split_log.txt")

split_ratio = 0.8  # 训练集比例
min_patent_count = 2  # 至少包含 20 个专利文件夹的类别才保留

# 清空输出目录
for d in [output_train, output_test]:
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)

log_lines = []

# === Step 1: 合并 train_3D 与 test_3D 的同类数据 ===
merged_dict = {}

categories = sorted(os.listdir(train_dir))
for cls in tqdm(categories, desc="Merging train/test by class"):
    cls_train_path = os.path.join(train_dir, cls)
    cls_test_path = os.path.join(test_dir, cls)

    # 跳过不存在的类别
    if not os.path.exists(cls_train_path) or not os.path.exists(cls_test_path):
        continue

    # 收集“专利文件夹”（即每个专利对应一个文件夹）
    train_patents = [os.path.join(cls_train_path, p) for p in os.listdir(cls_train_path)
                     if os.path.isdir(os.path.join(cls_train_path, p))]
    test_patents = [os.path.join(cls_test_path, p) for p in os.listdir(cls_test_path)
                    if os.path.isdir(os.path.join(cls_test_path, p))]

    all_patents = train_patents + test_patents
    merged_dict[cls] = all_patents

# === Step 2 & 3: 筛选类别（专利文件夹数 ≥ 20） ===
filtered_classes = {cls: paths for cls, paths in merged_dict.items() if len(paths) >= min_patent_count}

log_lines.append(f"共有 {len(filtered_classes)} 个类别满足条件（≥{min_patent_count} 个专利）\n")
print(f"✅ 筛选后类别数: {len(filtered_classes)}")

# === Step 4: 重新划分 train/test ===
for cls, all_patents in tqdm(filtered_classes.items(), desc="Splitting train/test"):
    random.shuffle(all_patents)
    n_total = len(all_patents)
    n_train = int(n_total * split_ratio)

    train_patents = all_patents[:n_train]
    test_patents = all_patents[n_train:]

    cls_train_out = os.path.join(output_train, cls)
    cls_test_out = os.path.join(output_test, cls)
    os.makedirs(cls_train_out, exist_ok=True)
    os.makedirs(cls_test_out, exist_ok=True)

    # 拷贝专利文件夹
    for src_path in train_patents:
        dst_path = os.path.join(cls_train_out, os.path.basename(src_path))
        shutil.copytree(src_path, dst_path)

    for src_path in test_patents:
        dst_path = os.path.join(cls_test_out, os.path.basename(src_path))
        shutil.copytree(src_path, dst_path)

    log_lines.append(f"{cls}: 总专利 {n_total}, train={len(train_patents)}, test={len(test_patents)}")

# === Step 5: 写入日志文件 ===
with open(log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines))

print("\n✅ 数据集重新划分完成！")
print(f"📄 日志已保存至: {log_path}")



