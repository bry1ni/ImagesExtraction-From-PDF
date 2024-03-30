import os
import io
from PIL import Image
import fitz  # PyMuPDF


def extract_images_from_pdf(pdf_path, output_folder, min_width=0, min_height=0, min_area=0, output_format="png"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_file = fitz.open(pdf_path)
    image_paths = []

    # PDF pages
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        image_list = page.get_images(full=True) # get images present in the page
        
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print(f"[!] No images found on page {page_index}")
        # Images 
        for image_index, img in enumerate(image_list, start=1):
                # Get the XREF of the image
                xref = img[0]
                # Extract the image bytes
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                # Get the image extension
                image_ext = base_image["ext"]
                # Load it to PIL
                image = Image.open(io.BytesIO(image_bytes))
                # Check if image meets the size criteria
                if image.width * image.height >= min_area:
                    image_path = os.path.join(output_folder, f"image{page_index + 1}_{image_index}.{output_format}")
                    image.save(open(image_path, "wb"), format=output_format.upper())
                    image_paths.append(image_path)
                    print(
                        f"[+] Image {image_index} saved from page {page_index} with size {image.width}x{image.height}")
                else:
                    print(
                        f"[-] Skipping small image {image_index} on page {page_index} with size {image.width}x{image.height}")

    return image_paths


pdf_path = "/Users/rayanpicso/Desktop/Humanaize/DATA_retrieval/Data/manual-1st-doc.pdf"
output_folder = "manual1-pieces-solvedTRY2"  # output folder
min_area = 10000  # min resolution

extract_images_from_pdf(pdf_path, output_folder, min_area=min_area)
