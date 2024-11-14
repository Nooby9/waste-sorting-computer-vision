from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("runs/detect/train_res_832/weights/best.pt")

# Export the model to ONNX format
model.export(format="onnx")  # creates 'yolo11n.onnx'
