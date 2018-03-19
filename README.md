# Tools-Python3

CLI Scripts

# xcodeimg.py

AppIcon (Mac, iPhone/iPad, Apple Watch) | LaunchImage (iPhone/iPad) | iTunesArtwork.

Script build all AppIcons and LaunchImage from any kind of images.

File formats ('png', 'gif', 'jpeg', 'jpg', 'tif', 'tiff', 'psd')

Args.
``` bash
xcodeimg.py icon.png launch.png
```

Copy images icon.* or launch.* in current dir.
``` bash
xcodeimg.py
```

Script create dir Assets.xcassets with AppIcon.appiconset and LaunchImage.launchimage.

Contents.json files in every dir.

Optimal size AppIcon 1024x1024.

Optimal size for LaunchImage 2208x2208 with AppIcon 512x512 in the middle.

Image crop from the center.

# imgmap.py | mapimg.py

Use imgmap.py with mapimg.py. You can change color of image.

imgmap.py - create matrix from image.

mapimg.py - create image from matrix.

Use black, white or transparent background. Use simple images.

Tested with trasparent, white, black background for "png" and "jpeg". Faster with indexed colors.

All images in folder with two colors.
``` bash
imgmap.py | mapimg.py 222,0,222,220 100,220,0,200
```
Args.
``` bash
imgmap.py test.png | mapimg.py 222,0,222,220
```
Stdin.
``` bash
echo 'test.png' | imgmap.py | mapimg.py 222,0,222,220
```
All images in folder with default color.
``` bash
imgmap.py test.png | mapimg.py
```
Args.
``` bash
imgmap.py test.png | mapimg.py 222,0,222,220
```
Stdin without imgmap.py.
``` bash
echo '[[1,1,0,1,1],[0,0,1,0,0],[1,1,0,1,1]]' | mapimg.py
```
