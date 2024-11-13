import os
import fitz  # PyMuPDF
from PIL import Image


def convert_pdf_to_jpg(pdf_path, output_folder, dpi=300, quality=95):
    """
    Convert a PDF file to a series of JPG images.
    
    :param pdf_path: Path to the PDF file
    :param output_folder: Folder to save the JPG images
    :param dpi: DPI for the output images (default: 300)
    :param quality: JPEG quality (0-100, default: 95)
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Iterate through each page
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_number]
        
        # Set the zoom factor based on DPI
        zoom = dpi / 72  # 72 is the default DPI for PDF
        
        # Create a matrix for rendering
        mat = fitz.Matrix(zoom, zoom)
        
        # Render page to an image
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save as JPG
        output_file = os.path.join(output_folder, f"page_{page_number + 1}.jpg")
        img.save(output_file, "JPEG", quality=quality)
        
        print(f"Saved page {page_number + 1} as {output_file}")
    
    # Close the PDF file
    pdf_document.close()