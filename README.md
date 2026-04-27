# AI DDR Report Generator 🏗️🤖

An intelligent AI-powered system designed to automate the creation of **Detailed Diagnostic Reports (DDR)** for property inspections. This tool processes visual inspection forms and thermal imaging reports to synthesize a comprehensive engineering diagnostic.

## 🚀 Overview
The **AI DDR Report Generator** solves the problem of manual data entry and multi-document cross-referencing in structural engineering. It uses AI to "link" human site observations with scientific thermal data, identifying root causes of moisture ingress and structural distress.

## ✨ Key Features
- **PDF Data Extraction**: Automatically rips text and images from complex PDF reports (Inspection & Thermal).
- **Intelligent Data Linking**: Matches site photos to thermal heatmaps by reasoning through room context and temperature anomalies.
- **Full-Page Rendering**: Captures complete technical pages to preserve markers, heatmaps, and reference photos.
- **Professional DDR Output**: Generates a structured 7-point Markdown report:
  1. Property Issue Summary
  2. Area-wise Observations (with visual evidence)
  3. Probable Root Cause
  4. Severity Assessment
  5. Recommended Actions
  6. Additional Notes
  7. Missing/Unclear Information
- **Modern Web UI**: A sleek Streamlit dashboard for easy file uploads and interactive report previews.

## 🛠️ Tech Stack
- **Language**: Python 3.11+
- **Frontend/Backend**: Streamlit
- **PDF Engine**: PyMuPDF (fitz)
- **AI Reasoning**: Gemini 1.5 Flash (via `google-genai`)
- **Image Processing**: Pillow (PIL)

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-DDR-report-generator.git
   cd AI-DDR-report-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 📖 How it Works
The core logic resides in `report_logic.py`. The system processes two input streams:
1. **Visual Input**: Photos showing peeling paint, cracks, or dampness.
2. **Technical Input**: Thermal scans showing temperature coldspots.

The AI analyzes the spatial data to confirm if a visual stain is an *active* leak based on its thermal signature, then formats the finding into a professional client-ready document.

## 🎥 Demo Video
[Link to Loom Video](YOUR_LOOM_LINK_HERE)

## 📄 License
MIT License
