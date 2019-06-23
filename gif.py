from PIL import Image
from PIL import GifImagePlugin
import os
import sys
import time


def LoadingScreen(framenumber, length):
    # Loading Screen While Frames Are Being Processed
    os.system('clear')
    print("Loading" + ((".") * ((framenumber % 3) + 1)))
    print("Frame Number: " + str(framenumber) + "/" + str(length))


def reverse(arr):
    # Reversing ASCII Character Order If Dark Mode
    reversedarr = []
    for i in reversed(arr):
        reversedarr.append(i)
    return reversedarr


def getTerminalSize():
    # Get Terminal Size To Convert GIF To Match Resolution
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows) - 1


def ascii(r, g, b, y, x, Array):
    # Converts Pixel Passed In And Appends to ASCII Array For Particular Frame
    value = r + g + b
    chars = ["#", "@", "$", "[", "|", "+", "^",
             "_", "~", "*", "\"", "'", ".", " "]
    try:
        if sys.argv[2].upper() == "D":
            chars = reverse(chars)
    except:
        pass

    for i in range(len(chars)):
        if value >= ((DEPTH / len(chars)) * i * 3):
            Array[y][x] = (chars[i] * 2)


def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Removing Transparency To Get Consistent Data Unpacking
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        alpha = im.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg
    else:
        return im


def ascify(filepath):
    # Generating ASCII Array For Each Frame
    img = Image.open(filepath).convert('RGB')
    width, height = img.size
    img = remove_transparency(img)
    Array = []
    for y in range(height):
        Array.append([])
        for x in range(width):
            Array[y].append("0")
    t = ""
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            ascii(r, g, b, y, x, Array)
        line = "".join(Array[y])
        t += line + "\n"
    return t


imageObject = Image.open(sys.argv[1])
DEPTH = 256
SCREENHEIGHT = getTerminalSize()
LENGTH = imageObject.n_frames
DURATION = imageObject.info['duration'] / 1000
w, h = imageObject.size

if h > SCREENHEIGHT:
    h = SCREENHEIGHT

    size = w, h

arr = []
for frame in range(0, LENGTH):
    imageObject.seek(frame)
    LoadingScreen(frame, LENGTH)
    thumb = imageObject.copy()
    thumb.thumbnail(size, Image.ANTIALIAS)
    thumb.save("./temp/" + str(frame) + ".jpg", 'GIF')
    arr.append(ascify("./temp/" + str(frame) + ".jpg"))
    os.remove("./temp/" + str(frame) + ".jpg")

while True:
    for frame in arr:
        os.system("clear")
        print(frame)
        time.sleep(DURATION)
