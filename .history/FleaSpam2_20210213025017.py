import d3dshot
import PIL

tarkPos = (10, 10)


def main():
    d = d3dshot.create(capture_output="pil", frame_buffer_size=60)
    d.capture(target_fps=120, region=(
        tarkPos[0], tarkPos[1], tarkPos[0]+1024, tarkPos[1]+768))
    sleep(1)
    d.get_latest_frame().show()
    d.stop()


main()
