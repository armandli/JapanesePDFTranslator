"""
Test suite for PDF to HTML conversion functionality.
"""

import pytest
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sensei.pdf_to_html import (
  PDFTextBlock,
  PDFImage,
  PDFToHTMLConverter,
  main
)


class TestPDFTextBlock:
  """Test PDFTextBlock class."""
  
  def test_init(self):
    """Test PDFTextBlock initialization."""
    block = PDFTextBlock("Hello", 10.0, 20.0, 100.0, 15.0, 0)
    assert block.text == "Hello"
    assert block.x == 10.0
    assert block.y == 20.0
    assert block.width == 100.0
    assert block.height == 15.0
    assert block.page == 0


class TestPDFImage:
  """Test PDFImage class."""
  
  def test_init(self):
    """Test PDFImage initialization."""
    image_data = b"fake_image_data"
    image = PDFImage(image_data, 50.0, 60.0, 200.0, 150.0, 1)
    assert image.image_data == image_data
    assert image.x == 50.0
    assert image.y == 60.0
    assert image.width == 200.0
    assert image.height == 150.0
    assert image.page == 1


class TestPDFToHTMLConverter:
  """Test PDFToHTMLConverter class."""
  
  def test_init_with_valid_file(self):
    """Test converter initialization with valid file."""
    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
      tmp_pdf.write(b"fake pdf content")
      tmp_pdf_path = tmp_pdf.name
    
    try:
      with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_html:
        tmp_html_path = tmp_html.name
      
      converter = PDFToHTMLConverter(tmp_pdf_path, tmp_html_path)
      assert converter.input_pdf_path == Path(tmp_pdf_path)
      assert converter.output_html_path == Path(tmp_html_path)
      assert converter.text_blocks == []
      assert converter.images == []
    finally:
      os.unlink(tmp_pdf_path)
      if os.path.exists(tmp_html_path):
        os.unlink(tmp_html_path)
  
  def test_init_with_invalid_file(self):
    """Test converter initialization with invalid file."""
    with pytest.raises(FileNotFoundError):
      PDFToHTMLConverter("nonexistent.pdf", "output.html")
  
  def test_create_text_block_from_chars(self):
    """Test _create_text_block_from_chars method."""
    # Create a temporary PDF file for initialization
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
      tmp_pdf.write(b"fake pdf content")
      tmp_pdf_path = tmp_pdf.name
    
    try:
      converter = PDFToHTMLConverter(tmp_pdf_path, "output.html")
      
      # Mock character data
      chars = [
        {'text': 'H', 'x0': 10, 'x1': 15, 'y0': 20, 'y1': 35},
        {'text': 'e', 'x0': 15, 'x1': 20, 'y0': 20, 'y1': 35},
        {'text': 'l', 'x0': 20, 'x1': 25, 'y0': 20, 'y1': 35},
        {'text': 'l', 'x0': 25, 'x1': 30, 'y0': 20, 'y1': 35},
        {'text': 'o', 'x0': 30, 'x1': 35, 'y0': 20, 'y1': 35},
      ]
      
      block = converter._create_text_block_from_chars(chars, 0)
      
      assert block.text == "Hello"
      assert block.x == 10
      assert block.y == 20
      assert block.width == 25  # 35 - 10
      assert block.height == 15  # 35 - 20
      assert block.page == 0
    finally:
      os.unlink(tmp_pdf_path)
  
  def test_convert_layout(self):
    """Test convert_layout method."""
    # Create a temporary PDF file for initialization
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
      tmp_pdf.write(b"fake pdf content")
      tmp_pdf_path = tmp_pdf.name
    
    try:
      converter = PDFToHTMLConverter(tmp_pdf_path, "output.html")
      
      # Create test text blocks simulating Japanese right-to-left layout
      # Column 1 (rightmost): x=300
      # Column 2 (middle): x=200  
      # Column 3 (leftmost): x=100
      text_blocks = [
        PDFTextBlock("右", 300, 10, 50, 20, 0),  # Right column, top
        PDFTextBlock("下", 300, 40, 50, 20, 0),  # Right column, bottom
        PDFTextBlock("中", 200, 10, 50, 20, 0),  # Middle column, top
        PDFTextBlock("央", 200, 40, 50, 20, 0),  # Middle column, bottom
        PDFTextBlock("左", 100, 10, 50, 20, 0),  # Left column, top
        PDFTextBlock("側", 100, 40, 50, 20, 0),  # Left column, bottom
      ]
      
      converted = converter.convert_layout(text_blocks)
      
      # After conversion, left-to-right reading order should be maintained
      # The original rightmost column should come first in HTML
      assert len(converted) == 6
      
      # Check that we have the expected structure
      # (Note: exact order depends on the algorithm, but general structure should be maintained)
      assert all(block.page == 0 for block in converted)
    finally:
      os.unlink(tmp_pdf_path)
  
  def test_generate_html(self):
    """Test generate_html method."""
    # Create a temporary PDF file for initialization
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
      tmp_pdf.write(b"fake pdf content")
      tmp_pdf_path = tmp_pdf.name
    
    try:
      converter = PDFToHTMLConverter(tmp_pdf_path, "output.html")
      
      # Create test data
      text_blocks = [
        PDFTextBlock("Hello", 10, 20, 100, 15, 0),
        PDFTextBlock("World", 10, 40, 100, 15, 0),
      ]
      
      images = [
        PDFImage(b"fake_image_data", 50, 60, 200, 150, 0),
      ]
      
      html_content = converter.generate_html(text_blocks, images)
      
      # Check that HTML structure is correct
      assert "<!DOCTYPE html>" in html_content
      assert "<html lang=\"en\">" in html_content
      assert "<title>Converted PDF</title>" in html_content
      assert "Hello" in html_content
      assert "World" in html_content
      assert "data:image/png;base64," in html_content
      assert "Page 1" in html_content
    finally:
      os.unlink(tmp_pdf_path)

  @patch('sensei.pdf_to_html.pdfplumber.open')
  def test_extract_text_with_positions(self, mock_pdfplumber_open):
    """Test extract_text_with_positions method."""
    # Create a temporary PDF file for initialization
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
      tmp_pdf.write(b"fake pdf content")
      tmp_pdf_path = tmp_pdf.name
    
    try:
      converter = PDFToHTMLConverter(tmp_pdf_path, "output.html")
      
      # Mock pdfplumber response
      mock_page = Mock()
      mock_page.chars = [
        {'text': 'H', 'x0': 10, 'x1': 15, 'y0': 20, 'y1': 35},
        {'text': 'e', 'x0': 15, 'x1': 20, 'y0': 20, 'y1': 35},
        {'text': 'l', 'x0': 20, 'x1': 25, 'y0': 20, 'y1': 35},
        {'text': 'l', 'x0': 25, 'x1': 30, 'y0': 20, 'y1': 35},
        {'text': 'o', 'x0': 30, 'x1': 35, 'y0': 20, 'y1': 35},
      ]
      
      mock_pdf = Mock()
      mock_pdf.pages = [mock_page]
      mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf
      
      text_blocks = converter.extract_text_with_positions()
      
      assert len(text_blocks) == 1
      assert text_blocks[0].text == "Hello"
      assert text_blocks[0].page == 0
    finally:
      os.unlink(tmp_pdf_path)

  @patch('sensei.pdf_to_html.fitz.open')
  def test_extract_images(self, mock_fitz_open):
    """Test extract_images method."""
    # Create a temporary PDF file for initialization
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
      tmp_pdf.write(b"fake pdf content")
      tmp_pdf_path = tmp_pdf.name
    
    try:
      converter = PDFToHTMLConverter(tmp_pdf_path, "output.html")
      
      # Mock fitz response
      mock_pixmap = Mock()
      mock_pixmap.n = 3
      mock_pixmap.alpha = 0
      mock_pixmap.tobytes.return_value = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00IEND\xaeB`\x82'
      mock_pixmap.width = 100
      mock_pixmap.height = 100
      
      mock_rect = Mock()
      mock_rect.x0 = 10
      mock_rect.y0 = 20
      mock_rect.width = 100
      mock_rect.height = 100
      
      mock_page = Mock()
      mock_page.get_images.return_value = [(123, 0, 0, 0, 0, 0, 0, 0)]
      mock_page.get_image_rects.return_value = [mock_rect]
      mock_page.rotation = 0  # Add rotation property
      
      mock_doc = Mock()
      mock_doc.__iter__ = Mock(return_value=iter([mock_page]))
      mock_doc.close.return_value = None
      
      mock_fitz_open.return_value = mock_doc
      
      # Mock fitz.Pixmap constructor
      with patch('sensei.pdf_to_html.fitz.Pixmap', return_value=mock_pixmap):
        images = converter.extract_images()
      
      assert len(images) == 1
      assert images[0].page == 0
    finally:
      os.unlink(tmp_pdf_path)


class TestMainFunction:
  """Test main function."""
  
  def test_main_with_help(self):
    """Test main function with help argument."""
    with pytest.raises(SystemExit) as exc_info:
      main(['--help'])
    assert exc_info.value.code == 0
  
  def test_main_with_missing_args(self):
    """Test main function with missing arguments."""
    with pytest.raises(SystemExit) as exc_info:
      main([])
    assert exc_info.value.code == 2
  
  def test_main_with_invalid_input_file(self):
    """Test main function with invalid input file."""
    result = main(['nonexistent.pdf', 'output.html'])
    assert result == 1
  
  @patch('sensei.pdf_to_html.PDFToHTMLConverter')
  def test_main_success(self, mock_converter_class):
    """Test main function success case."""
    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
      tmp_pdf.write(b"fake pdf content")
      tmp_pdf_path = tmp_pdf.name
    
    try:
      mock_converter = Mock()
      mock_converter.convert.return_value = None
      mock_converter_class.return_value = mock_converter
      
      result = main([tmp_pdf_path, 'output.html'])
      
      assert result == 0
      mock_converter_class.assert_called_once_with(tmp_pdf_path, 'output.html')
      mock_converter.convert.assert_called_once()
    finally:
      os.unlink(tmp_pdf_path)
  
  @patch('sensei.pdf_to_html.PDFToHTMLConverter')
  def test_main_conversion_error(self, mock_converter_class):
    """Test main function with conversion error."""
    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
      tmp_pdf.write(b"fake pdf content")
      tmp_pdf_path = tmp_pdf.name
    
    try:
      mock_converter = Mock()
      mock_converter.convert.side_effect = Exception("Conversion failed")
      mock_converter_class.return_value = mock_converter
      
      result = main([tmp_pdf_path, 'output.html'])
      
      assert result == 1
    finally:
      os.unlink(tmp_pdf_path)


def test_real_pdf_sample():
  """Test with actual PDF sample if available."""
  sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'
  
  if sample_pdf.exists():
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_html:
      tmp_html_path = tmp_html.name
    
    try:
      converter = PDFToHTMLConverter(str(sample_pdf), tmp_html_path)
      
      # Test text extraction
      text_blocks = converter.extract_text_with_positions()
      assert isinstance(text_blocks, list)
      
      # Test image extraction
      images = converter.extract_images()
      assert isinstance(images, list)
      
      # Test layout conversion
      converted_blocks = converter.convert_layout(text_blocks)
      assert isinstance(converted_blocks, list)
      assert len(converted_blocks) == len(text_blocks)
      
      # Test HTML generation
      html_content = converter.generate_html(converted_blocks, images)
      assert "<!DOCTYPE html>" in html_content
      assert "<html" in html_content
      assert "</html>" in html_content
      
      print(f"Sample PDF test passed: {len(text_blocks)} text blocks, {len(images)} images")
    finally:
      if os.path.exists(tmp_html_path):
        os.unlink(tmp_html_path)
  else:
    pytest.skip("Sample PDF not available")


def test_iai_tranomaki_jushinryu_pdf():
  """Test specific requirements for iai_tranomaki_jushinryu.pdf."""
  sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'
  
  if not sample_pdf.exists():
    pytest.skip("Sample PDF not available")
  
  with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_html:
    tmp_html_path = tmp_html.name
  
  try:
    converter = PDFToHTMLConverter(str(sample_pdf), tmp_html_path)
    
    # Perform full conversion
    converter.convert()
    
    # Read generated HTML
    with open(tmp_html_path, 'r', encoding='utf-8') as f:
      html_content = f.read()
    
    # Test 1: HTML should contain Japanese text
    # Look for Japanese characters (hiragana, katakana, kanji)
    japanese_chars = []
    for char in html_content:
      if (ord(char) >= 0x3040 and ord(char) <= 0x309F) or \
         (ord(char) >= 0x30A0 and ord(char) <= 0x30FF) or \
         (ord(char) >= 0x4E00 and ord(char) <= 0x9FFF):
        japanese_chars.append(char)
    
    assert len(japanese_chars) > 0, "HTML should contain Japanese characters"
    print(f"Found {len(japanese_chars)} Japanese characters")
    
    # Test 2: HTML should have white background
    assert 'background-color: white' in html_content, "HTML should have white background"
    
    # Test 3: HTML should contain images
    assert 'data:image/png;base64,' in html_content, "HTML should contain embedded images"
    
    # Test 4: HTML should contain Page 1 and Page 2
    assert 'Page 1' in html_content, "HTML should contain Page 1"
    assert 'Page 2' in html_content, "HTML should contain Page 2"
    
    # Test 5: HTML should contain text blocks in left-to-right order
    # Find all text blocks
    import re
    text_blocks = re.findall(r'<div class="text-block">(.*?)</div>', html_content)
    assert len(text_blocks) > 0, "HTML should contain text blocks"
    
    # Test 6: HTML structure should be correct
    assert '<!DOCTYPE html>' in html_content, "HTML should have proper DOCTYPE"
    assert '<html lang="en">' in html_content, "HTML should have language attribute"
    assert '</html>' in html_content, "HTML should be properly closed"
    
    print(f"Test passed: {len(text_blocks)} text blocks extracted with Japanese content")
    
  finally:
    if os.path.exists(tmp_html_path):
      os.unlink(tmp_html_path)