import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import datetime

# 🔐 Gemini API Configuration
genai.configure(api_key="AIzaSyBhoUEWI9gmaSwCi3jj2KJNW9gmArgb24g")  # 请替换为你的有效 key
model = genai.GenerativeModel(model_name="models/gemini-2.5-pro",
                              generation_config={"temperature": 0.7})

# 📁 Upload Path Setup
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🌐 Page Configuration
st.set_page_config(page_title="AI Outfit Stylist 🫐", layout="centered")
theme = st.toggle("🌗 Toggle Light / Dark Mode", value=True)

# 🎨 Dynamic Styling
background_color = "#f8f9fa" if theme else "#1e1e1e"
text_color = "#1e1e1e" if theme else "#f8f9fa"
button_color = "#4b0082"

st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{
        font-family: 'Times New Roman', serif;
        background-color: {background_color};
        color: {text_color};
    }}
    .stButton>button {{
        color: white !important;
        background-color: {button_color} !important;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 🖼️ Title & GIF
st.title("🫐 AI Outfit Assistant")
st.image("https://media.giphy.com/media/KzJkzjggfGN5Py6nkT/giphy.gif", width=150)
st.markdown("Let AI generate the perfect look for you today 👗👔")

# 🚻 Gender Selection
gender = st.radio("Select your gender:", ("Female 👧", "Male 👦"))

# 🎨 Style Selection
female_styles = ["Dark Academia 📚", "E-Girl 💀", "Soft Girl 🌸", "Edgy 🖤", "Boho 🌿", "Chic ✨", "Y2K 💿", "Surprise Me 🎲"]
male_styles = ["Streetwear 🧢", "Smart Casual 👞", "Business Formal 👔", "Athleisure 🏋️", "Preppy 🎓", "Minimalist ⚪", "Surprise Me 🎲"]

style = st.selectbox("Choose your outfit style:", female_styles if gender == "Female 👧" else male_styles)

# 📸 Upload Images
uploaded_files = st.file_uploader(
    "Upload your clothing / accessory photos (up to 5):",
    type=["jpg", "jpeg", "png", "avif"], accept_multiple_files=True
)

# 💾 Save Uploaded Files
image_paths = []
images_to_send = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        image_paths.append(file_path)
        images_to_send.append(Image.open(file_path))

# 🎯 Generate Outfit Suggestion
if st.button("✨ Generate My Outfit Suggestion!"):
    if not uploaded_files:
        st.warning("Please upload at least one image to proceed.")
    else:
        st.success("Generating suggestions... hang on 👗👕🧢")
        all_suggestions = []

        for idx, (img, path) in enumerate(zip(images_to_send, image_paths), start=1):
            prompt = f"""You are a professional fashion stylist. Based on the uploaded clothing/accessory image, 
please generate a complete outfit suggestion to match this piece.

👤 Gender: {gender}  
🎨 Preferred Style: {style}  
🖼️ This is outfit piece #{idx}.

The suggestion should be:
- 1 to 2 short creative paragraphs  
- Enhanced with emojis  
- Practical, stylish, and in English  
- Descriptive of matching tops, bottoms, shoes, and accessories"""

            try:
                response = model.generate_content([prompt, img])
                suggestion = response.text.strip().replace("\n", "\n\n")
                all_suggestions.append((img, suggestion))

            except Exception as e:
                st.error(f"❌ Failed to process image #{idx}: {e}")

        # 🖋️ Display All Suggestions
        for i, (img, suggestion) in enumerate(all_suggestions, start=1):
            st.image(img, caption=f"Photo #{i}", width=250)
            st.markdown(
                f"<div style='font-size:17px; line-height:1.8; color:{text_color}; background-color:rgba(255,255,255,0.05); padding:15px; border-radius:10px'>{suggestion}</div>",
                unsafe_allow_html=True
            )

        # 📝 Save to History
        with open("history.txt", "a", encoding="utf-8") as f:
            f.write(f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"👤 Gender: {gender} | 🎨 Style: {style}\n")
            for i, (_, suggestion) in enumerate(all_suggestions, start=1):
                f.write(f"📸 Image #{i} Suggestion:\n{suggestion}\n")
            f.write("="*40 + "\n")
