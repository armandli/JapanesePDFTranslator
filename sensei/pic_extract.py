"""
Picture extraction module for Japanese PDF Translator.

This module provides functionality to extract pictures from Japanese PDF files
and save them as individual PNG files.
"""

import sys
import argparse
from typing import List, Optional
from pathlib import Path
import io

# PDF processing libraries
import fitz  # PyMuPDF
from PIL import Image


class PDFImageExtractor:
  """Extracts images from PDF files and saves them as PNG files."""

  def __init__(self, input_pdf_path: str, output_prefix: str):
    self.input_pdf_path = Path(input_pdf_path)
    self.output_prefix = output_prefix

    if not self.input_pdf_path.exists():
      raise FileNotFoundError(f"Input PDF file not found: {input_pdf_path}")

  def extract_images(self) -> List[str]:
    """Extract images from PDF and save them as PNG files.

    Returns:
      List of output file paths for the extracted images.
    """
    output_files = []

    doc = fitz.open(self.input_pdf_path)

    image_counter = 0

    for page_num, page in enumerate(doc):
      image_list = page.get_images()

      for img_index, img in enumerate(image_list):
        # Get image data
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)

        if pix.n - pix.alpha < 4:  # GRAY or RGB
          img_data = pix.tobytes("png")
        else:  # CMYK needs conversion
          pix1 = fitz.Pixmap(fitz.csRGB, pix)
          img_data = pix1.tobytes("png")
          pix1 = None

        # Handle rotation for images
        if page.rotation != 0:
          img_pil = Image.open(io.BytesIO(img_data))
          if page.rotation == 180:
            img_pil = img_pil.rotate(180, expand=True)
          elif page.rotation == 90:
            img_pil = img_pil.rotate(-90, expand=True)
          elif page.rotation == 270:
            img_pil = img_pil.rotate(90, expand=True)

          # Save rotated image back to bytes
          img_buffer = io.BytesIO()
          img_pil.save(img_buffer, format='PNG')
          img_data = img_buffer.getvalue()

        # Generate output filename
        output_filename = f"{self.output_prefix}_{image_counter:03d}.png"
        output_path = Path(output_filename)

        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save image
        with open(output_path, 'wb') as f:
          f.write(img_data)

        output_files.append(str(output_path))
        image_counter += 1

        pix = None

    doc.close()
    return output_files


def main(argv: Optional[List[str]] = None) -> int:
  """Main entry point for the pic-extract command."""
  parser = argparse.ArgumentParser(
    description="Extract pictures from Japanese PDF files and save as PNG",
    prog="pic-extract"
  )

  parser.add_argument(
    "input_pdf",
    help="Path to the input PDF file"
  )

  parser.add_argument(
    "output_prefix",
    help="Output file path prefix for extracted images"
  )

  parser.add_argument(
    "--verbose",
    "-v",
    action="store_true",
    help="Enable verbose output"
  )

  args = parser.parse_args(argv)

  try:
    extractor = PDFImageExtractor(args.input_pdf, args.output_prefix)

    if args.verbose:
      print(f"Extracting images from {args.input_pdf}")
      print(f"Output prefix: {args.output_prefix}")

    output_files = extractor.extract_images()

    if args.verbose:
      print(f"Extracted {len(output_files)} images:")
      for file_path in output_files:
        print(f"  - {file_path}")
    else:
      print(f"Extracted {len(output_files)} images")

    return 0
  except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
  sys.exit(main())
