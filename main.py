#!/usr/bin/env python3

from PIL import Image
import sys
import struct

MAGIC = "42424242"
VERSION = 0
HEADER_SIZE = 9
PIXEL_FORMAT = "RGBA"
END_OF_FILE = "EOF"

class PILImage():

    def __init__(self):
        self.height: int = 0
        self.width: int = 0
        return

    def load(self, filename: str):
        self.image = Image.open(filename).convert(PIXEL_FORMAT)
        self.width, self.hight = self.image.size
        return

    def convert_to_my_image(self):
        new: MyImage = MyImage()
        new.array = [[] for i in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                pixel = self.image.getpixel((j, i))
                new.array[i].append(pixel)
        return new

    def display(self) -> None:
        if not self.image:
            print("Image not loaded !")
            return
        self.image.show()
        return

    def save(self, filename: str) -> None:
        self.image.save(filename)
        return

class MyImage():
    def __init__(self):
        self.input_name: str = ""
        self.output_name: str = ""
        self.image_file = None
        self.image = None
        self.array: list[list] = []
        self.height: int = 0
        self.width: int = 0
        self.bpp: int = 0
        if PIXEL_FORMAT == "RGBA":
            self.bpp: int = 4
        return

    def load(self, filename):
        self.input_name = filename
        with open(self.input_name, "rb") as file:
            data = file.read()
        magic = data[:8].decode("ascii")
        if magic != MAGIC:
            print("The file seems not to be a MyImageFormat file !")
            return
        version = data[8:9]
        version = struct.unpack('B', version)[0]
        if version > VERSION:
            print("The file format seems not to be correct !")
            return
        header_size = data[9:13]
        header_size = struct.unpack('I', header_size)[0]
        if header_size != HEADER_SIZE:
            print("The size of the header seems not to be correct !")
            return
        width = data[13:17]
        width = struct.unpack('I', width)[0]
        self.width = width
        height = data[17:21]
        height = struct.unpack('I', height)[0]
        self.height = height
        bpp = data[21:22]
        bpp = struct.unpack('B', bpp)[0]
        self.bpp = bpp
        self.array = []
        print(f"Height {height}, Width {width}, bpp {bpp}")
        for i in range(height):
            self.array.append([])
            for j in range(width):
                index = 22 + i * width * 4 + j * 4
                red = data[index:index+1]
                red = struct.unpack('B', red)[0]
                green = data[index+1:index+2]
                green = struct.unpack('B', green)[0]
                blue = data[index+2:index+3]
                blue = struct.unpack('B', blue)[0]
                alpha = data[index+3:index+4]
                alpha = struct.unpack('B', alpha)[0]
                self.array[i].append((red, green, blue, alpha))
        return

    def save(self, output_name: str):
        self.output_name = output_name
        with open(self.output_name, "wb") as file:
            file.write(MAGIC.encode("ascii"))
            file.write(VERSION.to_bytes(1, byteorder="little"))
            file.write(HEADER_SIZE.to_bytes(4, byteorder="little"))
            file.write(self.width.to_bytes(4, byteorder="little"))
            file.write(self.height.to_bytes(4, byteorder="little"))
            file.write(self.bpp.to_bytes(1, byteorder="little"))
            for i in range(self.height):
                for j in range(self.width):
                    r, g, b, a = self.array[i][j]
                    file.write(r.to_bytes(1, byteorder="little"))
                    file.write(g.to_bytes(1, byteorder="little"))
                    file.write(b.to_bytes(1, byteorder="little"))
                    file.write(a.to_bytes(1, byteorder="little"))
            file.write(END_OF_FILE.encode("ascii"))
        return

    def convert_to_pil_image(self) -> PILImage:
        new = PILImage()
        new.image = Image.new(PIXEL_FORMAT, (self.width, self.height))
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.array[y][x]
                new.image.putpixel((x, y), pixel)
        new.height = self.height
        new.width = self.width
        return new

    def display(self) -> None:
        pil: PILImage = self.convert_to_pil_image()
        pil.image.show()
        return

def main() -> int:
    return 0

if __name__ == "__main__":
    sys.exit(main())
