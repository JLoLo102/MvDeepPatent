import os
import shutil
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ========== 🔧 配置路径 ==========
txt_folder = '*/train_3D'       # 包含 *_related.txt 的目录
source_root = '*/trainData_search'         # 所有源文件夹所在位置
target_root = '*/train_3D'          # 输出根目录
log_file = 'copy_failures_merge.log'                  # 失败日志文件路径

# ========== 📝 写入失败日志 ==========
def log_failure(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} {msg}\n")

# ========== 📦 合并复制目录 ==========
def merge_folders(src, dst):
    try:
        if not os.path.exists(dst):
            shutil.copytree(src, dst)
            return f"✅ 创建并复制: {src} → {dst}"
        else:
            for item in os.listdir(src):
                s_item = os.path.join(src, item)
                d_item = os.path.join(dst, item)

                if os.path.isdir(s_item):
                    merge_folders(s_item, d_item)
                else:
                    if not os.path.exists(d_item):
                        shutil.copy2(s_item, d_item)
            return f"✅ 合并完成: {src} → {dst}"
    except Exception as e:
        msg = f"❌ 合并失败: {src} → {dst}, 错误: {e}"
        log_failure(msg)
        return msg

# ========== 🚀 主程序 ==========
def main():
    os.makedirs(target_root, exist_ok=True)
    if os.path.exists(log_file):
        os.remove(log_file)  # 清空旧日志

    for filename in os.listdir(txt_folder):
        if not filename.endswith('_related.txt'):
            continue

        # 提取类别名称
        category = filename.replace('_related.txt', '')
        category_dir = os.path.join(target_root, category)
        os.makedirs(category_dir, exist_ok=True)

        txt_path = os.path.join(txt_folder, filename)

        with open(txt_path, 'r', encoding='utf-8') as f:
            folder_names = [line.strip() for line in f if line.strip()]

        print(f"\n📂 处理类别：{category}，共 {len(folder_names)} 个源文件夹")

        copy_tasks = []

        for folder in folder_names:
            src_folder = os.path.join(source_root, folder)

            # ✅ 跳过不存在的源文件夹
            if not os.path.isdir(src_folder):
                log_failure(f"❌ 源文件夹不存在，跳过: {src_folder}")
                continue

            for item in os.listdir(src_folder):
                item_path = os.path.join(src_folder, item)
                if os.path.isdir(item_path):
                    dst_path = os.path.join(category_dir, item)
                    copy_tasks.append((item_path, dst_path))

        print(f"⏳ 正在合并复制 {len(copy_tasks)} 个子文件夹到 {category}/")

        # 多线程合并子文件夹
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(merge_folders, src, dst) for src, dst in copy_tasks]
            for f in tqdm(as_completed(futures), total=len(futures), desc=f"复制 {category}"):
                result = f.result()
                if result.startswith("❌"):
                    print(result)

    print(f"\n✅ 所有分类处理完成。失败日志已记录在：{log_file}")

# ========== 🏁 执行入口 ==========
if __name__ == '__main__':
    main()
