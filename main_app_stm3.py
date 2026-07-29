import streamlit as st
from PIL import Image
import tempfile
import os

import predict_TM
import llm_app

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Gesture Num : Decoding Sign Into Digits",
    page_icon="✌️",
    layout="wide"
)

# ---------------- API KEY ----------------

try:
    groq_api_key = st.secrets["groq_api_key"]
except Exception:
    groq_api_key = ""

# ---------------- CSS : BLACK + RED ----------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }

    h1, h2, h3, h4 {
        color: #ff0000;
    }

    .prediction-box {
        background-color: #111111;
        border: 2px solid #ff0000;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: #ffffff;
        font-size: 24px;
        font-weight: bold;
        margin-top: 15px;
    }

    .stButton>button {
        background-color: #ff0000;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------

st.markdown(
    """
    <h1 style='text-align:center;'>✌️ Gesture Num</h1>
    <p style='text-align:center; color:white;'>
    Decoding Sign Into Digits
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- LAYOUT ----------------

left, right = st.columns([1, 1.4])

image = None
topic = None

# ---------------- LEFT SIDE ----------------

with left:

    st.markdown("### 📥 Upload Gesture")

    option = st.radio(
        "Choose Input",
        ["📁 Upload Image", "📷 Camera"],
        horizontal=True
    )

    if option == "📁 Upload Image":

        uploaded = st.file_uploader(
            "Choose Image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded is not None:
            image = Image.open(uploaded)

    else:

        camera = st.camera_input("Capture Gesture")

        if camera is not None:
            image = Image.open(camera)

    if image is not None:

        st.image(image, caption="Uploaded Gesture", width=250)

        # Save temporary image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:

            image.save(temp.name)

            img_path = temp.name

        # Prediction
        try:
            with st.spinner("Predicting Gesture..."):
                topic = predict_TM.predict_TM(img_path)

            st.markdown(
                f"""
                <div class='prediction-box'>
                ✅ Predicted Digit : {topic}
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Prediction Error : {e}")

        finally:
            if os.path.exists(img_path):
                os.remove(img_path)

# ---------------- RIGHT SIDE ----------------

with right:

    st.markdown("### 🤖 AI Description")

    if topic is not None:

        # AI description
        try:
            description = llm_app.llm_app(topic, groq_api_key)
        except Exception:
            description = f"The detected digit is {topic}."

        st.success("Prediction Completed")

        st.write(description)

        st.markdown("---")

        # ---------------- VOICE OUTPUT ----------------

        st.markdown("### 🔊 Listen to Answer")

        try:
            from gtts import gTTS

            speech_text = f"Predicted digit is {topic}. {description}"

            tts = gTTS(text=speech_text, lang="en")

            audio_file = "answer.mp3"

            tts.save(audio_file)

            with open(audio_file, "rb") as audio:
                st.audio(audio.read(), format="audio/mp3")

            os.remove(audio_file)

        except Exception:
            st.warning(
                "Voice feature not available. Install gTTS using: pip install gTTS"
            )

        st.markdown("---")

        # ---------------- METRICS ----------------

        st.markdown("### 📊 Prediction Details")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Predicted Digit", topic)

        with c2:
            st.metric("Status", "Detected")

        st.progress(100)

    else:

        st.info("Upload an image or capture a gesture to start prediction.")

# ---------------- FOOTER ----------------

st.markdown("---")

st.caption(
    "Gesture Num | AI Powered Hand Gesture Recognition System"
)
