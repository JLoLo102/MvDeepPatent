import os

# 设置要搜索的根目录路径
root_dir = "/home/wangfei/dataset/jll/testData/out_test"
input_file = "common_folders.txt"

folder_names = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            folder_names.append(parts[0])  # 只取第一个字段作为名称

# 设置关键词
for folder in folder_names:

    keyword = folder

    # 输出文件
    output_file = "related_folder/test/"+keyword+"_related.txt"

    # 收集所有包含关键词的文件夹名称
    matched_folders = []

    for dirpath, dirnames, _ in os.walk(root_dir):
        for dirname in dirnames:
            if keyword.lower() in dirname.lower():  # 忽略大小写匹配
                matched_folders.append(dirname)

    # 写入文件，只写文件夹名
    with open(output_file, "w", encoding="utf-8") as f:
        for folder_name in matched_folders:
            f.write(folder_name + "\n")

    print(f"✅ 完成，共找到 {len(matched_folders)} 个包含 '{keyword}' 的文件夹名称，已写入：{output_file}")

