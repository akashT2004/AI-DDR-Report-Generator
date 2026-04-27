import pypdf
import os
import sys

def inspect_pdf(file_path, output_file):
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"\n--- Inspecting: {file_path} ---\n")
        if not os.path.exists(file_path):
            f.write("File not found.\n")
            return

        try:
            reader = pypdf.PdfReader(file_path)
            f.write(f"Number of pages: {len(reader.pages)}\n")
            
            for i, page in enumerate(reader.pages):
                f.write(f"\n--- Page {i+1} ---\n")
                text = page.extract_text()
                f.write(text[:2000] + ("..." if len(text) > 2000 else ""))
                f.write("\n")
                
                # Check for images
                image_count = 0
                if '/Resources' in page and '/XObject' in page['/Resources']:
                    xObject = page['/Resources']['/XObject'].get_object()
                    for obj in xObject:
                        if xObject[obj]['/Subtype'] == '/Image':
                            image_count += 1
                f.write(f"Images found on page: {image_count}\n")

        except Exception as e:
            f.write(f"Error: {e}\n")

if __name__ == "__main__":
    output_path = "scripts/inspection_results.txt"
    if os.path.exists(output_path):
        os.remove(output_path)
    inspect_pdf("Sample Report.pdf", output_path)
    inspect_pdf("Thermal Images.pdf", output_path)
    print(f"Results saved to {output_path}")
