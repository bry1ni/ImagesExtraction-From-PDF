import os
import io
from PIL import Image
import fitz  # PyMuPDF


def extract_images_from_pdf(pdf_path, output_folder, min_width=0, min_height=0, min_area=0, output_format="png"):
    collage = False
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_file = fitz.open(pdf_path)
    image_paths = []

    # Iterate over PDF pages
    for page_index in range(len(pdf_file)):
        # Get the page itself
        page = pdf_file[page_index]
        # Get image list
        image_list = page.get_images(full=True)
        # Print the number of images found on this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            if len(image_list) > 10:
                collage = True
        else:
            print(f"[!] No images found on page {page_index}")
        # Iterate over the images on the page
        for image_index, img in enumerate(image_list, start=1):
            if collage:
                # make a collage of all images
                images = []
                for img in image_list:
                    xref = img[0]
                    base_image = pdf_file.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    images.append(image)
                widths, heights = zip(*(i.size for i in images))
                total_width = sum(widths)
                max_height = max(heights)
                collage = Image.new('RGB', (total_width, max_height))
                x_offset = 0
                y_offset = 0
                for i, img in enumerate(images):
                    collage.paste(img, (x_offset, y_offset))
                    x_offset += img.width
                    if (i + 1) % 5 == 0:  # Start a new row after every 5 images
                        y_offset += img.height
                        x_offset = 0
                collage_path = os.path.join(output_folder, f"collage{page_index + 1}.{output_format}")
                collage.save(open(collage_path, "wb"), format=output_format.upper())
                image_paths.append(collage_path)
                print(f"[+] Collage saved from page {page_index}")
                collage = False

            else:
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
output_folder = "manual1-pieces-solvedTRY2"  # Output folder to save the images
min_area = 10000  # Minimum area (width * height) for images to be saved

extract_images_from_pdf(pdf_path, output_folder, min_area=min_area)
