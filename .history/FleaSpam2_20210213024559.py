import d3dshot
import PIL
from matplotlib.pyplot import imshow

tarkPos = (10, 10)


def main():
    d = d3dshot.create()
    d.capture(target_fps=120, region=(
        tarkPos[0], tarkPos[1], tarkPos[0]+1024, tarkPos[1]+768))
    imshow(d.get())
    d.stop()


main()
