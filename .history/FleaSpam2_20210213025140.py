import d3dshot
import PIL
import time

tarkPos = (10, 10)


def main():
    d = d3dshot.create(capture_output="pil", frame_buffer_size=60)
    d.capture(target_fps=120, region=(
        tarkPos[0], tarkPos[1], tarkPos[0]+1024, tarkPos[1]+768))
    time.sleep(1)
    im = d.get_latest_frame()
    im.show()
    d.stop()


main()
