from PIL import Image
from PIL import GifImagePlugin
import numpy as np
import os
import sys
import time


def EdgeDetect(inputfile, outputfile):

    kernel_gx = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1],
    ]

    img = Image.open(inputfile).convert("RGB")
    width, height = img.size

    barr = []
    gx = []
    gy = []
    output = []
    for y in range(height):
        barr.append([])
        gx.append([])
        gy.append([])
        output.append([])
        for x in range(width):
            barr[y].append(0)
            gx[y].append(0)
            gy[y].append(0)
            output[y].append([])

    for c in range(3):
        for y in range(0, height):
            for x in range(0, width):
                r, g, b = (img.getpixel((x, y)))
                colours = [r, g, b]
                brightness = colours[c]
                barr[y][x] = brightness

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                tx = 0
                ty = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        tx += barr[y + dy][x + dx] * kernel_gx[dy][dx]
                        ty += barr[y + dy][x + dx] * kernel_gx[dx][dy]
                gx[y][x] = tx
                gy[y][x] = ty

        for y in range(height):
            for x in range(width):
                output[y][x].append(pythagoras(gy[y][x], gx[y][x]))

    # normalise output so maximum pixel value is 256

    for y in range(height):
        for x in range(width):
            t = 0
            for n in range(3):
                t += abs(output[y][x][n])
            output[y][x] = t

    max = 0
    for y in output:
        for x in y:
            if x > max:
                max = x

    for y in range(height):
        for x in range(width):
            output[y][x] *= (256 / max)

    output = np.array(output).reshape(height, width)
    new_im = Image.fromarray(output)
    if new_im.mode != 'RGB':
        new_im = new_im.convert('RGB')
    new_im.save(outputfile)


def pythagoras(a, b):
    return ((a**2) + (b**2)) ** (1 / 2)


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


def ascify(filepath):
    # Generating ASCII Array For Each Frame
    img = Image.open(filepath).convert('RGB')
    # img = remove_transparency(img)
    width, height = img.size
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


GIF = Image.open(sys.argv[1])
DEPTH = 256
SCREENHEIGHT = getTerminalSize()
LENGTH = GIF.n_frames
DURATION = GIF.info['duration'] / 1000
ASCIIFRAMES = []
W, H = GIF.size

if H > SCREENHEIGHT:
    H = SCREENHEIGHT
    SIZE = W, H

for frame in range(0, LENGTH):
    # Iterating Through GIF Frames And Appending Them To ASCIIFrames Array
    GIF.seek(frame)
    LoadingScreen(frame, LENGTH)
    thumb = GIF.copy()
    thumb.thumbnail(SIZE, Image.ANTIALIAS)
    thumb.save("./temp/" + str(frame) + ".jpg", 'GIF')
    EdgeDetect("./temp/" + str(frame) + ".jpg",
               "./temp/" + str(frame) + "detected.jpg")
    ASCIIFRAMES.append(ascify("./temp/" + str(frame) + "detected.jpg"))
    os.remove("./temp/" + str(frame) + ".jpg")
    os.remove("./temp/" + str(frame) + "detected.jpg")

while True:
    # Playback
    for frame in ASCIIFRAMES:
        os.system("clear")
        print(frame)
        time.sleep(DURATION)
