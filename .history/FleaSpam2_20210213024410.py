import d3dshot
import PIL


def main():
    tarkPos = (10, 10)
    d = d3dshot.create()
    d.capture(target_fps=120, ())
    PIL.imshow(d.get())
    d.stop()


main()
