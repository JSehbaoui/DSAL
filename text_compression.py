import os
import zlib
import lzma
import matplotlib.pyplot as plt

class LZW:
    def compress(self, uncompressed):
        dict_size = 256
        dictionary = {chr(i): i for i in range(dict_size)}
        w = ""
        result = []
        for c in uncompressed:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                dictionary[wc] = dict_size
                dict_size += 1
                w = c
        if w:
            result.append(dictionary[w])
        return result

    def decompress(self, compressed):
        dict_size = 256
        dictionary = {i: chr(i) for i in range(dict_size)}
        result = []
        w = chr(compressed.pop(0))
        result.append(w)
        for k in compressed:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)
            result.append(entry)
            dictionary[dict_size] = w + entry[0]
            dict_size += 1
            w = entry
        return "".join(result)

def compress_with_lzw(text):
    lzw = LZW()
    compressed = lzw.compress(text)
    compressed_bytes = bytearray()
    for num in compressed:
        compressed_bytes.extend(num.to_bytes((num.bit_length() + 7) // 8, byteorder='big'))
    return compressed_bytes

def compress_with_deflate(text):
    compressed = zlib.compress(text.encode())
    return compressed

def compress_with_lzma(text):
    compressed = lzma.compress(text.encode())
    return compressed

def calculate_compression_ratio(original, compressed):
    return len(original) / len(compressed)

def format_size(size):
    # Formatiere die Dateigröße
    for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

def process_texts(directory):
    filenames = []
    lzw_ratios = []
    deflate_ratios = []
    lzma_ratios = []

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                text = (''.join(char for char in file.read() if ord(char) < 256)) * 10

            # Kompression mit LZW
            lzw_compressed = compress_with_lzw(text)
            lzw_ratio = calculate_compression_ratio(text.encode(), lzw_compressed)
            lzw_ratios.append(lzw_ratio)

            # Kompression mit DEFLATE
            deflate_compressed = compress_with_deflate(text)
            deflate_ratio = calculate_compression_ratio(text.encode(), deflate_compressed)
            deflate_ratios.append(deflate_ratio)

            # Kompression mit LZMA
            lzma_compressed = compress_with_lzma(text)
            lzma_ratio = calculate_compression_ratio(text.encode(), lzma_compressed)
            lzma_ratios.append(lzma_ratio)

            filenames.append(filename)
            original_size = len(text.encode())
            lzw_compressed_size = len(lzw_compressed)
            deflate_compressed_size = len(deflate_compressed)
            lzma_compressed_size = len(lzma_compressed)

            print(f"Datei: {filename}")
            print(f"  Originalgröße: {format_size(original_size)}")
            print(f"  LZW komprimierte Größe: {format_size(lzw_compressed_size)}")
            print(f"  LZW Verdichtungsverhältnis: {lzw_ratio:.2f}")
            print(f"  DEFLATE komprimierte Größe: {format_size(deflate_compressed_size)}")
            print(f"  DEFLATE Verdichtungsverhältnis: {deflate_ratio:.2f}")
            print(f"  LZMA komprimierte Größe: {format_size(lzma_compressed_size)}")
            print(f"  LZMA Verdichtungsverhältnis: {lzma_ratio:.2f}")

    # Plotting the compression ratios for each file
    x = range(len(filenames))
    width = 0.2

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar([i - width for i in x], lzw_ratios, width, label='LZW', color='blue')
    ax.bar(x, deflate_ratios, width, label='DEFLATE', color='green')
    ax.bar([i + width for i in x], lzma_ratios, width, label='LZMA', color='red') 

    ax.set_xlabel('Dateien')
    ax.set_ylabel('Verdichtungsverhältnis')
    ax.set_title('Verdichtungsverhältnisse der verschiedenen Kompressionsalgorithmen (TXT)')
    ax.set_xticks(x)
    ax.set_xticklabels(filenames, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    directory = 'texts'
    process_texts(directory)

