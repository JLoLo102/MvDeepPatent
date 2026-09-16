import os
import shutil
import logging
from pathlib import Path
from tqdm import tqdm

# ========== 配置 ==========
MIN_IMAGES = 5
DELETE_SOURCE_SUBFOLDERS = False  # 如果 True，会删除源目录中图片数 < MIN_IMAGES 的二级子文件夹（危险，慎用）
LOG_FILE = "filter_copy.log"

# ========== 日志 ==========
logging.basicConfig(
    filename=LOG_FILE,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)

# ========== 工具函数 ==========
def count_images(folder: Path, exts=None) -> int:
    """递归统计文件夹内图片数量（支持常见扩展名）"""
    if exts is None:
        exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
    return sum(1 for f in folder.rglob('*') if f.is_file() and f.suffix.lower() in exts)

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def safe_copy_tree(src: Path, dst: Path):
    """只在目标不存在时直接拷贝；若存在则先删除再拷贝（确保一致）"""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

# ========== 主逻辑 ==========
def filter_and_copy(folder1: str, folder2: str, train_dst: str, test_dst: str, min_images=MIN_IMAGES,
                    delete_source_subfolders=DELETE_SOURCE_SUBFOLDERS):
    folder1 = Path(folder1)
    folder2 = Path(folder2)
    train_dst = Path(train_dst)
    test_dst = Path(test_dst)

    # 创建目标根目录
    ensure_dir(train_dst)
    ensure_dir(test_dst)

    # 读取直接子文件夹集合
    subs1 = {p.name: p for p in folder1.iterdir() if p.is_dir()}
    subs2 = {p.name: p for p in folder2.iterdir() if p.is_dir()}

    common_names = sorted(set(subs1.keys()) & set(subs2.keys()))
    logging.info(f"共找到 {len(common_names)} 个同名的直接子文件夹：{common_names}")

    for name in tqdm(common_names, desc="处理同名直接子文件夹"):
        p1 = subs1[name]
        p2 = subs2[name]

        # 列出二级子文件夹
        second1 = [d for d in p1.iterdir() if d.is_dir()]
        second2 = [d for d in p2.iterdir() if d.is_dir()]

        # 计算每个二级子文件夹的图片数并筛选
        valid_second1 = []
        invalid_second1 = []
        for d in second1:
            cnt = count_images(d)
            if cnt >= min_images:
                valid_second1.append((d, cnt))
            else:
                invalid_second1.append((d, cnt))

        valid_second2 = []
        invalid_second2 = []
        for d in second2:
            cnt = count_images(d)
            if cnt >= min_images:
                valid_second2.append((d, cnt))
            else:
                invalid_second2.append((d, cnt))

        # 如果启用删除源中不合格二级文件夹（谨慎）
        if delete_source_subfolders:
            for d, cnt in invalid_second1:
                try:
                    shutil.rmtree(d)
                    logging.info(f"已从源 folder1 删除不合格二级子文件夹：{d}（{cnt} 张）")
                except Exception as e:
                    logging.warning(f"删除失败（folder1）: {d}: {e}")
            for d, cnt in invalid_second2:
                try:
                    shutil.rmtree(d)
                    logging.info(f"已从源 folder2 删除不合格二级子文件夹：{d}（{cnt} 张）")
                except Exception as e:
                    logging.warning(f"删除失败（folder2）: {d}: {e}")

            # 重新列 valid 列表（因为删除后可能变化）
            valid_second1 = [(d, count_images(d)) for d, _ in valid_second1]
            valid_second2 = [(d, count_images(d)) for d, _ in valid_second2]

        # 如果任意一侧没有剩余合格二级文件夹，则跳过该直接子文件夹（两侧都不保存）
        if not valid_second1 or not valid_second2:
            logging.info(f"跳过：{name} —— folder1 剩余合格二级文件夹: {len(valid_second1)}，folder2 剩余合格二级文件夹: {len(valid_second2)}")
            # 记录哪些被过滤掉
            if invalid_second1:
                logging.info(f"  folder1 被过滤的二级子文件夹（<{min_images}）：{[(str(d),c) for d,c in invalid_second1]}")
            if invalid_second2:
                logging.info(f"  folder2 被过滤的二级子文件夹（<{min_images}）：{[(str(d),c) for d,c in invalid_second2]}")
            continue

        # 两侧都有 >=1 个合格二级子文件夹，开始在目标路径中创建该直接子文件夹，并复制合格的二级子文件夹
        dst_train_parent = train_dst / name
        dst_test_parent = test_dst / name
        ensure_dir(dst_train_parent)
        ensure_dir(dst_test_parent)

        # 复制 folder1 中的合格二级子文件夹到 train/name/<sub>
        for d, cnt in valid_second1:
            dst = dst_train_parent / d.name
            logging.info(f"copy folder1/{name}/{d.name} -> {dst} (images={cnt})")
            safe_copy_tree(d, dst)

        # 复制 folder2 中的合格二级子文件夹到 test/name/<sub>
        for d, cnt in valid_second2:
            dst = dst_test_parent / d.name
            logging.info(f"copy folder2/{name}/{d.name} -> {dst} (images={cnt})")
            safe_copy_tree(d, dst)

        logging.info(f"✅ 保留并已复制：{name}，folder1保留 {len(valid_second1)} 个二级子文件夹，folder2保留 {len(valid_second2)} 个二级子文件夹")

    logging.info("处理完成。详细日志请查看：" + str(Path(LOG_FILE).resolve()))

if __name__ == "__main__":
# ===== 示例使用 =====
    folder1 = r"/home/just/dataset/jll/trainData_search"
    folder2 = r"/home/just/dataset/jll/testData_search"
    train_dst = r"/home/just/dataset/jll/train"
    test_dst = r"/home/just/dataset/jll/test"

    filter_and_copy(folder1, folder2, train_dst, test_dst, min_images=5,delete_source_subfolders=False)
# -*-coding:utf-8-*-
