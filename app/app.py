import streamlit as st
from transformers import LlamaTokenizer, LlamaForCausalLM
from pptx import Presentation

# Load the trained model and tokenizer
tokenizer = LlamaTokenizer.from_pretrained('./trained_model')
model = LlamaForCausalLM.from_pretrained('./trained_model')

def extract_text_from_pptx(file):
    prs = Presentation(file)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return " ".join(text)

def generate_summary(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=128, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Streamlit app
st.title("PPT Summarizer")
uploaded_file = st.file_uploader("Upload a PPT file", type=["pptx"])

if uploaded_file is not None:
    text = extract_text_from_pptx(uploaded_file)
    summary = generate_summary(text)
    st.write("Summary:")
    st.write(summary)
