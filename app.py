import streamlit as st
import os
import pandas as pd
from parser import process_resume  # Your existing resume parsing function

st.set_page_config(page_title="📄 Resume Parser", layout="centered")
st.title("🚀 Resume Parser Tool")

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
    }
    .stButton>button {
        background-color: #6c63ff;
        color: white;
        border-radius: 12px;
        padding: 0.5em 1em;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #5751d6;
    }
</style>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader("📎 Upload your PDF resumes", type="pdf", accept_multiple_files=True)

if uploaded_files and len(uploaded_files) > 0:
    st.success(f"✅ {len(uploaded_files)} resume(s) uploaded!")

    results = []
    resume_folder = "Uploaded_Resumes"
    os.makedirs(resume_folder, exist_ok=True)

    for uploaded_file in uploaded_files:
        save_path = os.path.join(resume_folder, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        result = process_resume(save_path)
        results.append(result)

    df = pd.DataFrame(results)

    st.markdown("### 📊 Parsed Resume Data")

    if not df.empty:
        # Sorting options
        sort_column = st.selectbox("🔽 Sort by", df.columns)
        sort_order = st.radio("Order", ["Ascending", "Descending"], horizontal=True)

        sorted_df = df.sort_values(by=sort_column, ascending=(sort_order == "Ascending"))

        st.dataframe(sorted_df, use_container_width=True)

        # Download button for sorted CSV
        st.download_button("📥 Download Sorted CSV", sorted_df.to_csv(index=False), file_name="sorted_parsed_resumes.csv")
else:
    st.info("👆 Upload one or more PDF resumes to begin!")
