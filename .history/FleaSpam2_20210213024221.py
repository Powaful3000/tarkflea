import d3dshot
import PIL


def main():
    d = d3dshot.create()
    d.capture()

    d.stop()


main()
