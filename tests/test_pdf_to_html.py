"""
Test suite for PDF to HTML conversion functionality.

This test suite focuses only on the real PDF file: pdf/input/iai_tranomaki_jushinryu.pdf
as requested in the issue to remove unrealistic test cases.
"""

import os
import sys
import pytest
import tempfile
import re
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sensei.pdf_to_html import (
  PDFToHTMLConverter,
  main
)


def test_iai_tranomaki_jushinryu_pdf_text_extraction():
  """Test Japanese text extraction from iai_tranomaki_jushinryu.pdf."""
  sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'

  if not sample_pdf.exists():
    pytest.skip("Sample PDF not available")

  with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_html:
    tmp_html_path = tmp_html.name

  try:
    converter = PDFToHTMLConverter(str(sample_pdf), tmp_html_path)

    # Test text extraction with OCR
    text_blocks = converter.extract_text_with_positions()
    assert isinstance(text_blocks, list)
    assert len(text_blocks) > 0, "Should extract text blocks from PDF"

    # Check that Japanese characters are being extracted
    japanese_chars = []
    for block in text_blocks:
      for char in block.text:
        if (ord(char) >= 0x3040 and ord(char) <= 0x309F) or \
           (ord(char) >= 0x30A0 and ord(char) <= 0x30FF) or \
           (ord(char) >= 0x4E00 and ord(char) <= 0x9FFF):
          japanese_chars.append(char)

    assert len(japanese_chars) > 0, "Should extract Japanese characters from PDF"
    print(f"Text extraction test passed: {len(text_blocks)} text blocks, {len(japanese_chars)} Japanese characters")

  finally:
    if os.path.exists(tmp_html_path):
      os.unlink(tmp_html_path)


def test_iai_tranomaki_jushinryu_pdf_image_extraction():
  """Test image extraction from iai_tranomaki_jushinryu.pdf."""
  sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'

  if not sample_pdf.exists():
    pytest.skip("Sample PDF not available")

  with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_html:
    tmp_html_path = tmp_html.name

  try:
    converter = PDFToHTMLConverter(str(sample_pdf), tmp_html_path)

    # Test image extraction
    images = converter.extract_images()
    assert isinstance(images, list)
    assert len(images) > 0, "Should extract images from PDF"

    # Test that images have valid properties
    for image in images:
      assert hasattr(image, 'image_data')
      assert hasattr(image, 'x')
      assert hasattr(image, 'y')
      assert hasattr(image, 'width')
      assert hasattr(image, 'height')
      assert hasattr(image, 'page')
      assert isinstance(image.image_data, bytes)
      assert len(image.image_data) > 0

    print(f"Image extraction test passed: {len(images)} images extracted")

  finally:
    if os.path.exists(tmp_html_path):
      os.unlink(tmp_html_path)


def test_iai_tranomaki_jushinryu_pdf_layout_conversion():
  """Test layout conversion from iai_tranomaki_jushinryu.pdf."""
  sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'

  if not sample_pdf.exists():
    pytest.skip("Sample PDF not available")

  with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_html:
    tmp_html_path = tmp_html.name

  try:
    converter = PDFToHTMLConverter(str(sample_pdf), tmp_html_path)

    # Extract text blocks
    text_blocks = converter.extract_text_with_positions()
    assert len(text_blocks) > 0, "Should have text blocks to convert"

    # Test layout conversion
    converted_blocks = converter.convert_layout(text_blocks)
    assert isinstance(converted_blocks, list)
    assert len(converted_blocks) == len(text_blocks), "Should preserve all text blocks"

    # Check that all blocks are properly structured
    for block in converted_blocks:
      assert hasattr(block, 'text')
      assert hasattr(block, 'x')
      assert hasattr(block, 'y')
      assert hasattr(block, 'width')
      assert hasattr(block, 'height')
      assert hasattr(block, 'page')

    print(f"Layout conversion test passed: {len(converted_blocks)} blocks converted")

  finally:
    if os.path.exists(tmp_html_path):
      os.unlink(tmp_html_path)


def test_iai_tranomaki_jushinryu_pdf_full_conversion():
  """Test full PDF to HTML conversion for iai_tranomaki_jushinryu.pdf."""
  sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'

  if not sample_pdf.exists():
    pytest.skip("Sample PDF not available")

  with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_html:
    tmp_html_path = tmp_html.name

  try:
    converter = PDFToHTMLConverter(str(sample_pdf), tmp_html_path)

    # Perform full conversion
    converter.convert()

    # Verify output file exists
    assert os.path.exists(tmp_html_path), "HTML output file should be created"

    # Read and verify HTML content
    with open(tmp_html_path, 'r', encoding='utf-8') as f:
      html_content = f.read()

    # Test 1: HTML should contain Japanese text
    japanese_chars = []
    for char in html_content:
      if (ord(char) >= 0x3040 and ord(char) <= 0x309F) or \
         (ord(char) >= 0x30A0 and ord(char) <= 0x30FF) or \
         (ord(char) >= 0x4E00 and ord(char) <= 0x9FFF):
        japanese_chars.append(char)

    assert len(japanese_chars) > 0, "HTML should contain Japanese characters"

    # Test 2: HTML structure should be correct
    assert '<!DOCTYPE html>' in html_content, "HTML should have proper DOCTYPE"
    assert '<html lang="en">' in html_content, "HTML should have language attribute"
    assert '</html>' in html_content, "HTML should be properly closed"
    assert '<title>Converted PDF</title>' in html_content, "HTML should have title"

    # Test 3: HTML should have white background
    assert 'background-color: white' in html_content, "HTML should have white background"

    # Test 4: HTML should NOT contain embedded images (per requirements)
    assert 'data:image/png;base64,' not in html_content, "HTML should not contain embedded images"

    # Test 5: HTML should contain page structure
    assert 'Page 1' in html_content, "HTML should contain Page 1"
    assert 'Page 2' in html_content, "HTML should contain Page 2"

    # Test 6: HTML should contain text blocks
    text_blocks = re.findall(r'<div class="text-block">(.*?)</div>', html_content)
    assert len(text_blocks) > 0, "HTML should contain text blocks"

    # Test 7: Text blocks should contain Japanese content
    japanese_text_blocks = []
    for block in text_blocks:
      for char in block:
        if (ord(char) >= 0x3040 and ord(char) <= 0x309F) or \
           (ord(char) >= 0x30A0 and ord(char) <= 0x30FF) or \
           (ord(char) >= 0x4E00 and ord(char) <= 0x9FFF):
          japanese_text_blocks.append(block)
          break

    assert len(japanese_text_blocks) > 0, "Should have text blocks with Japanese characters"

    print(f"Full conversion test passed: {len(japanese_chars)} Japanese characters in {len(text_blocks)} text blocks")

  finally:
    if os.path.exists(tmp_html_path):
      os.unlink(tmp_html_path)


def test_main_function_with_iai_tranomaki_jushinryu_pdf():
  """Test main function with iai_tranomaki_jushinryu.pdf."""
  sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'

  if not sample_pdf.exists():
    pytest.skip("Sample PDF not available")

  with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_html:
    tmp_html_path = tmp_html.name

  try:
    # Test successful conversion
    result = main([str(sample_pdf), tmp_html_path])
    assert result == 0, "Main function should return 0 for successful conversion"

    # Verify output file exists and contains Japanese characters
    assert os.path.exists(tmp_html_path), "HTML output file should be created"

    with open(tmp_html_path, 'r', encoding='utf-8') as f:
      html_content = f.read()

    japanese_chars = []
    for char in html_content:
      if (ord(char) >= 0x3040 and ord(char) <= 0x309F) or \
         (ord(char) >= 0x30A0 and ord(char) <= 0x30FF) or \
         (ord(char) >= 0x4E00 and ord(char) <= 0x9FFF):
        japanese_chars.append(char)

    assert len(japanese_chars) > 0, "Main function should produce HTML with Japanese characters"

    print(f"Main function test passed: {len(japanese_chars)} Japanese characters extracted")

  finally:
    if os.path.exists(tmp_html_path):
      os.unlink(tmp_html_path)


def test_main_function_error_handling():
  """Test main function error handling."""
  # Test with non-existent file
  result = main(['nonexistent.pdf', 'output.html'])
  assert result == 1, "Main function should return 1 for file not found error"

  # Test with missing arguments
  with pytest.raises(SystemExit) as exc_info:
    main([])
  assert exc_info.value.code == 2, "Main function should exit with code 2 for missing arguments"

  # Test with help argument
  with pytest.raises(SystemExit) as exc_info:
    main(['--help'])
  assert exc_info.value.code == 0, "Main function should exit with code 0 for help"