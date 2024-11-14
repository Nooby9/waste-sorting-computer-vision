import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

from ultralytics import YOLO

# Load the trained ONNX model
model = YOLO("runs/detect/train/weights/best.onnx")


# Perform object detection on a new image
results = model("000080.jpg")

# Save the annotated result
results[0].save("000080.png")
