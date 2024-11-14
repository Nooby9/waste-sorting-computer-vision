import gradio as gr


# Assuming `object_detection` is your function that takes an image and returns a label
def object_detection(image):
    # Placeholder for your object detection logic
    return "plastic"  # Example return value


# Scoring logic
score = 0


def evaluate_choice(image, chosen_bin):
    global score
    label = object_detection(image)

    # Define correct bins for each label
    correct_bins = {
        "organic": "Organic Garbage Bin",
        "plastic": "Recycle Garbage Bin",
        "paper": "Recycle Garbage Bin",
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

    return result


with gr.Blocks() as demo:
    global score
    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            img_input = gr.Image(type="numpy", label="Upload or Take a Picture")
            classify_button = gr.Button("Classify")

        with gr.Column(scale=1, min_width=300):
            bins_choice = gr.Radio(choices=["Organic Garbage Bin", "Recycle Garbage Bin"],
                                   label="Select the correct bin")
            submit_button = gr.Button("Submit Choice")

    with gr.Row():
        output_text = gr.Textbox(label="Result", elem_id="result-output")

    classify_button.click(fn=object_detection, inputs=img_input, outputs=output_text)
    submit_button.click(fn=evaluate_choice, inputs=[img_input, bins_choice], outputs=output_text)

    demo.css = """
    #result-output {
        font-size: 18px;
        text-align: center;
        color: #333;
    }
    """

demo.launch(share=True)