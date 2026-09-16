import os
import json
import shutil
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from collections import defaultdict

# === 配置部分 ===
json_file = '/home/just/dataset/wyh/testData/test.json'  # JSON 文件名
image_dir = '/home/just/dataset/wyh/testData/Segmentednew'  # 原始图片目录
output_dir = '/home/just/dataset/jll/testData_search'  # 输出分类后的根目录
log_file = 'copy_errors.log'  # 错误日志文件路径

num_workers = cpu_count()  # 自动使用最大核心数
compress = False  # 不压缩，保留原始 PNG

# === 创建输出目录 ===
os.makedirs(output_dir, exist_ok=True)

# === 读取 JSON 数据 ===
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# === 错误日志和统计容器 ===
error_log = []
class_counts = defaultdict(int)

# === 拷贝函数（单个数据项） ===
def process_entry(entry):
    try:
        object_class = entry.get('object').strip().lower()
        patent_id = entry['patentID']
        image_file = entry['subfigure_file']

        src_path = os.path.join(image_dir, image_file)
        target_dir = os.path.join(output_dir, object_class, patent_id)
        os.makedirs(target_dir, exist_ok=True)

        target_path = os.path.join(target_dir, image_file)

        if not os.path.exists(src_path):
            return (object_class, False, f'File not found: {src_path}')

        # 直接复制 PNG 文件
        shutil.copy2(src_path, target_path)
        return (object_class, True, None)

    except Exception as e:
        return (object_class, False, str(e))

# === 多进程执行 ===
def main():
    print(f"开始处理 {len(data)} 条记录，使用 {num_workers} 核心...")

    with Pool(num_workers) as pool:
        results = list(tqdm(pool.imap(process_entry, data), total=len(data), desc="处理进度"))

    # 分类处理结果
    for object_class, success, err in results:
        if success:
            class_counts[object_class] += 1
        else:
            error_log.append(f"[{object_class}] {err}")

    # 输出统计信息
    print("\n✅ 分类图像数量：")
    for cls, count in sorted(class_counts.items(), key=lambda x: -x[1]):
        print(f"{cls}: {count} 张")

    # 写入错误日志
    if error_log:
        with open(log_file, 'w', encoding='utf-8') as logf:
            for err in error_log:
                logf.write(err + '\n')
        print(f"\n⚠️ 复制失败记录已写入：{log_file}")
    else:
        print("\n🎉 所有图像成功处理！")

if __name__ == '__main__':
    main()