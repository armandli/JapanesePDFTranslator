# Japanese PDF Translator

Translate Japanese PDF magazines to English while retaining magazine format.

## Features

- Extract text from Japanese PDF files
- Translate Japanese text to English using multiple translation services
- Preserve original PDF formatting and layout
- Generate HTML output with preserved formatting
- Interactive development environment using Marimo notebooks

## Installation

1. Clone the repository:
```bash
git clone https://github.com/armandli/JapanesePDFTranslator.git
cd JapanesePDFTranslator
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

Or use the Makefile:
```bash
make venv
source venv/bin/activate
make install
```

## Usage

### Command Line Interface

```bash
japanese-pdf-translator input.pdf --output output.pdf --verbose
```

### Interactive Development

Use Marimo notebooks for interactive development:

```bash
marimo edit notebook/demo.py
```

## Project Structure

```
JapanesePDFTranslator/
├── sensei/                 # Main source code
│   ├── __init__.py
│   └── cli.py
├── notebook/               # Marimo notebooks
│   ├── demo.py
│   └── README.md
├── pdf/                    # PDF files
│   ├── input/              # Input Japanese PDFs
│   ├── output/             # Translated English PDFs
│   ├── samples/            # Sample files for testing
│   └── README.md
├── tests/                  # Unit tests
│   ├── __init__.py
│   └── test_basic.py
├── requirements.txt        # Dependencies
├── requirements-dev.txt    # Development dependencies
├── setup.py               # Package setup
├── pyproject.toml         # Tool configuration
├── Makefile              # Build automation
└── README.md             # This file
```

## Dependencies

### Core Dependencies
- **marimo**: Python notebook package for interactive development
- **pypdf**: Modern PDF processing library
- **pdfplumber**: PDF text extraction
- **PyMuPDF**: Comprehensive PDF library
- **googletrans**: Google Translate API wrapper
- **deep-translator**: Multiple translation services
- **openai**: OpenAI API for advanced translation
- **beautifulsoup4**: HTML parsing and processing
- **lxml**: Fast XML/HTML parser
- **html5lib**: Standards-compliant HTML parser

### Development Dependencies
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Type checking
- **isort**: Import sorting

## Development

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
pytest tests/ --cov=sensei --cov-report=html
```

### Code Formatting

```bash
# Format code
make format

# Check linting
make lint
```

### Building

```bash
# Clean build artifacts
make clean

# Install in development mode
make install-dev
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper tests
4. Ensure code follows 2-space indentation
5. Submit a pull request
