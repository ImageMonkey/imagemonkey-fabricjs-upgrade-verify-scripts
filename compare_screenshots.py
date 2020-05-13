import argparse
import os
import cv2
from os import listdir
from os.path import isfile, join
from skimage.metrics import structural_similarity as ssim


def get_files_in_directory(directory):
    return [f for f in listdir(directory) if isfile(join(directory, f))]

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder1", type=str, required=True, help="folder 1")
    parser.add_argument("--folder2", type=str, required=True, help="folder 2")
    parser.add_argument("--treshold", type=float, required=False, default=0.99, help="treshold")

    args = parser.parse_args()

    if not os.path.isdir(args.folder1):
        print("%s is not a directory" %args.folder1)
        sys.exit(1)

    if not os.path.exists(args.folder2):
        print("%s is not a directory" %args.folder2)
        sys.exit(1)


    files_in_folder1 = get_files_in_directory(args.folder1)
    files_in_folder2 = get_files_in_directory(args.folder2)

    if set(files_in_folder1) != set(files_in_folder2):
        print("folder1 and folder2 contents do not match!")
        sys.exit(1)
    print(files_in_folder1)

    for f in files_in_folder1:
        img1 = cv2.imread(args.folder1 + os.path.sep + f, 0)
        img2 = cv2.imread(args.folder2 + os.path.sep + f, 0) 
        s = ssim(img1, img2)
        if float(s) < args.treshold:
            print("ERROR: got: %f, expected: %f" %(s, args.treshold))

