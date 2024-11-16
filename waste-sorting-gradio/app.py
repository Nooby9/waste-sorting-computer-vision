import gradio as gr
import numpy as np


# Placeholder function
def object_detection(image):
    return "plastic"


def evaluate_choice(image, chosen_bin, score):
    label = object_detection(image)

    # Define correct bins for each label
    correct_bins = {
        "organic": "Organic Bin",
        "plastic": "Recycle Bin",
        "paper": "Recycle Bin",
        # Add more mappings as necessary
    }

    if label in correct_bins:
        if chosen_bin == correct_bins[label]:
            score += 1
            result = f"Correct! The item is {label}. Your score: {score}"
        else:
            score -= 1
            result = f"Wrong! The item is {label}. Your score: {score}"
    else:
        result = f"Unknown item: {label}. Your score: {score}"

    return result, score


def capture_pic(input_stream):
    return input_stream, input_stream


with gr.Blocks() as demo:
    # score
    score_state = gr.State(value=0)
    # img captured by live cam
    # use this value for frame captured by live cam
    latest_image_state = gr.State(value=np.zeros((100, 100, 3)))

    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            img_input = gr.Image(type="numpy", label="Upload or Take a Picture")
            classify_button = gr.Button("Classify")

        with gr.Column(scale=1, min_width=300):
            input_stream = gr.Image(sources=["webcam"], type="numpy", label="Webcam Capture")
            img_captured = gr.Image(label="Captured Image, for debug purpose. Remove when dev complete")

            # Update latest image state continuously
            dep = input_stream.stream(fn=capture_pic, inputs=input_stream, outputs=[img_captured, latest_image_state],
                                      every=0.1, concurrency_limit=30)

        with gr.Column(scale=1, min_width=300):
            bins_choice = gr.Radio(choices=["Organic Bin", "Recycle Bin", "Garbage Bin"],
                                   label="Select the correct bin")
            submit_image_upload_button = gr.Button("Play game with uploaded image!")
            submit_live_cam_button = gr.Button("Play game with live cam!")

    with gr.Row():
        output_text = gr.Textbox(label="Result", elem_id="result-output")

    # live cam
    submit_live_cam_button.click(fn=evaluate_choice, inputs=[latest_image_state, bins_choice, score_state],
                                 outputs=[output_text, score_state])
    submit_image_upload_button.click(fn=evaluate_choice, inputs=[img_input, bins_choice, score_state],
                                     outputs=[output_text, score_state])

    demo.css = """
    #result-output {
        font-size: 18px;
        text-align: center;
        color: #333;
    }
    """

demo.launch(share=True)
