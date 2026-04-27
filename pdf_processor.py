import fitz  # PyMuPDF
import os
import json
import re

def extract_from_pdf(pdf_path, output_dir):
    """Extracts text and images from a PDF."""
    doc = fitz.open(pdf_path)
    base_name = os.path.basename(pdf_path).replace(".pdf", "").replace(" ", "_")
    
    data = {
        "filename": pdf_path,
        "pages": []
    }
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    img_dir = os.path.join(output_dir, "images", base_name)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        
        page_data = {
            "page_num": page_num + 1,
            "text": text,
            "images": []
        }
        
        # 1. Capture FULL PAGE view (Ensures markers and overlays are preserved)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # High resolution
        full_page_path = os.path.join(img_dir, f"page{page_num+1}_full.png")
        pix.save(full_page_path)
        page_data["full_view"] = full_page_path
        
        # 2. Extract individual raw images (for backup)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_filename = f"page{page_num+1}_img{img_index+1}.{image_ext}"
                image_path = os.path.join(img_dir, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                page_data["images"].append({
                    "path": image_path,
                    "xref": xref
                })
            except:
                continue
            
        data["pages"].append(page_data)
        
    return data

def process_reports(inspection_pdf, thermal_pdf, result_json):
    print("Extracting from Inspection Report...")
    inspection_data = extract_from_pdf(inspection_pdf, "temp_data")
    
    print("Extracting from Thermal Report...")
    thermal_data = extract_from_pdf(thermal_pdf, "temp_data")
    
    combined_data = {
        "inspection": inspection_data,
        "thermal": thermal_data
    }
    
    with open(result_json, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=4)
    
    print(f"Data extracted and saved to {result_json}")

if __name__ == "__main__":
    process_reports("Sample Report.pdf", "Thermal Images.pdf", "data/extracted_data.json")
