import streamlit as st
import tempfile
import google.generativeai as genai

from api_key import api_key
genai.configure(api_key=api_key)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

system_prompts = """
Your Responsibility:
1. Detailed Analysis : Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report : Document all observed anomalies or signs of diseases. 
3. Recommedations and Next Steps : Based on your analysis, suggest potential next steps
4. Treatment Suggestions: If appropriate, recommend possible treatment options

Important Notes:
Scope of Response: Only respond if image pertains to human health issues
clarity of images : In case where the image quality impedes clear analysis
Disclaimer : Accompany your analysis with disclaimer : "Consult with your Doctor"

Please provide me an output with these 4 headings
"""

# Set page config
st.set_page_config(page_title="MediScan AI", page_icon=":robot")

# Set the title
st.title("MediScan AI 🧑‍⚕️❤️‍🩹")
st.subheader("A chatbot to identify your diseases")
uploaded_file = st.file_uploader("Upload image for analysis", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file,width=250,caption="Medical images")

submit_button = st.button("Generate the Analysis")

def upload_to_gemini(temp_file_path, mime_type=None):
    """Uploads the given file path to Gemini."""
    file = genai.upload_file(temp_file_path, mime_type=mime_type)
    # st.write(f"Uploaded file as: {file.uri}")
    return file

if submit_button and uploaded_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

    mime_type = uploaded_file.type  # Get MIME type of the uploaded file

    # Upload the image file to Gemini
    file = upload_to_gemini(temp_file_path, mime_type=mime_type)

    # Set up prompt parts
    prompt_parts = [
       file,
       system_prompts,
    ]

    # Start chat session
    chat_session = model.start_chat(history=[
        {
            "role": "user",
            "parts": [file, "What is this?"],
        }
    ])

    
    st.title("Here is the analysis based on your image: ")
    # Send message to get analysis
    response = chat_session.send_message(prompt_parts)
    st.write(response.text)
