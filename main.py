#!/usr/bin/env python3

from PIL import Image
import sys
import struct

MAGIC = "42424242"
VERSION = 0
HEADER_SIZE = 9
PIXEL_FORMAT = "RGBA"
END_OF_FILE = "EOF"

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

    def load(self, filename: str):
        if self.input_name != "":
            print("Image already loaded !")
            return
        self.input_name = filename
        self.image_file = Image.open(self.input_name)
        self.image = self.image_file.convert(PIXEL_FORMAT)
        self.width, self.height = self.image.size
        return

    def my_load(self, filename):
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

    def create_array(self):
        if self.image == None:
            print("Image not loaded !")
            return None
        self.array = [[] for i in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                pixel = self.image.getpixel((j, i))
                self.array[i].append(pixel)
        return self.array

    def display(self):
        if self.array == [[]]:
            print("The image is not loaded !")
            return
        print_image = Image.new(PIXEL_FORMAT, (self.width, self.height))
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.array[y][x]
                print_image.putpixel((x, y), pixel)
        print_image.show()
        return

    def my_save(self, output_name: str):
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

    def save(self, output_name: str):
        self.output_name = output_name
        save = Image.new(PIXEL_FORMAT, (self.width, self.height))
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.array[y][x]
                save.putpixel((x, y), pixel)
        save.save(self.output_name)
        return


def main() -> int:
    argv = sys.argv
    argc = len(argv)
    if argc != 3:
        print("Invalid number of arguments !")
        sys.exit(84)
    array = MyImage()
    array.my_load(argv[1])
    array.display()
    return 0
    array.create_array()
    array.my_save(argv[2])
    print(f"file successfully saved as {array.output_name}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
