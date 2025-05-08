from PIL import Image

from .variables import PIXEL_FORMAT

class PILImage():

    def __init__(self):
        self.height: int = 0
        self.width: int = 0
        return

    def load(self, filename: str):
        self.image = Image.open(filename).convert(PIXEL_FORMAT)
        self.width, self.height = self.image.size
        return

    def convert_to_my_image(self):
        from .MyImage import MyImage

        new: MyImage = MyImage()
        new.array = []
        new.width = self.width
        new.height = self.height
        for i in range(self.height):
            temp = []
            for j in range(self.width):
                pixel = self.image.getpixel((j, i))
                temp.append(pixel)
            new.array.append(temp)
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
