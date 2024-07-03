from PIL import Image
import io

def convert_local_blob_to_image(blob_path):
  try:
    # Open the blob file in binary read mode
    with open(blob_path, 'rb') as blob_file:
      image_data = blob_file.read()
  except FileNotFoundError:
    print("Error: Blob file not found at", blob_path)
    return None
  
  try:
    # Use Pillow to open the image data
    
    image = Image.open(io.BytesIO(image_data))
    if image.mode == 'RGBA':
      image = image.convert('RGB')
    return image
  except (IOError, SyntaxError):
    print("Error: Invalid image format or corrupted data")
    return None

# Replace '/Users/shrishaa/Garbage/website/imagesss/blob' with your actual path
blob_file_path = "/Users/shrishaa/Garbage/website/imagesss/blob"
image = convert_local_blob_to_image(blob_file_path)

if image:
  # Save the image (replace 'output_image.jpg' with your desired filename and format)
  image.save("/Users/shrishaa/Garbage/website/imagesss/blob_to_img/output_image.jpg")
  print("Image successfully converted and saved!")
else:
  print("Conversion failed. Check for errors in the console.")
