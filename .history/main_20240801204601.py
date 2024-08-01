### Health Management APP
from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(prompt, image, input_text):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-001')
        response = model.generate_content([prompt, image[0], input_text])
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Function to setup input image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            # Read the file into bytes
            bytes_data = uploaded_file.getvalue()
            image_parts = [
                {
                    "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                    "data": bytes_data
                }
            ]
            return image_parts
        except Exception as e:
            st.error(f"Error processing the uploaded file: {e}")
            return None
    else:
        st.error("No file uploaded")
        return None

# Initialize our Streamlit app
st.set_page_config(page_title="NutriVision AI")
st.header("NutriVision AI")

image_path = 'assets/aidoctor.png'
try:
    st.image(image_path, caption='NutriVision AI', width=500)
except Exception as e:
    st.error(f"Error loading image: {e}")

uploaded_file = st.file_uploader("Choose an Image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
    except Exception as e:
        st.error(f"Error opening uploaded image: {e}")

submit = st.button("Tell me the total calories")

input_prompt = """
You are an expert nutritionist. You need to see the food items from the image
and calculate the total calories. Also, provide details of every food item with its calorie intake
in the format below:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----
"""

# If submit button is clicked
if submit:
    if uploaded_file is None:
        st.error("Please upload an image file before submitting.")
    else:
        image_data = input_image_setup(uploaded_file)
        if image_data:
            response = get_gemini_response(input_prompt, image_data, "")
            if response:
                st.subheader("The Response is")
                st.write(response)
