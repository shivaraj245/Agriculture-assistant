# importing neccseary modules
import streamlit as st
from pathlib import Path
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

#from apikey import api_key1
# set the page configuration
api_key1 = os.getenv('api_key1')
# set the page configuration
st.set_page_config(page_title="Vital Image Analytics", page_icon=":robot:")

# config gemini api key
genai.configure(api_key=api_key1)

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 8192,
}

# saftey setting
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_prompt = """
A agricuture/horticulture specialist who works for MNC that helps farmers to produce good quality products.  
You should analyse the image and give the complete details on that particular image.

Your Responsibilities include:

1.Detailed Analysis: Thoroughly analyze each image, focusing on identifing what is in the image.

2.Requitements: Document all observed requirements that is needed to grow the crop. Clearly articulate these findings.

3.Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including future activites needed to be done have better yield that are required.

4.Suggestions: If appropriate, recommend possible fertiliser and nutrients that is needed for this crop/grain, in what ratio and give detailed note.

5.other idea: Tell me what are the other common plants that could be grown with this that are suitable. It should be able to idetify what it is, its ideal temperature,soil for growth and the origin.


IMPORTANT NOTE:only provide answer when yhe image is realted to agriculture ,farming if not reply with "Please upload valid image"

Please provide me an output with these 4 heading 1)detailed analysis, 2)Requitements, 3)Recommendations and Next Steps, 4)Suggestions, 5)other idea

"""

# model configaration
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


# set the logo
st.image(r"OIG2.jpeg", width=150)

# set the title

st.title(" Ai 🤖 Agriculture Assistant 🌾🧑‍🌾👩‍🌾")

# set the subtitle

st.subheader("An application that can help users to identify Arigulture  images")

uploaded_file = st.file_uploader("Upload the Agriculture image for analysis", type=["png", "jpg", "jpeg"])
if uploaded_file:
    # displaying image
    st.image(uploaded_file, width=250, caption="Uploaded crop/grains image")
submit_button = st.button("Generate Analysis")

if submit_button:
    image_data = uploaded_file.getvalue()

    # making image ready
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },

    ]

    # making inbuilt promt ready
    prompt_parts = [

        image_parts[0],
        system_prompt,
    ]

    st.title("Here is the analysis based on image that is")
    # genarating reponse
    response = model.generate_content(prompt_parts)
    st.write(response.text)


