"""
Test pic-extract functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path

from sensei.pic_extract import PDFImageExtractor, main


class TestPicExtract:
  """Test cases for pic-extract functionality."""

  def test_pdf_image_extractor_init(self):
    """Test PDFImageExtractor initialization."""
    sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'

    if not sample_pdf.exists():
      pytest.skip("Sample PDF not available")

    extractor = PDFImageExtractor(str(sample_pdf), "/tmp/test_output")
    assert extractor.input_pdf_path == sample_pdf
    assert extractor.output_prefix == "/tmp/test_output"

  def test_pdf_image_extractor_file_not_found(self):
    """Test PDFImageExtractor with non-existent file."""
    with pytest.raises(FileNotFoundError):
      PDFImageExtractor("non_existent_file.pdf", "/tmp/test_output")

  def test_extract_images_from_iai_tranomaki_jushinryu(self):
    """Test image extraction from iai_tranomaki_jushinryu.pdf."""
    sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'

    if not sample_pdf.exists():
      pytest.skip("Sample PDF not available")

    # Create temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
      output_prefix = os.path.join(temp_dir, "extracted_image")

      extractor = PDFImageExtractor(str(sample_pdf), output_prefix)
      output_files = extractor.extract_images()

      # Test that images were extracted
      assert len(output_files) > 0, "Should extract at least one image"

      # Test that all output files exist
      for file_path in output_files:
        assert os.path.exists(file_path), f"Output file should exist: {file_path}"

        # Test that files are PNG format
        assert file_path.endswith('.png'), f"Output file should be PNG: {file_path}"

        # Test that files have reasonable size (not empty)
        file_size = os.path.getsize(file_path)
        assert file_size > 1000, f"Output file should be reasonably sized: {file_path}"

  def test_extract_images_output_format(self):
    """Test that output files follow the expected naming format."""
    sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'

    if not sample_pdf.exists():
      pytest.skip("Sample PDF not available")

    # Create temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
      output_prefix = os.path.join(temp_dir, "my_prefix")

      extractor = PDFImageExtractor(str(sample_pdf), output_prefix)
      output_files = extractor.extract_images()

      # Test naming pattern
      for i, file_path in enumerate(output_files):
        expected_name = f"my_prefix_{i:03d}.png"
        expected_path = os.path.join(temp_dir, expected_name)
        assert file_path == expected_path, f"Output file name should follow pattern: {file_path}"

  def test_main_function(self):
    """Test main function with command line arguments."""
    sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'

    if not sample_pdf.exists():
      pytest.skip("Sample PDF not available")

    # Create temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
      output_prefix = os.path.join(temp_dir, "test_main")

      # Test successful execution
      result = main([str(sample_pdf), output_prefix])
      assert result == 0, "Main function should return 0 for successful execution"

      # Test that output files were created
      output_files = [f for f in os.listdir(temp_dir) if f.startswith("test_main") and f.endswith(".png")]
      assert len(output_files) > 0, "Main function should create output files"

  def test_main_function_with_verbose(self):
    """Test main function with verbose output."""
    sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'

    if not sample_pdf.exists():
      pytest.skip("Sample PDF not available")

    # Create temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
      output_prefix = os.path.join(temp_dir, "test_verbose")

      # Test successful execution with verbose flag
      result = main([str(sample_pdf), output_prefix, "--verbose"])
      assert result == 0, "Main function should return 0 for successful execution"

  def test_main_function_file_not_found(self):
    """Test main function with non-existent input file."""
    with tempfile.TemporaryDirectory() as temp_dir:
      output_prefix = os.path.join(temp_dir, "test_error")

      # Test error handling
      result = main(["non_existent_file.pdf", output_prefix])
      assert result == 1, "Main function should return 1 for error"

  def test_expected_number_of_images(self):
    """Test that the expected number of images are extracted from the sample PDF."""
    sample_pdf = Path(__file__).parent.parent / 'pdf' / 'input' / 'iai_tranomaki_jushinryu.pdf'

    if not sample_pdf.exists():
      pytest.skip("Sample PDF not available")

    # Create temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
      output_prefix = os.path.join(temp_dir, "expected_count")

      extractor = PDFImageExtractor(str(sample_pdf), output_prefix)
      output_files = extractor.extract_images()

      # Based on the issue description, we expect to extract 3 images
      # The PDF has 2 pages: page 1 with 1 picture, page 2 with 2 pictures
      assert len(output_files) == 3, f"Expected 3 images, but got {len(output_files)}"
