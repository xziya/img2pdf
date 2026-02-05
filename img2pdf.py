#!/usr/bin/env python3
"""
A tool to convert multiple JPG images to a single PDF file.
Supports both GUI and command-line modes.
"""

import os
import subprocess
import argparse
from PIL import Image


def convert_images_to_pdf(image_paths, output_pdf):
    """
    Convert multiple JPG images to a single PDF file.

    Args:
        image_paths (list): List of paths to JPG images
        output_pdf (str): Path to the output PDF file
    """
    if not image_paths:
        print("Error: No images provided")
        return

    try:
        # Open the first image to start the PDF
        first_image = Image.open(image_paths[0])

        # Convert to RGB mode if needed
        if first_image.mode == "RGBA":
            first_image = first_image.convert("RGB")

        # Collect remaining images
        other_images = []
        for image_path in image_paths[1:]:
            img = Image.open(image_path)
            if img.mode == "RGBA":
                img = img.convert("RGB")
            other_images.append(img)

        # Save as PDF
        first_image.save(output_pdf, save_all=True, append_images=other_images)
        print(f"Successfully converted {len(image_paths)} images to {output_pdf}")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def select_files():
    """
    Open file dialog to select multiple image files using macOS's native dialog.

    Returns:
        list: List of selected file paths
    """
    try:
        # Use AppleScript to open the file dialog
        script = """
        set theFiles to choose file with prompt "Select images to convert" of type {"public.image"} with multiple selections allowed
        set thePaths to ""
        repeat with aFile in theFiles
            set thePaths to thePaths & POSIX path of aFile & "|"
        end repeat
        return thePaths
        """
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True
        )
        if result.returncode == 0:
            # Process the result
            output = result.stdout.strip()
            if not output:
                return []

            # Split by | separator
            files = output.split("|")
            # Remove any empty strings
            files = [f.strip() for f in files if f.strip()]
            return files
        else:
            print(f"Error selecting files: {result.stderr}")
            return []
    except Exception as e:
        print(f"Error in file selection: {str(e)}")
        return []


def select_output_file(default_dir):
    """
    Open file dialog to select output PDF file path using macOS's native dialog.

    Args:
        default_dir: Default directory to open in the dialog

    Returns:
        str: Selected output file path
    """
    try:
        # Use AppleScript to open the save dialog
        script = f'''
        set defaultPath to POSIX file "{default_dir}"
        set theFile to choose file name with prompt "Save PDF as" default name "output.pdf" default location defaultPath
        return POSIX path of theFile
        '''
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Error selecting output file: {result.stderr}")
            return ""
    except Exception as e:
        print(f"Error in output file selection: {str(e)}")
        return ""


def check_write_permission(directory):
    """
    Check if the current user has write permission to the specified directory.

    Args:
        directory: Directory to check

    Returns:
        bool: True if write permission exists, False otherwise
    """
    try:
        # Create a temporary file to test write permission
        test_file = os.path.join(directory, ".test_write_permission.tmp")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        return True
    except:
        return False


def gui_mode():
    """
    Run the tool in GUI mode.
    """
    print("Image to PDF Converter")
    print("=====================")
    print()

    # Get current directory
    current_dir = os.getcwd()

    # Select image files
    print("Step 1: Select images to convert...")
    image_paths = select_files()

    if not image_paths:
        print("No images selected. Exiting...")
        return

    print(f"Selected {len(image_paths)} images:")
    for img_path in image_paths[:10]:  # Show first 10 images
        print(f"- {os.path.basename(img_path)}")
    if len(image_paths) > 10:
        print(f"... and {len(image_paths) - 10} more images")
    print()

    # Select output file
    print("Step 2: Select output PDF file...")
    output_pdf = select_output_file(current_dir)

    if not output_pdf:
        print("No output file selected. Exiting...")
        return

    # Ensure output file has .pdf extension
    if not output_pdf.lower().endswith(".pdf"):
        output_pdf += ".pdf"

    # Check write permission for the output directory
    output_dir = os.path.dirname(output_pdf)
    if not check_write_permission(output_dir):
        print(f"Error: No write permission to {output_dir}")
        print(f"Falling back to current directory: {current_dir}")
        # Use current directory with the same filename
        output_filename = os.path.basename(output_pdf)
        output_pdf = os.path.join(current_dir, output_filename)
        print(f"New output location: {output_pdf}")

    print(f"Output file: {output_pdf}")
    print()

    # Convert images to PDF
    print("Step 3: Converting images to PDF...")
    success = convert_images_to_pdf(image_paths, output_pdf)

    if success:
        print("\nConversion completed successfully!")
        print(f"Output PDF saved to: {output_pdf}")
        # Try to open the output PDF
        if os.name == "posix":
            try:
                subprocess.run(["open", output_pdf], check=True)
                print("Opening the output PDF file...")
            except:
                print(
                    "Could not open the output PDF automatically. Please open it manually."
                )
    else:
        print("\nConversion failed. Please check the error message above.")


def main():
    """
    Main function to handle both GUI and command-line modes.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Convert multiple images to a single PDF file"
    )
    parser.add_argument(
        "images", 
        nargs="*", 
        help="Path to image files (if not provided, GUI mode will be used)"
    )
    parser.add_argument(
        "-o", "--output", 
        default="output.pdf", 
        help="Output PDF file name (default: output.pdf)"
    )

    args = parser.parse_args()

    # Check if images were provided via command line
    if args.images:
        # Command-line mode
        print("Image to PDF Converter")
        print("=====================")
        print()

        # Validate input files
        valid_images = []
        for img_path in args.images:
            if os.path.exists(img_path):
                valid_images.append(img_path)
            else:
                print(f"Warning: File not found: {img_path}")

        if not valid_images:
            print("Error: No valid images provided")
            return

        # Get output path
        output_pdf = args.output
        if not output_pdf.lower().endswith(".pdf"):
            output_pdf += ".pdf"

        # Check write permission for the output directory
        output_dir = os.path.dirname(output_pdf) if os.path.dirname(output_pdf) else os.getcwd()
        current_dir = os.getcwd()

        if not check_write_permission(output_dir):
            print(f"Error: No write permission to {output_dir}")
            print(f"Falling back to current directory: {current_dir}")
            # Use current directory with the same filename
            output_filename = os.path.basename(output_pdf)
            output_pdf = os.path.join(current_dir, output_filename)
            print(f"New output location: {output_pdf}")

        print(f"Converting {len(valid_images)} images to {output_pdf}...")
        success = convert_images_to_pdf(valid_images, output_pdf)

        if success:
            print("\nConversion completed successfully!")
            print(f"Output PDF saved to: {output_pdf}")
            # Try to open the output PDF
            if os.name == "posix":
                try:
                    subprocess.run(["open", output_pdf], check=True)
                    print("Opening the output PDF file...")
                except:
                    print(
                        "Could not open the output PDF automatically. Please open it manually."
                    )
        else:
            print("\nConversion failed. Please check the error message above.")
    else:
        # GUI mode
        gui_mode()


if __name__ == "__main__":
    main()
