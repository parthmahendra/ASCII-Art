from PIL import Image
import numpy as np


kernel_gx = [
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1],
]

img = Image.open("./steam.PNG").convert("RGB")
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
            colours = [r,g,b]
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
            output[y][x].append(((gx[y][x] ** 2) + (gy[y][x] ** 2)) ** (1 / 2))


# normalise output so maximum pixel value is 256

for y in range(height):
    for x in range(width):
        output[y][x] =  ((output[y][x][0] ** 2) + (output[y][x][1] ** 2) + (output[y][x][2] ** 2)) ** (1/2)


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
new_im.save("edgeDetected.jpeg")
