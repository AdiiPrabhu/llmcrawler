import streamlit as st
import pandas as pd
import traceback
from main import extract_all
from utils import save_data
import json

st.set_page_config(page_title="LLM Employee Extractor", layout="wide")
st.title("🧠 LLM-Powered Employee Extractor")

with st.sidebar:
    st.header("🔧 Settings")
    seed_url = st.text_input("Seed URL", placeholder="https://example.com")
    depth = st.slider("Recursion Depth", min_value=1, max_value=4, value=2)
    max_pages = st.slider("Max Pages to Crawl", min_value=1, max_value=100, value=20)
    output_format = st.radio("Output Format", ["CSV", "JSON"])

if st.button("🚀 Run Extraction"):
    if not seed_url:
        st.error("Please enter a valid seed URL.")
    else:
        try:
            with st.spinner("Working... This may take a few seconds..."):
                data = extract_all(seed_url, depth, max_pages)

            if data:
                df = pd.DataFrame(data)
                st.success(f"✅ Found {len(df)} employee entries")
                st.dataframe(df)

                if output_format == "CSV":
                    csv_data = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇ Download CSV", data=csv_data, file_name="employees.csv", mime="text/csv")
                else:
                    json_data = json.dumps(data, indent=2)
                    st.download_button("⬇ Download JSON", data=json_data, file_name="employees.json", mime="application/json")
            else:
                st.warning("⚠️ No employee data found.")
        except Exception:
            st.error("❌ An error occurred while processing.")
            st.code(traceback.format_exc())
