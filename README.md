---
title: AWSA
emoji: 🐨
colorFrom: gray
colorTo: pink
sdk: gradio
sdk_version: 5.6.0
app_file: app.py
pinned: false
short_description: Automated Waste Sorting Assistant
---
## Waste Sorting Gradio Application
This project utilizes a Gradio interface to streamline waste classification using a YOLO object detection model and LLM based feedback. The interface gamifies the learning experience by identifying waste items from an uploaded image, allowing users to classify them into recyclable and non-recyclable categories, with immediate validation and engaging educational feedback.

## Requirements
### Environment:
- Python 3.7+
- OpenAI Python SDK version 0.28.
### Dependencies:
- gradio
- numpy
- ultralytics
- openai
- Other standard Python libraries.
### OpenAI API Key:
- Users must provide their own OpenAI API key by setting it in the environment variable OPENAI_API_KEY.
### YOLO Model:
- Ensure the YOLO model weights file is located at the specified path: yolo11_waste_sorting/runs/detect/train_res_640/weights/best.onnx.

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
