#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IMAGE -> MATRIX

Use imgmap.py with mapimg.py

Tested with trasparent, white, black "png" and "jpeg".

All images in folder with default color.
$ imgmap.py test.png | mapimg.py
Args.
$ imgmap.py test.png | mapimg.py 222,0,222,220
Stdin without imgmap.py.
echo '[[1,1,0,1,1],[0,0,1,0,0],[1,1,0,1,1]]' | mapimg.py
Stdin without imgmap.py + scale.
echo '[[1,1,0,1,1],[0,0,1,0,0],[1,1,0,1,1]]' | mapimg.py -4
Stdin without imgmap.py + scale and 2 colors
echo '[[1,1,2,1,1],[0,2,1,2,0],[1,1,2,1,1]]' | mapimg.py -4 222,0,222,255 128,128,128,255
"""

__version__ = 1.0

# mapimg.py

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


from os import getcwd, sep
from sys import argv, stderr, stdin
from PIL import Image

DEFAULT_COLOR = (0, 255, 0, 255)
SCALE = 1


def matrix_image(map_image, scale, colors):
    """
    matrix_image(map_image, scale, colors)

    take:
        map_image: matrix with 0 - background, 1,2,3...n - diferent colors;
        colors: list with RGB colors  colors[0] == main color.
    return:
        new_clone: PIL Image
        delta_color: number of colors to finish image.
    """
    new_w = len(map_image[0])
    new_h = len(map_image)

    new_clone = Image.new('RGBA', (new_w, new_h), (0, 0, 0, 0))

    delta_color = 0
    for i in range(new_h):
        for j in range(new_w):
            if map_image[i][j] != 0:
                # if not enougnh colors use again first color
                if map_image[i][j] <= len(colors):
                    color = colors[map_image[i][j] - 1]
                else:
                    # give solutions how many colors need to finish image
                    delta = map_image[i][j] - len(colors)
                    if delta > delta_color:
                        delta_color = delta

                    color = colors[0]
                new_clone.putpixel((j, i), color)

    new_clone = new_clone.resize((new_w * scale, new_h * scale))

    return new_clone, delta_color


if __name__ == '__main__':
    if stdin.isatty() is False:
        # all errors in stderr
        for num, matr in enumerate(stdin.readlines(), 1):
            if len(argv) > 1 and argv[1].startswith('-'):
                scale = int(argv[1][1:])
            else:
                scale = SCALE
            if argv[2:]:
                colors = [eval(i) for i in argv[2:]]
            else:
                colors = [DEFAULT_COLOR]
            image, delta = matrix_image(eval(matr), scale, colors)

            filename = f'mapimg_{num}.png'
            if delta:
                adds = 's' if delta > 1 else ''
                advice = f'Add {delta} color{adds} for {filename}.'
                stderr.write(f'Error: not enough colors. {advice}\n')

            print(f'Create image: {getcwd()}{sep}{filename}')
            image.save(filename)
