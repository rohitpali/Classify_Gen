import streamlit as st
from pipeline.pipeline import AssetCheckPipeline

st.set_page_config(page_title="ClassifyGen", layout="wide")

st.title("🧠 ClassifyGen")
st.write("Upload your text or file and get classification instantly.")

pipeline = AssetCheckPipeline()

# Input option
option = st.radio("Choose input type:", ["Text", "File"])

if option == "Text":
    text = st.text_area("Enter text here")
    classification = st.selectbox("Select classification type:", ["Laptop", "Mobile", "Camera", "General"])

    if st.button("Classify"):
        if text.strip() != "":
            with st.spinner("Processing..."):
                result = pipeline.predict(text, classification)
            st.success(f"Classification Result:\n{result}")
        else:
            st.error("Please enter some text.")

else:
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    classification = st.selectbox("Select classification type:", ["Laptop", "Mobile", "Camera", "General"])

    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        if st.button("Classify File"):
            with st.spinner("Processing..."):
                result = pipeline.predict(content, classification)
            st.success(f"Classification Result:\n{result}")
