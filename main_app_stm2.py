import streamlit as st
from PIL import Image
import tempfile
import predict_TM
import llm_app

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Gesture Num : Decoding Sign Into Digits",
    page_icon="✌️",
    layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#0F172A,#1E293B,#2563EB);
}

.block-container{
padding-top:25px;
padding-bottom:30px;
}

/* Title */

.title{
text-align:center;
font-size:45px;
font-weight:800;
color:white;
}

.subtitle{
text-align:center;
font-size:18px;
color:#CBD5E1;
margin-bottom:30px;
}

/* Cards */

[data-testid="stVerticalBlock"]{
gap:1rem;
}

.card{

background:#111827;

padding:20px;

border-radius:20px;

border:1px solid #374151;

box-shadow:0px 8px 20px rgba(0,0,0,.35);

}

/* Prediction */

.prediction{

background:linear-gradient(90deg,#059669,#10B981);

padding:18px;

border-radius:15px;

text-align:center;

font-size:24px;

font-weight:bold;

color:white;

margin-top:15px;

}

/* File uploader */

[data-testid="stFileUploader"]{

background:#1F2937;

padding:12px;

border-radius:15px;

border:2px dashed #3B82F6;

}

/* Camera */

[data-testid="stCameraInput"]{

background:#1F2937;

padding:12px;

border-radius:15px;

border:2px dashed #3B82F6;

}

/* Radio */

div[role="radiogroup"] label{

color:white !important;

font-size:17px !important;

font-weight:bold;

}

/* Text */

h1,h2,h3{

color:#60A5FA;

}

p{

color:#F3F4F6;

font-size:17px;

line-height:1.7;

}

img{

border-radius:15px;

}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="title">
✌️ Gesture Num : Decoding Sign Into Digits
</div>

<div class="subtitle">
AI Powered Hand Gesture Number Recognition
</div>
""", unsafe_allow_html=True)

# ---------------- LAYOUT ----------------

left,right=st.columns([1,1.4])

image=None
topic=None

# ---------------- LEFT ----------------

with left:

    st.markdown("### 📥 Upload Gesture")

    option=st.radio(
        "",
        ["📁 Upload Image","📷 Camera"],
        horizontal=True
    )

    if option=="📁 Upload Image":

        uploaded=st.file_uploader(
            "Choose Image",
            type=["jpg","jpeg","png"]
        )

        if uploaded:

            image=Image.open(uploaded)

    else:

        camera=st.camera_input("Capture Gesture")

        if camera:

            image=Image.open(camera)

    if image:

        st.image(
            image,
            caption="Uploaded Gesture",
            width=200
        )

        with tempfile.NamedTemporaryFile(delete=False,suffix=".jpg") as temp:

            image.save(temp.name)

            img_path=temp.name

        with st.spinner("Predicting..."):

            topic=predict_TM.predict_TM(img_path)

        st.markdown(f"""
        <div class="prediction">
        ✅ Predicted Digit : {topic}
        </div>
        """,unsafe_allow_html=True)

# ---------------- RIGHT ----------------

with right:

    st.markdown("### 🤖 AI Description")

    if topic:

        description=llm_app.llm_app(topic)

        st.success("Prediction Completed")

        st.write(description)

        st.markdown("---")

        st.markdown("### 📊 Prediction Details")

        c1,c2=st.columns(2)

        with c1:
            st.metric("Predicted Digit",topic)

        with c2:
            st.metric("Status","Detected")

        st.progress(100)

    else:

        st.info("Upload an image or capture a gesture to start prediction.")

# ---------------- FOOTER ----------------

st.markdown("---")

st.caption("Gesture Num : Decoding Sign Into Digits | AI Powered Hand Gesture Recognition System")