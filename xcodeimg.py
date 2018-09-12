#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XCODE ICONS

Create AppIcon (Mac, iPhone/iPad, Apple Watch) LaunchImage (iOS) iTunesArtwork.

Args.
$ xcodeimg.py icon.png launch.png
Copy images icon.* or launch.* in current dir.
$ xcodeimg.py

Optimal size AppIcon 1024x1024.
Optimal size for LaunchImage 2208x2208 with AppIcon 512x512 in the middle.
Image crop from the center.
File formats ('png', 'gif', 'jpeg', 'jpg', 'tif', 'tiff','psd')

Script create dir Assets.xcassets with AppIcon.appiconset and LaunchImage.launchimage.
Script create Contents.json files in every dir.
"""

__version__ = 1.0

# xcodeimg.py

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

import json
import os
import sys
from shutil import rmtree

from PIL import Image


def create_image(directory, data, img, type_img):
    """
    create_image(directory, data, img, type_img)

    take:
        directory: dir for new images
        data: json data
        img: PIL image
        type_img: 'icon' or 'launch'
    return:
        None

    Create images for all sizes from Contents.json.
    """
    if not os.path.isdir(os.getcwd() + os.sep + directory):
        os.mkdir(os.getcwd() + os.sep + directory)
    name = 'Contents.json'
    with open(os.path.join(os.getcwd(), directory, name), 'w') as file:
        # for python3
        json.dump(data, file, ensure_ascii=False, indent=4,
                  separators=(',', ': '), sort_keys=True)
    # save itunes artwork
    # without png
    if type_img == 'icon':
        img_res = img
        for i in [('iTunesArtwork.png', (512, 512)),
                  ('iTunesArtwork@2x.png', (1024, 1024))]:
            resize = img_res.resize(i[1], Image.ANTIALIAS)
            resize.save(os.path.join(os.getcwd(), i[0]))
            # make without png
            os.rename(i[0], i[0].split('.')[0])

    for i in data['images']:
        img_res = img

        if type_img == 'icon':

            filename = i['filename']
            wid, hei = img_res.size
            c_wid = wid // 2
            c_hei = hei // 2

            delta = wid // 2
            if wid > hei:
                delta = hei // 2

            img_res = img_res.crop((c_wid - delta, c_hei - delta,
                                    c_wid + delta, c_hei + delta))
            size = int(float(i['size'].split('x')[0]) *
                       float(i['scale'].split('x')[0]))

            resize = img_res.resize([size, size], Image.ANTIALIAS)
        else:
            filename = i['filename']
            # to avoid black parts in small images
            sizex = int(float(i['size'].split('x')[0]) *
                        float(i['scale'].split('x')[0]))
            sizey = int(float(i['size'].split('x')[1]) *
                        float(i['scale'].split('x')[0]))
            size = (sizex, sizey)
            if (1334 in size or 768 in size or 1024 in size or 640 in size):
                img_res = img.resize((1334, 1334), Image.ANTIALIAS)
            elif 320 in size:
                img_res = img.resize((640, 640), Image.ANTIALIAS)
            else:
                img_res = img.resize((2208, 2208), Image.ANTIALIAS)
            wid, hei = img_res.size
            c_wid = wid // 2
            c_hei = hei // 2
            hlf_x = size[0] // 2
            hlf_y = size[1] // 2
            resize = img_res.crop((c_wid - hlf_x, c_hei - hlf_y,
                                   c_wid + hlf_x, c_hei + hlf_y))

        resize.save(os.path.join(os.getcwd(), directory, filename))


def main(images):
    """
    main(images)

    take:
        images: icon.* and\or launch.*

    return:
        None

    Wait for user input and call create_image for every image.
    """
    if len(images) > 1:
        image_app, image_launch = images[0], images[1]
    else:
        image_app, image_launch = images[0], images[0]

    img_app = Image.open(os.path.realpath(image_app))
    typeic = input('AppIcon: Mac(m), iPhone/iPad(i), Apple Watch(w), No(n): '
                   ).lower() or 'i'

    if typeic == 'm':
        print('Create AppIcon for Mac.')
        content_app = {
            'images': [
                {
                    'idiom': 'mac',
                    'filename': 'icon_16x16.png',
                    'size': '16x16',
                    'scale': '1x'
                },
                {
                    'idiom': 'mac',
                    'filename': 'icon_16x16@2x.png',
                    'size': '16x16',
                    'scale': '2x'
                },
                {
                    'idiom': 'mac',
                    'filename': 'icon_32x32.png',
                    'size': '32x32',
                    'scale': '1x'
                },
                {
                    'idiom': 'mac',
                    'filename': 'icon_32x32@2x.png',
                    'size': '32x32',
                    'scale': '2x'
                },
                {
                    'idiom': 'mac',
                    'filename': 'icon_128x128.png',
                    'size': '128x128',
                    'scale': '1x'
                },
                {
                    'idiom': 'mac',
                    'filename': 'icon_128x128@2x.png',
                    'size': '128x128',
                    'scale': '2x'
                },
                {
                    'idiom': 'mac',
                    'filename': 'icon_256x256.png',
                    'size': '256x256',
                    'scale': '1x'
                },
                {
                    'idiom': 'mac',
                    'filename': 'icon_256x256@2x.png',
                    'size': '256x256',
                    'scale': '2x'
                },
                {
                    'idiom': 'mac',
                    'filename': 'icon_512x512.png',
                    'size': '512x512',
                    'scale': '1x'
                },
                {
                    'idiom': 'mac',
                    'filename': 'icon_512x512@2x.png',
                    'size': '512x512',
                    'scale': '2x'
                }
            ],
            'info': {
                'version': 1,
                'author': 'xcode'
            }
        }
    elif typeic == 'i':
        print('Create AppIcon for iPhone/iPad.')
        content_app = {
            'images': [
                {
                    'size': '20x20',
                    'idiom': 'iphone',
                    'filename': 'Icon-Notification@2x.png',
                    'scale': '2x'
                },
                {
                    'size': '20x20',
                    'idiom': 'iphone',
                    'filename': 'Icon-Notification@3x.png',
                    'scale': '3x'
                },
                {
                    'size': '29x29',
                    'idiom': 'iphone',
                    'filename': 'Icon-Small.png',
                    'scale': '1x'
                },
                {
                    'size': '29x29',
                    'idiom': 'iphone',
                    'filename': 'Icon-Small@2x.png',
                    'scale': '2x'
                },
                {
                    'size': '29x29',
                    'idiom': 'iphone',
                    'filename': 'Icon-Small@3x.png',
                    'scale': '3x'
                },
                {
                    'size': '57x57',
                    'idiom': 'iphone',
                    'filename': 'Icon.png',
                    'scale': '1x'
                },
                {
                    'size': '57x57',
                    'idiom': 'iphone',
                    'filename': 'Icon@2x.png',
                    'scale': '2x'
                },

                {
                    'size': '40x40',
                    'idiom': 'iphone',
                    'filename': 'Icon-Small-40@2x.png',
                    'scale': '2x'
                },
                {
                    'size': '40x40',
                    'idiom': 'iphone',
                    'filename': 'Icon-Small-40@3x.png',
                    'scale': '3x'
                },
                {
                    'size': '60x60',
                    'idiom': 'iphone',
                    'filename': 'Icon-60@2x.png',
                    'scale': '2x'
                },
                {
                    'size': '60x60',
                    'idiom': 'iphone',
                    'filename': 'Icon-60@3x.png',
                    'scale': '3x'
                },

                {
                    'size': '20x20',
                    'idiom': 'ipad',
                    'filename': 'Icon-Notification.png',
                    'scale': '1x'
                },
                {
                    'size': '20x20',
                    'idiom': 'ipad',
                    'filename': 'Icon-Notification@2x.png',
                    'scale': '2x'
                },
                {
                    'size': '29x29',
                    'idiom': 'ipad',
                    'filename': 'Icon-Small.png',
                    'scale': '1x'
                },
                {
                    'size': '29x29',
                    'idiom': 'ipad',
                    'filename': 'Icon-Small@2x.png',
                    'scale': '2x'
                },
                {
                    'size': '40x40',
                    'idiom': 'ipad',
                    'filename': 'Icon-Small-40.png',
                    'scale': '1x'
                },
                {
                    'size': '40x40',
                    'idiom': 'ipad',
                    'filename': 'Icon-Small-40@2x.png',
                    'scale': '2x'
                },
                {
                    'size': '50x50',
                    'idiom': 'ipad',
                    'filename': 'Icon-Small-50.png',
                    'scale': '1x'
                },
                {
                    'size': '50x50',
                    'idiom': 'ipad',
                    'filename': 'Icon-Small-50@2x.png',
                    'scale': '2x'
                },
                {
                    'size': '72x72',
                    'idiom': 'ipad',
                    'filename': 'Icon-72.png',
                    'scale': '1x'
                },
                {
                    'size': '72x72',
                    'idiom': 'ipad',
                    'filename': 'Icon-72@2x.png',
                    'scale': '2x'
                },
                {
                    'size': '76x76',
                    'idiom': 'ipad',
                    'filename': 'Icon-76.png',
                    'scale': '1x'
                },
                {
                    'size': '76x76',
                    'idiom': 'ipad',
                    'filename': 'Icon-76@2x.png',
                    'scale': '2x'
                },
                {
                    'size': '83.5x83.5',
                    'idiom': 'ipad',
                    'filename': 'Icon-83.5@2x.png',
                    'scale': '2x'
                }
            ],
            'info': {
                'version': 1,
                'author': 'xcode'
            }
        }
    elif typeic == 'w':
        print('Create AppIcon for Apple Watch.')
        content_app = {
            'images': [
                {
                    'size': '24x24',
                    'idiom': 'watch',
                    'scale': '2x',
                    'filename': 'icon-watch-24@2x.png',
                    'role': 'notificationCenter',
                    'subtype': '38mm'
                },
                {
                    'size': '27.5x27.5',
                    'idiom': 'watch',
                    'scale': '2x',
                    'filename': 'icon-watch-27.5@2x.png',
                    'role': 'notificationCenter',
                    'subtype': '42mm'
                },
                {
                    'size': '29x29',
                    'idiom': 'watch',
                    'filename': 'icon-watch-29@2x.png',
                    'role': 'companionSettings',
                    'scale': '2x'
                },
                {
                    'size': '29x29',
                    'idiom': 'watch',
                    'filename': 'icon-watch-29@3x.png',
                    'role': 'companionSettings',
                    'scale': '3x'
                },
                {
                    'size': '40x40',
                    'idiom': 'watch',
                    'scale': '2x',
                    'filename': 'icon-watch-40@2x.png',
                    'role': 'appLauncher',
                    'subtype': '38mm'
                },
                {
                    'size': '44x44',
                    'idiom': 'watch',
                    'scale': '2x',
                    'filename': 'icon-watch-44@2x.png',
                    'role': 'longLook',
                    'subtype': '42mm'
                },
                {
                    'size': '86x86',
                    'idiom': 'watch',
                    'scale': '2x',
                    'filename': 'icon-watch-86@2x.png',
                    'role': 'quickLook',
                    'subtype': '38mm'
                },
                {
                    'size': '98x98',
                    'idiom': 'watch',
                    'scale': '2x',
                    'filename': 'icon-watch-98@2x.png',
                    'role': 'quickLook',
                    'subtype': '42mm'
                }
            ],
            'info': {
                'version': 1,
                'author': 'xcode'
            }
        }
    else:
        print('No AppIcon.')
        typeic = 'n'

    img_lch = Image.open(os.path.realpath(image_launch))

    typelnc = input('LaunchImage(l), No(n): ').lower() or 'l'

    if typelnc == 'l':
        print('Create LaunchImage for iPhone/iPad.')
        content_lch = {
            'images': [
                {
                    'size': '320x480',
                    'orientation': 'portrait',
                    'idiom': 'iphone',
                    'filename': 'Default.png',
                    'extent': 'full-screen',
                    'scale': '1x'
                },
                {
                    'size': '320x480',
                    'orientation': 'portrait',
                    'idiom': 'iphone',
                    'filename': 'Default@2x.png',
                    'extent': 'full-screen',
                    'scale': '2x'
                },
                {
                    'size': '320x568',
                    'orientation': 'portrait',
                    'idiom': 'iphone',
                    'filename': 'Default-568h@2x.png',
                    'extent': 'full-screen',
                    'subtype': 'retina4',
                    'scale': '2x'
                },
                {
                    'size': '768x1004',
                    'orientation': 'portrait',
                    'idiom': 'ipad',
                    'filename': 'Portrait-status.png',
                    'extent': 'to-status-bar',
                    'scale': '1x'
                },
                {
                    'size': '768x1024',
                    'orientation': 'portrait',
                    'idiom': 'ipad',
                    'filename': 'Portrait.png',
                    'extent': 'full-screen',
                    'scale': '1x'
                },
                {
                    'size': '1024x748',
                    'orientation': 'landscape',
                    'idiom': 'ipad',
                    'filename': 'Landscape-status.png',
                    'extent': 'to-status-bar',
                    'scale': '1x'
                },
                {
                    'size': '1024x768',
                    'orientation': 'landscape',
                    'idiom': 'ipad',
                    'filename': 'Landscape.png',
                    'extent': 'full-screen',
                    'scale': '1x'
                },
                {
                    'size': '768x1004',
                    'orientation': 'portrait',
                    'idiom': 'ipad',
                    'filename': 'Landscape-status@2x.png',
                    'extent': 'to-status-bar',
                    'scale': '2x'
                },
                {
                    'size': '768x1024',
                    'orientation': 'portrait',
                    'idiom': 'ipad',
                    'filename': 'Portrait@2x.png',
                    'extent': 'full-screen',
                    'scale': '2x'
                },
                {
                    'size': '1024x748',
                    'orientation': 'landscape',
                    'idiom': 'ipad',
                    'filename': 'Portrait-status@2x.png',
                    'extent': 'to-status-bar',
                    'scale': '2x'
                },
                {
                    'size': '1024x768',
                    'orientation': 'landscape',
                    'idiom': 'ipad',
                    'filename': 'Landscape@2x.png',
                    'extent': 'full-screen',
                    'scale': '2x'
                },
                {
                    'size': '414x736',
                    'extent': 'full-screen',
                    'idiom': 'iphone',
                    'subtype': '736h',
                    'filename': 'Default-736h@3x.png',
                    'minimum-system-version': '8.0',
                    'orientation': 'portrait',
                    'scale': '3x'
                },
                {
                    'size': '736x414',
                    'extent': 'full-screen',
                    'idiom': 'iphone',
                    'subtype': '736h',
                    'filename': 'Default-Landscape-736h@3x.png',
                    'minimum-system-version': '8.0',
                    'orientation': 'landscape',
                    'scale': '3x'
                },
                {
                    'size': '375x667',
                    'extent': 'full-screen',
                    'idiom': 'iphone',
                    'subtype': '667h',
                    'filename': 'Default-667h@2x.png',
                    'minimum-system-version': '8.0',
                    'orientation': 'portrait',
                    'scale': '2x'
                },
                {
                    'size': '320x480',
                    'orientation': 'portrait',
                    'idiom': 'iphone',
                    'filename': 'Default@2x.png',
                    'extent': 'full-screen',
                    'minimum-system-version': '7.0',
                    'scale': '2x'
                },
                {
                    'size': '320x568',
                    'orientation': 'portrait',
                    'idiom': 'iphone',
                    'subtype': 'retina4',
                    'filename': 'Default-568h@2x.png',
                    'extent': 'full-screen',
                    'minimum-system-version': '7.0',
                    'scale': '2x'
                },
                {
                    'size': '768x1024',
                    'orientation': 'portrait',
                    'idiom': 'ipad',
                    'filename': 'Portrait.png',
                    'extent': 'full-screen',
                    'minimum-system-version': '7.0',
                    'scale': '1x'
                },
                {
                    'size': '1024x768',
                    'orientation': 'landscape',
                    'idiom': 'ipad',
                    'filename': 'Landscape.png',
                    'extent': 'full-screen',
                    'minimum-system-version': '7.0',
                    'scale': '1x'
                },
                {
                    'size': '768x1024',
                    'orientation': 'portrait',
                    'idiom': 'ipad',
                    'filename': 'Portrait@2x.png',
                    'extent': 'full-screen',
                    'minimum-system-version': '7.0',
                    'scale': '2x'
                },
                {
                    'size': '1024x768',
                    'orientation': 'landscape',
                    'idiom': 'ipad',
                    'filename': 'Landscape@2x.png',
                    'extent': 'full-screen',
                    'minimum-system-version': '7.0',
                    'scale': '2x'
                }
            ],
            'info': {
                'version': 1,
                'author': 'xcode'
            }
        }

    else:
        print('No LaunchImage.')

        typelnc = 'n'

    new_dir = 'Assets.xcassets'
    if not os.path.isdir(os.getcwd() + os.sep + new_dir):
        os.mkdir(os.getcwd() + os.sep + new_dir)

    os.chdir(new_dir)
    root = os.getcwd()
    # clean dir
    files = os.listdir()
    for i in range(len(files)):
        if os.path.isdir(files[i]):
            os.chdir(files[i])
            rmtree(os.getcwd())
            os.chdir(root)
        else:
            os.remove(files[i])

    assets = {
        'info': {
            'version': 1,
            'author': 'xcode'
        }
    }
    name = 'Contents.json'
    with open(os.path.join(os.getcwd(), name), 'w') as file:
        # for python3
        json.dump(assets, file, ensure_ascii=False, indent=4,
                  separators=(',', ': '), sort_keys=True)

    all_images = []
    if typeic != 'n':
        all_images.append(('AppIcon.appiconset',
                           content_app, img_app, 'icon'))
    if typelnc != 'n':
        all_images.append(('LaunchImage.launchimage',
                           content_lch, img_lch, 'launch'))
    if len(all_images) > 0:
        for i in all_images:
            create_image(*i)
        print('Create iconset:', os.getcwd())
    else:
        # clean dir
        rmtree(os.getcwd())


if __name__ == '__main__':
    print('Xcode iconset.')
    img = []
    type_img = ('.png', '.gif', '.jpeg', '.jpg', '.tif', '.tiff', '.psd')
    if len(sys.argv) > 1:
        for i in [i for i in sys.argv[1:3] if os.path.isfile(i)]:
            extens = os.path.splitext(i)[-1].lower()
            if extens in type_img:
                img.append(i)

    elif len(sys.argv) == 1:
        for i in [i for i in os.listdir() if os.path.isfile(i)]:
            extens = os.path.splitext(i)[-1].lower()

            if (i.startswith('icon') or
                    i.startswith('launch')) and extens in type_img:
                img.append(i)

    if len(img) > 0:
        main(img)
    else:
        print('Error: Enter correct path.', end=' ')
        print('Put "icon.*" or "launch.*" image in current dir.')
        print('Supported formats: png, gif, jpeg, jpg, tif, tiff.')
