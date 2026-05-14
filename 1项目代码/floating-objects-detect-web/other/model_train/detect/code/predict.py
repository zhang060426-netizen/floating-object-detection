from tkinter import image_names
from ultralytics import YOLO

# 加载训练好的模型
model = YOLO("output/已经训练好的模型和测试结果/train/weights/best.pt")

# 图片路径
image_path = "dataset/small_dataset/train/images/0137.jpg"

# 预测图片
results = model(image_path, save=True, imgsz=640, save_dir="output_test/predict")

# 输出结果
print(results)
