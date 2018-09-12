#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MATRIX -> IMAGE.

Use imgmap.py with mapimg.py.

All image in folder with two colors.
$ imgmap.py | mapimg.py 222,0,222,220 100,220,0,200
Args.
$ imgmap.py test.png | mapimg.py 222,0,222,220
Stdin.
$ echo 'test.png' | imgmap.py | mapimg.py 222,0,222,220
Stdout.
$ imgmap.py icon.png >> out.txt
"""

__version__ = 1.0

# imgmap.py

# MIT License
# Copyright (c) 2017 Alexander Veledzimovich veledz@gmail.com

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# use black, white or transparent background
# indexed colors - faster and better, resolution <600 px
# PNG: trasparent - OK,  white - OK, black - OK, indexed - OK, RGB - BAD
# BMP: transparent - OK, white - OK, black - OK, indexed - OK, RGB - OK
# TIFF: transparent - OK, white - OK, black - OK, indexed - OK, RGB - OK
# JPEG: transparent - NO, white - BAD, black - BAD indexed - NO, RGB - BAD

from glob import glob
from os import path
from sys import argv, stderr, stdin, stdout

from PIL import Image

# made tolerance


def image_matrix(img):
    """
    image_matrix(img)

    take:
        img: PATH to image file
    return:
        map_image: matrix with 0 - background, 1,2,3...n - diferent colors.
    """

    image = Image.open(img)
    image = image.convert('RGBA')
    back = image.getpixel((0, 0))

    if back in [(0, 0, 0, 0), (255, 255, 255, 0), (0, 0, 0, 255),
                (255, 255, 255, 255)]:

        w, h = image.size

        # create map image
        map_image = [[0] * w for i in range(h)]

        colors = dict()
        # create map with colors
        for y in range(h):
            for x in range(w):
                pix = image.getpixel((x, y))

                if pix != back:
                    if not colors.get(pix):
                        colors[pix] = 1
                    else:
                        colors[pix] += 1

                    map_image[y][x] = pix

        # sort colors for find main color
        sort_colors = sorted(list(colors.items()),
                             key=lambda i: i[1], reverse=True)

        # put  numbers to code colors
        for y in range(h):
            for num, item in enumerate(sort_colors, 1):
                for x in range(w):
                    if map_image[y][x] == item[0]:
                        map_image[y][x] = num

        return map_image


if __name__ == '__main__':
    inp = []
    EXT = ('*.jpeg', '*.jpg', '*.png', '*.gif', '*.tiff', '*.tif', '*.bmp')
    if argv[1:]:
        inp = [i for i in argv[1:] if path.exists(i)]
    elif stdin.isatty() is False:
        # to avoid /n in the end of the line
        inp = [i.strip() for i in stdin.readlines()
               if path.exists(i.strip())]

    elif any([glob(i) for i in EXT]):
        all_images = [glob(i) for i in EXT] + [glob(i.upper()) for i in EXT]
        inp = [image for list_ in all_images
               for image in list_]
    else:
        stderr.write('Error: empty input\n')
    if inp:
        map_collection = []
        for i in inp:
            matrix = image_matrix(i)
            if matrix:
                map_collection.append(matrix)
            else:
                stderr.write(
                    'Error: use black/white/transparent background\n'
                )

        for i in map_collection:
            # use print easiest way but it is also a string
            print(i)
    else:
        stderr.write('Error: wrong path\n')
