from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")

# Train the model
train_results = model.train(
    data="./sampled_dataset/data.yaml",  # path to dataset YAML
    epochs=100,  # number of training epochs
    imgsz=832,  # training image size
    batch=4,
    device="0",  # device to run on, i.e. device=0 or device=0,1,2,3 or device=cpu
)

# Evaluate model performance on the validation set
metrics = model.val(iou=0.5)

# Export the model to ONNX/TensorRT format
path = model.export(format="ONNX")  # return path to exported model
print(path)