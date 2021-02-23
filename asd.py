# import numpy as np
import cv2
import matplotlib.pyplot as plt
import cv2
from matplotlib import pyplot as plt
import json
import time
import numpy as np
bf = cv2.BFMatcher()
sift = cv2.SIFT_create()


def gen(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    return (gray, keypoints, descriptors)


testIMG = cv2.imread("./search/okHD.png")
succeedIMG = cv2.imread("./search/asd.png")
failIMG = cv2.imread("./search/asdadsasd.png")
test = gen(testIMG)
succeed = gen(succeedIMG)
fail = gen(failIMG)


def go(against):
    return bf.knnMatch(test[2], against[2], k=2)


Now = time.time()
a = [[m] for m, n in go(succeed) if m.distance < 0.75*n.distance]
print((time.time()-Now))
b = [[m] for m, n in go(fail) if m.distance < 0.75*n.distance]


print(len(a), len(b))


def imagesearcharea(image, precision=0.8, im=None):
    if im is None:
        print("fuck")
        return

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    if template is None:
        raise FileNotFoundError('Image file not found: {}'.format(image))

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc
