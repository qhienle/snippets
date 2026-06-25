#!/usr/bin/env python3
"""
Convert [Mermaid code](https://mermaid.ai/open-source/intro/) to an image file (PNG).

USAGE: mmd2img.py --help
"""

import sys
import os
import argparse
import logging

__version__ = "0.1"

class Mermaid:
    """
    Mermaid class
    """
    def __init__(self):
        """
        Initialize Class
        """
        pass


def parse_args():
    """
    Parse command-line options
    """
    parser = argparse.ArgumentParser(description="Convert Mermaid diagrams to image files (PNG)")
    parser.add_argument('mmd', help="Mermaid code [REQUIRED]")
    parser.add_argument('-o', '--optional', help="Optional argument")
    parser.add_argument('-f', '--flag', action="store_true", help="Optional flag")
    parser.add_argument('--logging-level', '-l', dest='level', default='info',
                        help="Logging level (str), can be 'debug', 'info', 'warning'. Default='info'")
    return parser.parse_args()


def configure_logging(level):
    """
    Set logging level, based on the level names of the `logging` module.
    - level (str): 'debug', 'info' or 'warning'
    """
    if level == 'debug':
        level_name = logging.DEBUG
    elif level == 'info':
        level_name = logging.INFO
    else:
        level_name = logging.WARNING
    logging.basicConfig(level=level_name, 
                        format='[%(asctime)s] %(levelname)s: %(message)s', 
                        datefmt='%Y-%m-%d@%H:%M:%S')


def main(args):
    """
    Main function
    """
    args = parse_args()
    configure_logging(args.level)
    _test(args)


if __name__ == '__main__':
    sys.exit(main())
