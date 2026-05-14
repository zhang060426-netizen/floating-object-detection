from ultralytics import YOLO

# 加载基础yolo模型
model = YOLO("weights/yolo26n.pt")

# 使用数据集训练模型
results = model.train(data="dataset/small_dataset/data.yaml", epochs=50, imgsz=640, save_dir="output/train")