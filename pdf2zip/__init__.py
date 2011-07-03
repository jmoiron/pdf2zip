#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pdf2zip utility"""

import os
import sys
import time
import zipfile
import glob
import optparse
import subprocess
import multiprocessing

VERSION = (1, 0)
TEMP = "/tmp/"

if os.path.exists("/dev/shm/"):
    TEMP = "/dev/shm/"

def write(string):
    sys.stdout.write(string)
    sys.stdout.flush()

def execute(cmd, wait=True):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if wait:
        return p.wait()
    return

def check_deps():
    pdfimages = which('pdfimages')
    convert = which('convert')
    if not pdfimages:
        print "Error: program `pdfimages` required."
        sys.exit(2)
    if not convert:
        print "Error: imagemagick program `convert` required."
        sys.exit(2)
    return pdfimages, convert

def rmdir(filename):
    dest = destdir(filename)
    files = glob.glob('%s/*' % dest)
    for file in files:
        os.unlink(file)
    os.rmdir(dest)

def destdir(filename):
    """Generate a destination directory for images given a filename."""
    safe = filename.lower().replace(" ", "_").replace('.pdf', '')
    dest = os.path.join(TEMP, safe)
    if not os.path.exists(dest):
        os.makedirs(dest)
    return dest

def skipfile(filename):
    """Read a skip file, return a list of integers."""
    with open(filename) as f:
        data = f.readlines()
    return map(int, map(str.strip, data))

def to_images(filename):
    """Turn a filename (pdf) to images with pdfimages."""
    cmd = ['pdfimages', '-j', filename, destdir(filename) + '/orig']
    write("Creating images in %s ... " % (destdir(filename) + '/'))
    execute(cmd)
    write("done.\n")
    return

def strip_images(filename, skip):
    """Delete the images corresponding to a strip list."""
    skip = list(set(skip))
    dest = destdir(filename)
    files = glob.glob('%s/*' % dest)
    numfilter = lambda x: int(os.path.basename(x).split('-')[1].split('.')[0])
    filemap = dict([(numfilter(f), f) for f in files])
    for num in skip:
        os.unlink(filemap[num])
    write("Deleted %d unwanted images.\n" % len(skip))

def convert_image(args):
    cmdbase, path, q = args
    dest = os.path.dirname(path)
    base = os.path.basename(path)
    result = os.path.join(dest, 'v2-%s' % base)
    cmd = cmdbase + [path, result]
    execute(cmd)
    q.put(1)

def convert_images(filename, opts):
    """Run convert on images."""
    dest = destdir(filename)
    quality = opts.quality
    if opts.scale:
        cmdbase = ["convert", "-scale", opts.scale]
    elif opts.dimensions:
        cmdbase = ["convert", "-resize", opts.dimensions]
    elif opts.ipad:
        cmdbase = ["convert", "-resize", "1650x1650"]
    cmdbase += ["-quality", str(opts.quality)]
    images = glob.glob('%s/*' % dest)

    manager = multiprocessing.Manager()
    q = manager.Queue()
    pool = multiprocessing.Pool()
    result = pool.map_async(convert_image, [(cmdbase,i,q) for i in images])
    count, total = 0, len(images)
    while count < total:
        q.get()
        count += 1
        write("\rConverting %d of %d " % (count, total))
    write("Converting %d of %d\n" % (total, total))

    for image in images:
        full = os.path.join(dest, image)
        os.unlink(full)

def zip_images(filename):
    dest = destdir(filename)
    zf = zipfile.ZipFile(filename.replace('.pdf', '.zip'), 'w')
    current = os.getcwd()
    destdirname = os.path.basename(dest)
    # cd to one step above the directory
    os.chdir(os.path.dirname(dest))
    for path in glob.glob('%s/*' % destdirname):
        zf.write(path)
    zf.close()
    for path in glob.glob('%s/*' % destdirname):
        os.remove(path)
    os.rmdir(dest)
    os.chdir(current)

def main():
    check_deps()
    opts, args = parse_args()
    if not len(args) == 1:
        print "Error: must supply one pdf file."
        sys.exit(2)
    filename = args[0]
    skip = []
    if opts.skip_file:
        skip = skipfile(opts.skip_file)
    if opts.skip:
        skip = map(int, opts.skip.split(','))
    to_images(filename)
    if skip:
        strip_images(filename, skip)
    if any([opts.scale, opts.dimensions, opts.ipad]):
        convert_images(filename, opts)
    zip_images(filename)
    return 0

def parse_args():
    parser = optparse.OptionParser(version='.'.join(map(str, VERSION)),
        usage="./%prog [options] file.pdf")
    parser.add_option('', '--skip', help="comma separated pages to skip (0 is first)")
    parser.add_option('', '--skip-file', help="supply a file with a number per line of pages to skip")
    parser.add_option('', '--scale', help="scale pages to certain size (ex. 50%)")
    parser.add_option('-d', '--dimensions', help="resize images to fit within box")
    parser.add_option('-q', '--quality', default=90, help="quality of jpeg compression (default 90)")
    parser.add_option('', '--ipad', action="store_true", help="resize images to a good size for ipad")
    opts, args = parser.parse_args()
    opts.quality = int(opts.quality)
    return opts, args

def which(program):
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None
