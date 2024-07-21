import os
import io
import zlib
import lzma
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def compress_with_lzw(data):
    with io.BytesIO() as output:
        tiff_image = Image.fromarray(data)
        tiff_image.save(output, format='TIFF', compression='tiff_lzw')
        return output.getvalue()

def compress_with_deflate(data):
    return zlib.compress(data, level=9)

def compress_with_lzma(data):
    return lzma.compress(data)

def calculate_compression_ratio(original_size, compressed_size):
    return original_size / compressed_size if compressed_size != 0 else 0

def format_size(size):
    for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

def process_images(directory):
    filenames = []
    lzw_ratios = []
    deflate_ratios = []
    lzma_ratios = []

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            filepath = os.path.join(directory, filename)
            image = Image.open(filepath)
            original_size = os.path.getsize(filepath)

            # Extract RGB values as raw data
            rgb_data = np.array(image.convert('RGB'))
            raw_data = rgb_data.tobytes()

            # Kompression mit LZW
            lzw_compressed = compress_with_lzw(rgb_data)
            lzw_ratio = calculate_compression_ratio(len(raw_data), len(lzw_compressed))
            lzw_ratios.append(lzw_ratio)

            # Kompression mit DEFLATE
            deflate_compressed = compress_with_deflate(raw_data)
            deflate_ratio = calculate_compression_ratio(len(raw_data), len(deflate_compressed))
            deflate_ratios.append(deflate_ratio)

            # Kompression mit LZMA
            lzma_compressed = compress_with_lzma(raw_data)
            lzma_ratio = calculate_compression_ratio(len(raw_data), len(lzma_compressed))
            lzma_ratios.append(lzma_ratio)

            filenames.append(filename)
            print(f"Datei: {filename}")
            print(f"  Originalgröße: {format_size(original_size)}")
            print(f"  LZW komprimierte Größe: {format_size(len(lzw_compressed))}")
            print(f"  LZW Verdichtungsverhältnis: {lzw_ratio:.2f}")
            print(f"  DEFLATE komprimierte Größe: {format_size(len(deflate_compressed))}")
            print(f"  DEFLATE Verdichtungsverhältnis: {deflate_ratio:.2f}")
            print(f"  LZMA komprimierte Größe: {format_size(len(lzma_compressed))}")
            print(f"  LZMA Verdichtungsverhältnis: {lzma_ratio:.2f}")

    # Plotting the compression ratios for each file
    x = np.arange(len(filenames))
    width = 0.2

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(x - width, lzw_ratios, width, label='LZW', color='blue')
    ax.bar(x, deflate_ratios, width, label='DEFLATE', color='green')
    ax.bar(x + width, lzma_ratios, width, label='LZMA', color='red')

    ax.set_xlabel('Dateien')
    ax.set_ylabel('Verdichtungsverhältnis')
    ax.set_title('Verdichtungsverhältnisse der verschiedenen Kompressionsalgorithmen')
    ax.set_xticks(x)
    ax.set_xticklabels(filenames, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    directory = 'images'
    process_images(directory)
