import d3dshot
import PIL


def main():
    d = d3dshot.create()
    d.capture()
    PIL.imshow(d.get())
    d.stop()


main()
