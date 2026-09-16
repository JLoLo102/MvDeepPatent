with open('common_folders.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 按第二列（第一个数值）倒序排序
sorted_lines = sorted(
    lines,
    key=lambda line: int(line.strip().split()[1]),
    reverse=True
)

# 将排序结果写入新文件
with open('sorted_common_folders.txt', 'w', encoding='utf-8') as f:
    f.writelines(sorted_lines)