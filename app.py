import streamlit as st
import os
import json
import warnings
from pdf_processor import process_reports
from report_logic import generate_ddr
from PIL import Image

# Mute FutureWarnings for a clean demo
warnings.filterwarnings("ignore", category=FutureWarning)

# Page Config
st.set_page_config(page_title="AI DDR Report Generator", page_icon="🏗️", layout="wide")

# Styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ AI DDR Report Generator")
st.subheader("Transform technical inspection data into structured diagnostic reports")

# File Uploaders
col1, col2 = st.columns(2)

with col1:
    inspection_file = st.file_uploader("Upload Inspection Report (PDF)", type=["pdf"])
with col2:
    thermal_file = st.file_uploader("Upload Thermal Images (PDF)", type=["pdf"])

if st.button("Generate Diagnostic Report"):
    if inspection_file and thermal_file:
        with st.spinner("Processing documents... This may take a moment."):
            # 1. Save uploaded files to temp
            if not os.path.exists("temp_uploads"):
                os.makedirs("temp_uploads")
            
            insp_path = os.path.join("temp_uploads", inspection_file.name)
            therm_path = os.path.join("temp_uploads", thermal_file.name)
            
            with open(insp_path, "wb") as f:
                f.write(inspection_file.getbuffer())
            with open(therm_path, "wb") as f:
                f.write(thermal_file.getbuffer())
            
            # 2. Run Pipeline
            try:
                extracted_json = "data/extracted_data.json"
                final_output = "output/DDR_Report.md"
                
                # Extraction
                process_reports(insp_path, therm_path, extracted_json)
                
                # Reasoning
                generate_ddr(extracted_json, final_output)
                
                st.success("Report Generated Successfully!")
                
                # 3. Display Results
                tab1, tab2 = st.tabs(["📄 Final Report", "🖼️ Extracted Images"])
                
                with tab1:
                    if os.path.exists(final_output):
                        with open(final_output, "r", encoding="utf-8") as f:
                            report_md = f.read()
                        
                        # Better way to show the report in Streamlit
                        st.header("Diagnostic Report Preview")
                        
                        # Split report by image tags to interleave st.markdown and st.image
                        parts = report_md.split("![")
                        st.markdown(parts[0]) # Show the title/summary
                        
                        for part in parts[1:]:
                            try:
                                # Extract caption and path
                                caption_end = part.find("]")
                                path_start = part.find("(") + 1
                                path_end = part.find(")")
                                
                                caption = part[:caption_end]
                                path = part[path_start:path_end]
                                remaining_text = part[path_end+1:]
                                
                                if os.path.exists(path):
                                    st.image(path, caption=caption)
                                st.markdown(remaining_text)
                            except:
                                st.markdown(f"![{part}") # Fallback
                                
                        st.download_button("Download Report (.md)", report_md, file_name="DDR_Report.md")
                
                with tab2:
                    st.write("Below are the images extracted and analyzed by the system.")
                    img_dir = "temp_data/images"
                    if os.path.exists(img_dir):
                        for root, dirs, files in os.walk(img_dir):
                            for file in files:
                                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                                    img_path = os.path.join(root, file)
                                    st.image(img_path, caption=f"Source: {file}")
                
            except Exception as e:
                st.error(f"Error during processing: {str(e)}")
    else:
        st.warning("Please upload both PDF reports first.")

st.markdown("---")
st.caption("AI Generalist Assignment | Applied AI Builder System")
