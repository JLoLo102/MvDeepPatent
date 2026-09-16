import json
from collections import Counter
import torch

from tools.ImgDataset import MultiviewImgDataset

train_dataset = MultiviewImgDataset("*/selected_1000/train_3D", scale_aug=False, rot_aug=False, num_models=1000, num_views=5)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=16)
labels = []
class_labels=[]
for i in range(len(train_loader.dataset)):
    class_id = train_loader.dataset[i][0]  # 取第一个返回值，即 class_id
    labels.append(class_id)

label_count = Counter(labels)
for k in sorted(label_count.keys()):
    # print(f"Class {k}: {label_count[k]} samples")
    class_labels.append(label_count[k])

with open("stats.json", "w") as f:
    json.dump({
        "class_counts": class_labels
    }, f, indent=2)

print("class_counts =", class_labels)
print("统计完成，已保存到 stats.json")
