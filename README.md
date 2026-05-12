# BadFS: A Simple Filesystem Implementation

BadFS is a basic filesystem implementation. It provides a simple interface for managing up to 32 files, each limited to 512 bytes of data.

## Overview

BadFS uses a fixed-size disk image divided into 512-byte sectors. The filesystem supports:
- Up to 32 files
- File names up to 15 characters (null-terminated)
- File sizes up to 512 bytes each
- No directory structure (flat filesystem)
- No metadata beyond file names

## Disk Layout

The disk image is structured as follows:

- **Sector 0**: Reserved (unused)
- **Sector 1**: File allocation table (FAT) - 512 bytes containing 32 file names (16 bytes each)
- **Sectors 2-33**: File data storage (32 sectors, one per file)

## API Reference

#### `read(index: int) -> bytes`
Reads data from a file.
- `index`: File index (0-31)
- Returns: 512 bytes of file data

#### `write(index: int, data: bytearray | bytes)`
Writes data to a file. Data is truncated to 512 bytes if longer, or padded with zeros if shorter.
- `index`: File index (0-31)
- `data`: Data to write

#### `delete(index: int) -> bool`
Deletes a file by clearing its name in the table.
- `index`: File index (0-31)
- Returns: Always True

#### `list() -> list[str]`
Returns the current file allocation table.
- Returns: List of 32 strings (file names or empty strings)

#### `find(name: str) -> int | None`
Finds the index of a file by name.
- `name`: File name to search for
- Returns: File index (0-31) or None if not found

#### `add_file(name: str) -> int | bool`
Adds a new file to the first available slot.
- `name`: File name (up to 15 characters)
- Returns: File index (0-31) on success, False if no slots available

## Usage Example

```python
from io import BufferedRandom
import os

# Create or open a disk image
if not os.path.isfile("disk.img"):
    with open("disk.img", "wb+") as f:
        f.write(bytes(512 * 33))  # Initialize 33 sectors

disk = open("disk.img", "rb+")
fs = BadFS(disk)

# Add a file
index = fs.add_file("example.txt")
if index is not False:
    fs.write(index, b"Hello, World!")

# Read a file
data = fs.read(index)
print(data.decode())

# List files
files = [name for name in fs.list() if name]
print("Files:", files)

# Delete a file
fs.delete(index)

disk.close()
```

## Interactive Testing

The module includes an interactive shell for testing. Run the script directly:

```bash
python main.py
```

Available commands:
- `ls`: List all files
- `cat <filename>`: Display file contents
- `rm <filename>`: Delete a file
- `touch <filename>`: Create/update a file with text input
- `import <source_file> <dest_name>`: Import a file from disk
- `export <source_name> <dest_file>`: Export a file to disk
- `exit`: Quit the interactive shell

## Limitations

- Maximum 32 files
- File names limited to 15 characters
- Files limited to 512 bytes each
- No subdirectories
- No file metadata (timestamps, permissions, etc.)
- No error handling for disk I/O failures
- Simple allocation strategy

## Dependencies

- Python 3.x
- Standard library only (io, struct, shlex, os)

## License

This is a prototype implementation for "educational purposes."
