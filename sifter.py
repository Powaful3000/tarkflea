import cv2


class img:
    att = {}

    def __init__(self, keypoints=None, descriptors=None):
        self.att["keypoints"] = keypoints
        self.att["descriptors"] = descriptors


class Sifter:

    def siftImage(self, i):
        keypoints, descriptors = self.sift.detectAndCompute(
            cv2.cvtColor(i, cv2.COLOR_BGR2GRAY), None)
        return i(keypoints, descriptors)

    def siftImageLoc(self, loc):
        return self.siftImage(cv2.imread(loc))

    def add(self, i):
        self.images += self.siftImage(i)

    def addLoc(self, loc):
        self.add(self.siftImageLoc(loc))

    def __init__(self):
        self.images = []
        self.bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        self.sift = cv2.SIFT_create()
