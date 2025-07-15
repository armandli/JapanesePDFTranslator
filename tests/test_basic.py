"""
Test configuration and basic tests for Japanese PDF Translator.
"""

import pytest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_import_sensei():
  """Test that the sensei package can be imported."""
  try:
    import sensei
    assert hasattr(sensei, '__version__')
    assert hasattr(sensei, '__author__')
  except ImportError:
    pytest.fail("Could not import sensei package")

def test_version():
  """Test that version is properly set."""
  import sensei
  assert sensei.__version__ == "0.1.0"

def test_author():
  """Test that author is properly set."""
  import sensei
  assert sensei.__author__ == "Armand Li"