import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

from ultralytics import YOLO

# Load the trained ONNX model
model = YOLO("runs/detect/train5/weights/best.onnx")


# Perform object detection on a new image
results = model("waste2.png")

# Save the annotated result
results[0].save("waste2_annotated.png")
