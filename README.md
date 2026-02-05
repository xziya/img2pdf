# Image to PDF Converter

A simple and user-friendly tool to convert multiple JPG images to a single PDF file.

## Features

- **GUI Interface**: Uses macOS native file dialogs for easy file selection
- **Batch Processing**: Convert multiple images at once
- **Format Support**: Handles various image formats including JPG, PNG, BMP, and GIF
- **Automatic Mode Conversion**: Converts RGBA images to RGB for PDF compatibility
- **Permission Handling**: Automatically falls back to current directory if write permission is denied
- **Auto-open**: Opens the generated PDF file after conversion

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. **Clone or download this repository**

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Mode (Recommended)

Run the tool with:

```bash
python3 img2pdf.py
```

### Operation Steps

1. **Select Images**: A file dialog will appear. Select multiple images you want to convert. You can hold down the Command key (⌘) to select multiple files.

2. **Choose Output Location**: A save dialog will appear, defaulting to the current directory. Enter a name for your PDF file.

3. **Conversion**: The tool will process the images and create a PDF file.

4. **View Result**: The generated PDF file will automatically open in your default PDF viewer.

### Command-Line Mode

The tool also supports basic command-line usage:

```bash
python3 img2pdf.py [image1.jpg] [image2.jpg] ...
```

## Examples

### Basic Usage

Convert three images to a PDF file:

```bash
python3 img2pdf.py photo1.jpg photo2.jpg photo3.jpg
```

### Output Location

The PDF file will be saved to the current directory with the name you specified in the save dialog.

## Troubleshooting

### Permission Errors

If you encounter a "Permission denied" error, the tool will automatically fall back to saving the PDF file in the current directory.

### Image Format Issues

The tool automatically handles different image formats and modes. If an image is in RGBA mode (with transparency), it will be converted to RGB mode for PDF compatibility.

### Large Number of Images

The tool can handle a large number of images, but converting many high-resolution images may take some time. Please be patient during the conversion process.

## Dependencies

- **Pillow**: Python Imaging Library (PIL) fork for image processing

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please feel free to submit a pull request.
