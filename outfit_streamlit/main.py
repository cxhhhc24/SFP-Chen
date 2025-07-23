import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import datetime

# 🔐 Gemini API Key Configuration
genai.configure(api_key="AIzaSyBhoUEWI9gmaSwCi3jj2KJNW9gmArgb24g")  # ← Replace with your actual Gemini API key
model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")

# 📁 Upload Folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🌐 Page Config
st.set_page_config(page_title="AI Outfit Stylist 🫐", layout="centered")
theme = st.toggle("🌗 Toggle Light / Dark Mode", value=True)

# 🎨 Styling Colors (High Contrast)
background_color = "#ffffff" if theme else "#0f0f0f"
text_color = "#0f0f0f" if theme else "#f0f0f0"
button_color = "#4b0082"
contrast_box_color = "#f0f8ff" if theme else "#2a2a2a"

# 💅 Custom Styling
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font-family: 'Times New Roman', serif;
        background-color: {background_color};
        color: {text_color};
    }}
    .stButton>button {{
        color: white !important;
        background-color: {button_color} !important;
        border-radius: 12px;
        padding: 10px 22px;
        font-size: 16px;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# 🖼️ Title & GIF
st.title("🫐 AI Outfit Assistant")
try:
    st.image("https://media.tenor.com/SI1t4cUQwYkAAAAC/fashion-style.gif", width=180)
except:
    st.markdown("🧥 Welcome to your AI Stylist!")

st.markdown("Let AI help you create the perfect outfit today! 👗👕")

# 🚻 Gender & Style
gender = st.radio("Select your gender:", ("Female 👧", "Male 👦"))

female_styles = [
    "Dark Academia 📚", "E-Girl 💀", "Soft Girl 🌸", "Edgy 🖤", 
    "Boho 🌿", "Chic ✨", "Y2K 💿", "Surprise Me 🎲"
]
male_styles = [
    "Streetwear 🧢", "Smart Casual 👞", "Business Formal 👔", 
    "Athleisure 🏋️", "Preppy 🎓", "Minimalist ⚪", "Surprise Me 🎲"
]

style = st.selectbox("Choose your outfit style:",
                     female_styles if gender == "Female 👧" else male_styles)

# 📸 File Upload
uploaded_files = st.file_uploader(
    "Upload up to 5 clothing / accessory photos:",
    type=["jpg", "jpeg", "png", "avif"],
    accept_multiple_files=True
)

image_paths = []
images_to_send = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        image_paths.append(file_path)
        images_to_send.append(Image.open(file_path))

# 🎯 Generate Suggestion
if st.button("✨ Generate My Outfit Suggestion!"):
    if not uploaded_files:
        st.warning("Please upload at least one image first.")
    else:
        st.info("Generating outfit suggestions... Please wait 👗🧥🧢")
        all_suggestions = []

        for idx, (img, path) in enumerate(zip(images_to_send, image_paths), start=1):
            prompt = f"""You are a professional fashion stylist. Based on the uploaded clothing or accessory photo,
please generate a complete outfit suggestion that complements it.

👤 Gender: {gender}  
🎨 Preferred Style: {style}  
🖼️ Item #{idx}

Please include:
- 1–2 stylish and engaging paragraphs of outfit suggestions  
- Use emojis to enhance tone  
- Matching top, bottom, shoes, and accessories  
- Output in English only"""

            try:
                response = model.generate_content([prompt, img])
                suggestion = response.text.strip().replace("\n", "\n\n")
                all_suggestions.append((img, suggestion))
            except Exception as e:
                st.error(f"❌ Error generating suggestion for Image #{idx}: {e}")

        for i, (img, suggestion) in enumerate(all_suggestions, start=1):
            st.image(img, caption=f"Uploaded Photo #{i}", width=250)
            st.markdown(f"""
                <div style='font-size:17px; line-height:1.8; 
                            color:{text_color}; 
                            background-color:{contrast_box_color}; 
                            padding:15px; border-radius:10px'>
                    {suggestion}
                </div>
            """, unsafe_allow_html=True)

        # 💾 Save History
        with open("history.txt", "a", encoding="utf-8") as f:
            f.write(f"\n📅 {datetime.datetime.now()}\n")
            f.write(f"👤 Gender: {gender} | 🎨 Style: {style}\n")
            for i, (_, suggestion) in enumerate(all_suggestions, 1):
                f.write(f"📸 Image #{i} Suggestion:\n{suggestion}\n")
            f.write("=" * 60 + "\n")
