# __MyImageFormat (v0)__
---
## __How is my image format working ?__

### __The output file looks like this:__

- MAGIC_NUMBER (8 bytes)
- VERSION (1 byte)
- HEADER_SIZE (4 bytes)
- IMAGE_WIDTH (4 bytes)
- IMAGE_HEIGHT (4 bytes)
- BYTES_PER_PIXELS (1 byte)
- PIXELS (IMAGE_WIDTH * IMAGE_HEIGHT * BYTES_PER_PIXELS bytes) (RGBA format)
- END_OF_FILE (3 bytes)

### Values:

- MAGIC_NUMBER = "42424242"
- VERSION = 0 (In v0)
- HEADER_SIZE = 9 (In v0)
- END_OF_FILE = "EOF" (In v0)
