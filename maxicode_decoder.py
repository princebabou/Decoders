from pyzbar.pyzbar import decode
from PIL import Image

def decode_barcode_from_path(image_path):
    # Open the image file from the given path
    image = Image.open(image_path)

    # Decode the barcode(s) in the image
    decoded_objects = decode(image)

    # If no barcode found
    if not decoded_objects:
        print("No barcode detected.")
        return

    # Print all decoded barcode data
    for obj in decoded_objects:
        print("Type:", obj.type)
        print("Data:", obj.data.decode('utf-8'))

# Example usage
image_path = 'barcode.jpg'
decode_barcode_from_path(image_path)
