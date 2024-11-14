import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

from ultralytics import YOLO

# Load the trained ONNX model
model = YOLO("runs/detect/train_res_832/weights/best.pt")


# Perform object detection on a new image
results = model("sample_run_images/organic_waste.jpg")

# Save the annotated result
results[0].save("sample_run_images/organic_waste_annotated.png")
