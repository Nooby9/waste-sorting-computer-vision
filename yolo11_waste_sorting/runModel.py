import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

from ultralytics import YOLO

# Load the trained ONNX model
model = YOLO("runs/detect/train_res_640/weights/best.onnx")


# Perform object detection on a new image
results = model("sample_run_images/plastic_bottles.jpg", imgsz=640)

# Save the annotated result
results[0].save("sample_run_images/plastic_bottles_annotated.png")
