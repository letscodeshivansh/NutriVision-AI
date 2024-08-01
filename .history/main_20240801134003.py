### Health Management APP
from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input, image, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input, image[0], prompt])
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
    st.image(image_path, caption='NutriVision AI', width=600)
except Exception as e:
    st.error(f"Error loading image: {e}")

input = st.text_input("Input Prompt: ", key="input")
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
    image_data = input_image_setup(uploaded_file)
    if image_data is not None:
        response = get_gemini_response(input_prompt, image_data, input)
        if response:
            st.subheader("The Response is")
            st.write(response)
