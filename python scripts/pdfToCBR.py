import os
import fitz  # PyMuPDF library for PDF handling
import patoolib  # patool library for creating CBR archives

def pdf_to_cbr(pdf_path, output_cbr):
    # Create a temporary directory for image files
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)

    # Extract PDF pages as images (JPEG format) in the temporary directory
    pdf_document = fitz.open(pdf_path)
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        image = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))  # 300 DPI
        image_path = os.path.join(temp_dir, f"page_{page_number + 1:03d}.jpg")
        image.save(image_path, "jpeg")

    pdf_document.close()

    # Create a CBR archive
    patoolib.create_archive(output_cbr, (temp_dir,), verbosity=-1)

    # Clean up: remove temporary image files and directory
    for file in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file)
        os.remove(file_path)
    os.rmdir(temp_dir)

if __name__ == "__main__":
    input_pdf = "input/slaine theking - Pat Mills.pdf"  # Replace with your input PDF file
    output_cbr = "output/slaine theking - Pat Mills.cbr"  # Replace with the desired output CBR file

    pdf_to_cbr(input_pdf, output_cbr)
    print(f"CBR file '{output_cbr}' created successfully.")
