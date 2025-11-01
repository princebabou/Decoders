"""
Barcode Decoder Script
Decodes various types of barcodes from images including QR codes, PDF417, Aztec, etc.
"""

import cv2
from pyzbar import pyzbar
from PIL import Image
import numpy as np
import os
import sys


def decode_barcode_pyzbar(image_path):
    """
    Decode barcodes using pyzbar library.
    Supports: QR Code, EAN, UPC, Code128, Code39, PDF417, Aztec, DataMatrix, etc.
    """
    print(f"\n{'='*60}")
    print(f"Processing: {os.path.basename(image_path)}")
    print(f"{'='*60}")
    
    # Read image using OpenCV
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Could not read image from {image_path}")
        return []
    
    # Convert to grayscale for better detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Try decoding from original image
    barcodes = pyzbar.decode(image)
    
    # If no barcodes found, try with grayscale
    if not barcodes:
        barcodes = pyzbar.decode(gray)
    
    # If still no barcodes, try with PIL
    if not barcodes:
        pil_image = Image.open(image_path)
        barcodes = pyzbar.decode(pil_image)
    
    results = []
    
    if barcodes:
        print(f"✓ Found {len(barcodes)} barcode(s)!\n")
        
        for idx, barcode in enumerate(barcodes, 1):
            # Extract barcode data
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            
            # Get barcode location
            (x, y, w, h) = barcode.rect
            
            print(f"Barcode #{idx}:")
            print(f"  Type: {barcode_type}")
            print(f"  Data: {barcode_data}")
            print(f"  Location: x={x}, y={y}, width={w}, height={h}")
            print()
            
            results.append({
                'type': barcode_type,
                'data': barcode_data,
                'location': (x, y, w, h)
            })
            
            # Draw rectangle around barcode on the image
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Put text above the barcode
            text = f"{barcode_type}: {barcode_data[:30]}"
            cv2.putText(image, text, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Save annotated image
        output_path = image_path.rsplit('.', 1)[0] + '_decoded.' + image_path.rsplit('.', 1)[1]
        cv2.imwrite(output_path, image)
        print(f"✓ Annotated image saved to: {output_path}\n")
        
    else:
        print("✗ No barcodes detected in this image.\n")
    
    return results


def decode_all_images_in_directory(directory="."):
    """
    Decode all barcode images in the specified directory.
    """
    # Supported image extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')
    
    print("\n" + "="*60)
    print("BARCODE DECODER - Batch Processing")
    print("="*60)
    
    # Find all image files
    image_files = [f for f in os.listdir(directory) 
                   if f.lower().endswith(image_extensions) 
                   and not f.endswith('_decoded.png') 
                   and not f.endswith('_decoded.jpg')]
    
    if not image_files:
        print("No image files found in the directory.")
        return
    
    print(f"Found {len(image_files)} image(s) to process.\n")
    
    all_results = {}
    
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        results = decode_barcode_pyzbar(image_path)
        all_results[image_file] = results
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    total_barcodes = sum(len(results) for results in all_results.values())
    successful_images = sum(1 for results in all_results.values() if results)
    
    print(f"Total images processed: {len(image_files)}")
    print(f"Images with barcodes: {successful_images}")
    print(f"Total barcodes decoded: {total_barcodes}")
    print()
    
    return all_results


def decode_single_image(image_path):
    """
    Decode a single image file.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return None
    
    return decode_barcode_pyzbar(image_path)


def main():
    """
    Main function to run the barcode decoder.
    """
    print("\n" + "="*60)
    print("BARCODE DECODER")
    print("="*60)
    print("Supports: QR Code, PDF417, Aztec, EAN, UPC, Code128, etc.")
    print("="*60 + "\n")
    
    # Check if a specific image path is provided as command line argument
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        decode_single_image(image_path)
    else:
        # Process all images in current directory
        decode_all_images_in_directory()


if __name__ == "__main__":
    main()
