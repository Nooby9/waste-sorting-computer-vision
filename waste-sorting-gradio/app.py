import gradio as gr
import numpy as np
from ultralytics import YOLO
import openai
import os

# Load the YOLO model
# model = YOLO("yolo11_waste_sorting\\runs\\detect\\train_res_640\\weights\\best.onnx")
model = YOLO("best.onnx")

# Waste categories
waste_categories = {
    "recyclable": [
        "Aluminium_foil",
        "Battery",
        "Aluminium_blister_pack",
        "Carded_blister_pack",
        "Other_plastic_bottle",
        "Clear_plastic_bottle",
        "Glass_bottle",
        "Plastic_bottle_cap",
        "Metal_bottle_cap",
        "Food_Can",
        "Aerosol",
        "Drink_can",
        "Toilet_tube",
        "Other_carton",
        "Egg_carton",
        "Drink_carton",
        "Corrugated_carton",
        "Meal_carton",
        "Pizza_box",
        "Paper_cup",
        "Glass_cup",
        "Glass_jar",
        "Plastic_lid",
        "Metal_lid",
        "Normal_paper",
        "Paper_bag",
        "Plastic_film",
        "Magazine_paper",
        "Wrapping_paper",
        "Scrap_metal",
    ],
    "non_recyclable": [
        "Broken_glass",
        "Food_waste",
        "Tissues",
        "Plastified_paper_bag",
        "Six_pack_rings",
        "Garbage_bag",
        "Other_plastic_wrapper",
        "Single-use_carrier_bag",
        "Polypropylene_bag",
        "Crisp_packet",
        "Spread_tub",
        "Tupperware",
        "Disposable_food_container",
        "Foam_food_container",
        "Other_plastic_container",
        "Plastic_glooves",
        "Plastic_utensils",
        "Pop_tab",
        "Rope_&_strings",
        "Shoe",
        "Squeezable_tube",
        "Plastic_straw",
        "Paper_straw",
        "Styrofoam_piece",
        "Unlabeled_litter",
        "Cigarette",
    ],
}


# GPT explanation function
def generate_gpt_explanation(item, user_choice, correct_choice):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = [
        {
            "role": "system",
            "content": "You are an expert in explaining waste sorting and environmental impact.",
        },
        {
            "role": "user",
            "content": (
                f"The waste item '{item}' is categorized as '{user_choice} by the user, which is wrong.'.\n\n"
                f"The correct category is '{correct_choice}'\n\n"
                "Explain why this categorization is incorrect, in strictly one sentence, "
                "focusing on its environmental impact or recycling properties."
            ),
        },
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=80,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"


# Object detection function
def object_detection(image):
    results = model(image, imgsz=640)
    items = []
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        label = results[0].names[class_id]
        items.append(label)
    return list(set(items))  # Remove duplicates


# Gradio interface
with gr.Blocks(
        css="""
.upload_img_element {
    max-width: 100%;
    max-height: 50%;
    height: auto;
}
.center-container {
    display: flex;
    justify-content: center;
    align-items: center;
}
"""
) as demo:
    gr.Markdown(
        """
        # Automated Waste Sorting Application
        Upload an image to detect and classify waste items into recyclable or non-recyclable categories. 
        Help promote environmental sustainability through proper waste sorting!
        You might see error because missing OPENAI api keys. Unfortunately you need to use your own key.
        """
    )

    detected_items_state = gr.State([])  # Keep track of detected items

    with gr.Row(elem_classes=["center-container"]):
        img_input = gr.Image(
            type="numpy", label="Upload an Image", elem_classes=["upload_img_element"]
        )


    @gr.render(inputs=img_input)
    def render_detected_items(image):
        if image is None:
            gr.Markdown("### Please upload an image.")
            return

        detected_items = object_detection(image)
        detected_items_state.value = detected_items

        if not detected_items:
            gr.Markdown("### No items detected.")
            return

        gr.Markdown(f"### Detected Items ({len(detected_items)}):")
        user_choices = []
        for item in detected_items:
            with gr.Row():
                gr.Markdown(f"**{item}**")
                user_choice = gr.Radio(
                    choices=["recyclable", "non_recyclable"],
                    label=f"Classify '{item}'",
                )
                user_choices.append(user_choice)

        submit_btn = gr.Button("Submit")
        feedback_box = gr.Textbox(label="Feedback", lines=10, interactive=False)

        def evaluate_user_choices(*choices):
            feedback = []
            for detected_item, user_choice in zip(detected_items, choices):
                correct_choice = (
                    "recyclable"
                    if detected_item in waste_categories["recyclable"]
                    else "non_recyclable"
                )
                if user_choice == correct_choice:
                    feedback.append(
                        f"✅ Correct! '{detected_item}' is {correct_choice}."
                    )
                else:
                    explanation = generate_gpt_explanation(
                        detected_item, correct_choice, user_choice
                    )
                    feedback.append(
                        f"❌ Wrong! '{detected_item}' is {correct_choice}, not {user_choice}.\nExplanation: {explanation}"
                    )
            return "\n".join(feedback)

        submit_btn.click(
            evaluate_user_choices,
            inputs=user_choices,
            outputs=[feedback_box],
        )

demo.launch(share=True)
