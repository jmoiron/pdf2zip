pdf2zip
-------

pdf2zip is a small utility to batch convert PDFs that are image based (like
many online distributions of magazines are) into a zipfile full of images.
Various options are available, including options on the quality of the
resulting images, options to scale or resize the images to a bounding box,
and the ability to specify pages in the PDF to skip.

This was primarily developed for personal use, but is made available in the
hopes that it might be useful for someone.

To install, just::

    pip install pdf2zip

usage
-----

    Usage: ./pdf2zip [options] file.pdf

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      --skip=SKIP           comma separated pages to skip (0 is first)
      --skip-file=SKIP_FILE
                            supply a file with a number per line of pages to skip
      --scale=SCALE         scale pages to certain size (ex. 50%)
      -d DIMENSIONS, --dimensions=DIMENSIONS
                            resize images to fit within box
      -q QUALITY, --quality=QUALITY
                            quality of jpeg compression (default 90)
      --ipad                resize images to a good size for ipad

