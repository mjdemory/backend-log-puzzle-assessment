#!/usr/bin/env python2
"""
Log Puzzle exercise
Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0
Given an Apache logfile, find the puzzle URLs and download the images.
Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
__author__ = "Michael DeMory, with help from Tiffany McLean, Mavrick Watts, Daniel,and Zac Gerber "

import os
import re
import sys
import urllib.request
import argparse


def read_urls (filename):
    """Open, pattern search for specific urls, read files"""
    path = "http://" + filename.split("_")[1]
    urls = set()
    images = re.findall(r'GET (\/.*?\.jpg)', open(filename).read())

    for image in images:
        if '/puzzle/' in image:
            urls.add(path + image)

    return sorted(urls, key=return_last_word)

def return_last_word(url):
    """allows for sort on last portion of file name"""
    matches = re.search(r'-(\w+)-(\w+).jpg', url)
    if matches:
        return matches.group(2)
    return url

def download_images(img_urls, dest_dir):
    """download images and assemble"""

    if not os.path.exists(dest_dir):
	    os.makedirs(dest_dir)

    os.chdir(dest_dir)

    tags_image = []


    for i, url in enumerate(img_urls):
        image_name = f'img{i}'

        response = urllib.request.urlopen(url)

        image = open(image_name, "wb")

        image.write(response.read())

        tags_image.append('<img src="{0}">'.format(image_name))

    html_file = open("index.html", "w")
    html_file.write("<html><body>{0}</body></html>".format(''.join(tags_image)))

def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')
    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        'usage: [--todir dir] logfile'
        sys.exit(1)

    value = parser.parse_args(args)

    img_urls = read_urls(value.logfile)

    if value.todir:
        download_images(img_urls, value.todir)
    else:
        print('\n'.join(img_urls))

    
    # parsed_args = parser.parse_args(args)
    # img_urls = read_urls(parsed_args.logfile)
    # if parsed_args.todir:
    #     download_images(img_urls, parsed_args.todir)
    # else:
    #     print('\n'.join(img_urls))

if __name__ == '__main__':
    main(sys.argv[1:])

