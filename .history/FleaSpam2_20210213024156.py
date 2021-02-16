import d3dshot


def main(): {
    d = d3dshot.create()
    d.capture()

    d.stop()
}


main()
