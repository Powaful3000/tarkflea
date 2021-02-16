import d3dshot
import time

tarkPos = (10, 10)
d = d3dshot.create(capture_output="pil", frame_buffer_size=2)
d.capture(target_fps=120, region=(
    tarkPos[0], tarkPos[1], tarkPos[0]+1024, tarkPos[1]+768))


def main():
    time.sleep(1)
    d.d.get_frame(0)
    d.stop()


main()
