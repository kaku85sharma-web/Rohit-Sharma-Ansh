import streamlit as st
from PIL import Image
import tempfile
import predict_TM
import llm_app

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Image Topic Prediction",
    page_icon="🖼️",
    layout="wide"
)

st.title("🖼️ Image Topic Prediction using LLM")

# Create two columns
col1, col2 = st.columns([1, 2])

# ===================================
# LEFT COLUMN
# Upload + Prediction
# ===================================
with col1:

    st.subheader("Upload Image")

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=300 )

        # Save uploaded image temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        image.save(temp_file.name)

        # Predict Topic
        topic = predict_TM.predict_TM(temp_file.name)

        st.markdown("---")
        st.subheader("Prediction")
        st.success(topic)

# ===================================
# RIGHT COLUMN
# LLM Description
# ===================================
        output = llm_app.llm_app(topic)

        with col2:
            st.subheader("Description")
            st.write(output)