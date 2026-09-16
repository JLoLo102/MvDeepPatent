# -*-coding:utf-8-*-
import os

# ===============================
# 配置区（你只需要改这里）
# ===============================

DATA_ROOT = "*/patent_3D_v2"

TRAIN_DIR = os.path.join(DATA_ROOT, "new_train_3D")
TEST_DIR  = os.path.join(DATA_ROOT, "new_test_3D")

CLASS_FILES = {
    # "527": "file_name.txt",
    # "1000": "file_name_1000.txt",
    "4449": "file_name_4449.txt",
}

# ===============================
# 工具函数
# ===============================

def load_classes(file_path):
    with open(file_path, "r") as f:
        return set(line.strip() for line in f if line.strip())

def count_patents(split_dir, class_ids):
    count = 0
    for cls in class_ids:
        cls_dir = os.path.join(split_dir, cls)
        if not os.path.isdir(cls_dir):
            continue

        for item in os.listdir(cls_dir):
            item_path = os.path.join(cls_dir, item)
            if os.path.isdir(item_path):
                count += 1   # 一个目录 = 一个专利
    return count

# ===============================
# 主流程
# ===============================

if __name__ == "__main__":
    print(f"{'Classes':<10} {'Train Patents':<15} {'Test Patents':<15}")
    print("-" * 45)

    for setting, class_file in CLASS_FILES.items():
        class_ids = load_classes(class_file)

        train_cnt = count_patents(TRAIN_DIR, class_ids)
        test_cnt  = count_patents(TEST_DIR, class_ids)

        print(f"{setting:<10} {train_cnt:<15} {test_cnt:<15}")
