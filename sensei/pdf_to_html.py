"""
PDF to HTML conversion module.

This module provides functionality to convert Japanese PDF files to HTML format,
handling the conversion from right-to-left column layout to left-to-right row layout.
"""

import sys
import argparse
from typing import List, Dict, Optional
from pathlib import Path
import io

# PDF processing libraries
import fitz  # PyMuPDF
import pdfplumber
import pytesseract
from PIL import Image


class PDFTextBlock:
  """Represents a text block extracted from PDF with position information."""

  def __init__(self, text: str, x: float, y: float, width: float, height: float, page: int):
    self.text = text
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.page = page


class PDFImage:
  """Represents an image extracted from PDF."""

  def __init__(self, image_data: bytes, x: float, y: float, width: float, height: float, page: int):
    self.image_data = image_data
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.page = page


class PDFToHTMLConverter:
  """Main converter class for PDF to HTML conversion."""

  def __init__(self, input_pdf_path: str, output_html_path: str):
    self.input_pdf_path = Path(input_pdf_path)
    self.output_html_path = Path(output_html_path)
    self.text_blocks: List[PDFTextBlock] = []
    self.images: List[PDFImage] = []

    if not self.input_pdf_path.exists():
      raise FileNotFoundError(f"Input PDF file not found: {input_pdf_path}")

  def extract_text_with_positions(self) -> List[PDFTextBlock]:
    """Extract text blocks with position information from PDF."""
    text_blocks = []

    # First try traditional text extraction with pdfplumber
    with pdfplumber.open(self.input_pdf_path) as pdf:
      for page_num, page in enumerate(pdf.pages):
        # Extract text with bounding box information
        chars = page.chars
        if chars:
          # Group characters into text blocks
          # For now, we'll create a simple text block per line
          current_line = []
          current_y = None
          tolerance = 2  # pixels tolerance for same line

          for char in chars:
            if current_y is None:
              current_y = char['y0']
              current_line = [char]
            elif abs(char['y0'] - current_y) <= tolerance:
              current_line.append(char)
            else:
              # New line detected, process current line
              if current_line:
                text_blocks.append(self._create_text_block_from_chars(current_line, page_num))
              current_line = [char]
              current_y = char['y0']

          # Process the last line
          if current_line:
            text_blocks.append(self._create_text_block_from_chars(current_line, page_num))

    # If no text found, try OCR extraction
    if not text_blocks:
      text_blocks = self.extract_text_with_ocr()

    return text_blocks

  def extract_text_with_ocr(self) -> List[PDFTextBlock]:
    """Extract text blocks using OCR from PDF pages."""
    text_blocks = []
    
    doc = fitz.open(self.input_pdf_path)
    
    for page_num, page in enumerate(doc):
      # Get page as high-resolution image
      mat = fitz.Matrix(2, 2)  # 2x zoom for better OCR accuracy
      pix = page.get_pixmap(matrix=mat)
      img_data = pix.tobytes('png')
      
      # Convert to PIL Image
      img = Image.open(io.BytesIO(img_data))
      
      # Handle rotation - if page is rotated, rotate it back
      if page.rotation == 180:
        img = img.rotate(180, expand=True)
      elif page.rotation == 90:
        img = img.rotate(-90, expand=True)
      elif page.rotation == 270:
        img = img.rotate(90, expand=True)
      
      # Use OCR to extract text with position data
      try:
        # Get detailed OCR data with bounding boxes
        # Try Japanese OCR first
        ocr_data = pytesseract.image_to_data(img, lang='jpn', output_type=pytesseract.Output.DICT)
        
        # If Japanese OCR doesn't produce good results, try with English as fallback
        if not any(text.strip() for text in ocr_data['text']):
          ocr_data = pytesseract.image_to_data(img, lang='jpn+eng', output_type=pytesseract.Output.DICT)
        
        # Process OCR results and group into text blocks
        current_line_blocks = []
        current_line_y = None
        tolerance = 20  # pixels tolerance for same line
        
        for i, text in enumerate(ocr_data['text']):
          # Skip empty text
          if not text.strip():
            continue
            
          # Get position info (scale back from 2x zoom)
          conf = int(ocr_data['conf'][i])
          if conf < 30:  # Skip low confidence text
            continue
            
          x = ocr_data['left'][i] / 2  # Scale back from 2x zoom
          y = ocr_data['top'][i] / 2
          w = ocr_data['width'][i] / 2
          h = ocr_data['height'][i] / 2
          
          # Handle page rotation coordinate adjustment
          if page.rotation == 180:
            page_width = page.rect.width
            page_height = page.rect.height
            x = page_width - x - w
            y = page_height - y - h
          
          # Group into lines based on y-coordinate
          if current_line_y is None or abs(y - current_line_y) <= tolerance:
            current_line_blocks.append({
              'text': text,
              'x': x,
              'y': y,
              'width': w,
              'height': h
            })
            current_line_y = y if current_line_y is None else current_line_y
          else:
            # Process current line
            if current_line_blocks:
              line_text = ' '.join(block['text'] for block in current_line_blocks)
              # Sort blocks by x-coordinate and create text block
              current_line_blocks.sort(key=lambda b: b['x'])
              min_x = min(block['x'] for block in current_line_blocks)
              min_y = min(block['y'] for block in current_line_blocks)
              max_x = max(block['x'] + block['width'] for block in current_line_blocks)
              max_y = max(block['y'] + block['height'] for block in current_line_blocks)
              
              text_blocks.append(PDFTextBlock(
                line_text,
                min_x,
                min_y,
                max_x - min_x,
                max_y - min_y,
                page_num
              ))
            
            # Start new line
            current_line_blocks = [{
              'text': text,
              'x': x,
              'y': y,
              'width': w,
              'height': h
            }]
            current_line_y = y
        
        # Process the last line
        if current_line_blocks:
          line_text = ' '.join(block['text'] for block in current_line_blocks)
          current_line_blocks.sort(key=lambda b: b['x'])
          min_x = min(block['x'] for block in current_line_blocks)
          min_y = min(block['y'] for block in current_line_blocks)
          max_x = max(block['x'] + block['width'] for block in current_line_blocks)
          max_y = max(block['y'] + block['height'] for block in current_line_blocks)
          
          text_blocks.append(PDFTextBlock(
            line_text,
            min_x,
            min_y,
            max_x - min_x,
            max_y - min_y,
            page_num
          ))
        
      except Exception as e:
        print(f"OCR failed for page {page_num}: {e}")
        continue
    
    doc.close()
    return text_blocks

  def _create_text_block_from_chars(self, chars: List[Dict], page_num: int) -> PDFTextBlock:
    """Create a text block from a list of characters."""
    text = ''.join(char['text'] for char in chars)

    # Calculate bounding box
    x_coords = [char['x0'] for char in chars] + [char['x1'] for char in chars]
    y_coords = [char['y0'] for char in chars] + [char['y1'] for char in chars]

    x = min(x_coords)
    y = min(y_coords)
    width = max(x_coords) - x
    height = max(y_coords) - y

    return PDFTextBlock(text, x, y, width, height, page_num)

  def extract_images(self) -> List[PDFImage]:
    """Extract images from PDF."""
    images = []

    doc = fitz.open(self.input_pdf_path)

    for page_num, page in enumerate(doc):
      image_list = page.get_images()

      for img in image_list:
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

        # Get image position (approximate)
        image_rect = page.get_image_rects(img)[0] if page.get_image_rects(img) else None

        if image_rect:
          x, y, width, height = image_rect.x0, image_rect.y0, image_rect.width, image_rect.height
          
          # Adjust coordinates for rotation
          if page.rotation == 180:
            page_width = page.rect.width
            page_height = page.rect.height
            x = page_width - x - width
            y = page_height - y - height
        else:
          x, y, width, height = 0, 0, pix.width, pix.height

        images.append(PDFImage(img_data, x, y, width, height, page_num))
        pix = None

    doc.close()
    return images

  def convert_layout(self, text_blocks: List[PDFTextBlock]) -> List[PDFTextBlock]:
    """Convert Japanese right-to-left column layout to left-to-right row layout."""
    # Group text blocks by page
    pages = {}
    for block in text_blocks:
      if block.page not in pages:
        pages[block.page] = []
      pages[block.page].append(block)

    converted_blocks = []

    for page_num, blocks in pages.items():
      # Sort blocks by x-coordinate (right to left) then by y-coordinate (top to bottom)
      blocks.sort(key=lambda b: (-b.x, b.y))

      # Group blocks into columns based on x-coordinate
      columns = []
      current_column = []
      tolerance = 50  # pixels tolerance for same column

      for block in blocks:
        if not current_column:
          current_column = [block]
        elif abs(block.x - current_column[0].x) <= tolerance:
          current_column.append(block)
        else:
          if current_column:
            columns.append(sorted(current_column, key=lambda b: b.y))
          current_column = [block]

      if current_column:
        columns.append(sorted(current_column, key=lambda b: b.y))

      # Reverse column order for left-to-right reading
      columns.reverse()

      # Flatten columns back to blocks
      for column in columns:
        converted_blocks.extend(column)

    return converted_blocks

  def generate_html(self, text_blocks: List[PDFTextBlock], images: List[PDFImage]) -> str:
    """Generate HTML content from text blocks (images are ignored)."""
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted PDF</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
            background-color: white;
            color: black;
        }}
        .page {{
            margin-bottom: 50px;
            page-break-after: always;
            background-color: white;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .text-block {{
            margin-bottom: 10px;
            background-color: white;
        }}
        .image {{
            display: block;
            margin: 10px 0;
            background-color: white;
        }}
        h1 {{
            color: #333;
            background-color: white;
        }}
        h2 {{
            color: #333;
            background-color: white;
        }}
    </style>
</head>
<body>
    <h1>Converted PDF Content</h1>
    {content}
</body>
</html>"""

    # Group content by page
    pages = {}

    # Add text blocks
    for block in text_blocks:
      if block.page not in pages:
        pages[block.page] = {'text': []}
      pages[block.page]['text'].append(block)

    # Generate HTML content
    content_parts = []

    for page_num in sorted(pages.keys()):
      page_data = pages[page_num]
      content_parts.append(f'<div class="page" id="page-{page_num + 1}">')
      content_parts.append(f'<h2>Page {page_num + 1}</h2>')

      # Add text blocks
      for block in page_data['text']:
        if block.text.strip():
          content_parts.append(f'<div class="text-block">{block.text}</div>')

      content_parts.append('</div>')

    return html_template.format(content='\n'.join(content_parts))

  def convert(self) -> None:
    """Main conversion method."""
    print(f"Converting {self.input_pdf_path} to {self.output_html_path}")

    # Extract text with positions
    print("Extracting text...")
    self.text_blocks = self.extract_text_with_positions()
    print(f"Extracted {len(self.text_blocks)} text blocks")

    # Extract images
    print("Extracting images...")
    self.images = self.extract_images()
    print(f"Extracted {len(self.images)} images")

    # Convert layout
    print("Converting layout...")
    converted_text_blocks = self.convert_layout(self.text_blocks)

    # Generate HTML
    print("Generating HTML...")
    html_content = self.generate_html(converted_text_blocks, self.images)

    # Write HTML file
    self.output_html_path.parent.mkdir(parents=True, exist_ok=True)
    with open(self.output_html_path, 'w', encoding='utf-8') as f:
      f.write(html_content)

    print(f"Conversion complete! HTML file saved to {self.output_html_path}")


def main(argv: Optional[List[str]] = None) -> int:
  """Main entry point for the PDF to HTML converter."""
  parser = argparse.ArgumentParser(
    description="Convert Japanese PDF files to HTML format",
    prog="pdf_to_html"
  )

  parser.add_argument(
    "input_pdf",
    help="Path to the input PDF file"
  )

  parser.add_argument(
    "output_html",
    help="Path for the output HTML file"
  )

  parser.add_argument(
    "--verbose",
    "-v",
    action="store_true",
    help="Enable verbose output"
  )

  args = parser.parse_args(argv)

  try:
    converter = PDFToHTMLConverter(args.input_pdf, args.output_html)
    converter.convert()
    return 0
  except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
  sys.exit(main())
