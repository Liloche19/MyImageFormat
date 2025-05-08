#!/usr/bin/env python3

import sys

from src.PILImage import PILImage
from src.MyImage import MyImage

def main() -> int:
    if len(sys.argv) != 3:
        return 84
    original = PILImage()
    original.load(sys.argv[1])
    print("Original image loaded !")
    res = original.convert_to_my_image()
    print("Image converted !")
    res.save(sys.argv[2])
    print("Image saved !")
    res.display()
    print("Image displayed !")
    return 0

if __name__ == "__main__":
    sys.exit(main())
