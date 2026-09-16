def load_folder_counts(file_path):
    """加载txt文件为字典：folder_name -> count"""
    data = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                folder, count = parts
                data[folder] = int(count)
    return data

# 文件路径
train_file = "top_2000_folders_train.txt"
test_file = "top_2000_folders_test.txt"
output_file = "common_folders.txt"

# 读取两个文件的内容
train_data = load_folder_counts(train_file)
test_data = load_folder_counts(test_file)

# 找到两个文件都有的folder
common_folders = set(train_data.keys()) & set(test_data.keys())

# 写入输出文件
with open(output_file, "w", encoding="utf-8") as out:
    for folder in sorted(common_folders):
        train_count = train_data[folder]
        test_count = test_data[folder]
        out.write(f"{folder} {train_count} {test_count}\n")

print(f"✅ 完成，共找到 {len(common_folders)} 个公共文件夹，已写入：{output_file}")