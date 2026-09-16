import os
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import traceback

# 设置路径和输出文件
root_dir = "/home/wangfei/dataset/jll/testData/out_test"
output_file = "top_2000_folders_test.txt"
error_log_file = "error_log.txt"


# 获取一级子文件夹路径
all_folders = [os.path.join(root_dir, d) for d in os.listdir(root_dir)
               if os.path.isdir(os.path.join(root_dir, d))]

def count_subfolders(folder_path):
    """统计当前文件夹下的直接子文件夹数量"""
    try:
        subfolders = [name for name in os.listdir(folder_path)
                      if os.path.isdir(os.path.join(folder_path, name))]
        folder_name = os.path.basename(folder_path)
        return (folder_name, len(subfolders))
    except Exception:
        with open(error_log_file, "a", encoding="utf-8") as log:
            log.write(f"出错文件夹：{folder_path}\n错误信息：{traceback.format_exc()}\n")
        return None

if __name__ == "__main__":
    print(f"开始统计 {len(all_folders)} 个文件夹的直接子文件夹数量...")

    results = []
    with Pool(cpu_count()) as pool:
        for result in tqdm(pool.imap_unordered(count_subfolders, all_folders), total=len(all_folders)):
            if result:
                results.append(result)

    # 取子文件夹最多的前2000个
    top_2000 = sorted(results, key=lambda x: x[1], reverse=True)[:2000]

    # 写入结果
    with open(output_file, "w", encoding="utf-8") as f:
        for folder_name, count in top_2000:
            f.write(f"{folder_name} {count}\n")

    print(f"✅ 完成！写入 {len(top_2000)} 项到 {output_file}")
    print(f"❗ 如有错误，查看日志：{error_log_file}")