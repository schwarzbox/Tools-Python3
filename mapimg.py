#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script for create image from matrix.

Use imgmap.py with mapimg.py

Tested with trasparent, white, black "png" and "jpeg".

All images in folder with default color.
$ imgmap.py test.png | mapimg.py
Args.
$ imgmap.py test.png | mapimg.py 222,0,222,220
Stdin without imgmap.py.
echo '[[1,1,0,1,1],[0,0,1,0,0],[1,1,0,1,1]]' | mapimg.py
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


from sys import argv, stderr, stdin, stdout

from PIL import Image

DEFAULT_COLOR = (0, 255, 0, 255)


def matrix_image(map_image, colors=[DEFAULT_COLOR]):
    """
    matrix_image(map_image, colors=[DEFAULT_COLOR])

    take:
        map_image: matrix with 0 - background, 1,2,3...n - diferent colors;
        colors: list with RGB colors  colors[0] == main color.
    return:
        new_clone: PIL Image
        delta_color: number of colors to finish image.
    """

    # rotate matrix
    new_w = len(map_image)
    new_h = len(map_image[0])

    new_clone = Image.new('RGBA', (new_w, new_h), (0, 0, 0, 0))

    delta_color = 0
    for i in range(new_w):
        for j in range(new_h):
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
                new_clone.putpixel((i, j), color)

    return new_clone, delta_color


if __name__ == '__main__':
    if stdin.isatty() is False:
        # all errors in stderr
        for num, matr in enumerate(stdin.readlines(), 1):
            if argv[1:]:
                colors = [eval(i) for i in argv[1:]]
            else:
                colors = [DEFAULT_COLOR]
            image, delta = matrix_image(eval(matr), colors)

            filename = f'mapimg_{num}.png'
            if delta:
                stderr.write('ERROR: not enough colors\n')
                adds = 's' if delta > 1 else ''
                advice = f'{filename}: add {delta} color{adds}\n'
                stdout.write(advice)
            # test image
            image.save(filename)
