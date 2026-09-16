import os
import shutil
from tqdm import tqdm
import math

# 原始目录
train_root = "/home/just/dataset/jll/selected_1000/train_3D"
test_root = "/home/just/dataset/jll/selected_1000/test_3D"

# 输出新目录
output_root = "/home/just/dataset/jll/selected_1000/output_3D"
output_train = os.path.join(output_root, "train")
output_test = os.path.join(output_root, "test")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_dir(output_train)
ensure_dir(output_test)

# 所有分类
train_classes = set(os.listdir(train_root))
test_classes = set(os.listdir(test_root))
all_classes = sorted(train_classes.union(test_classes))

for cls in tqdm(all_classes, desc="Re-splitting classes"):
    src_train_cls = os.path.join(train_root, cls)
    src_test_cls  = os.path.join(test_root, cls)

    out_train_cls = os.path.join(output_train, cls)
    out_test_cls  = os.path.join(output_test, cls)

    # 获取专利文件夹
    train_items = os.listdir(src_train_cls) if os.path.exists(src_train_cls) else []
    test_items  = os.listdir(src_test_cls)  if os.path.exists(src_test_cls)  else []

    all_items = sorted(train_items + test_items)
    total = len(all_items)

    # ============ ① 总数 < 5：全部放 test ============
    if total < 5:
        ensure_dir(out_test_cls)
        for item in all_items:
            src = os.path.join(src_train_cls, item) if item in train_items \
                else os.path.join(src_test_cls, item)
            shutil.copytree(src, os.path.join(out_test_cls, item))

        print(f"[SMALL] {cls}: 总 {total} 个 → 全部分到 test")
        continue

    # ============ ② 总数 ≥ 5：8:2 重新划分 ============
    # 先算默认 8:2
    test_num = max(5, math.floor(total * 0.2))   # 至少 5
    train_num = total - test_num

    # 防止 train=0 的极端情况
    if train_num < 0:
        train_num = 0

    # 划分
    test_set = all_items[:test_num]
    train_set = all_items[test_num:]

    # ===== 复制到新目录 =====
    if train_set:
        ensure_dir(out_train_cls)
        for item in train_set:
            src = os.path.join(src_train_cls, item) if item in train_items \
                else os.path.join(src_test_cls, item)
            shutil.copytree(src, os.path.join(out_train_cls, item))

    if test_set:
        ensure_dir(out_test_cls)
        for item in test_set:
            src = os.path.join(src_train_cls, item) if item in train_items \
                else os.path.join(src_test_cls, item)
            shutil.copytree(src, os.path.join(out_test_cls, item))

    print(f"[SPLIT] {cls}: 总 {total} 个 → train={train_num}, test={test_num}")