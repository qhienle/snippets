#!/usr/bin/env python3
"""
Convert [Mermaid code](https://mermaid.ai/open-source/intro/) to an image file (PNG).

USAGE:  python mmd2img.py --help
        python mmd2img.py < diagram.mmd
        python mmd2img.py << 'EOF'
        flowchart LR
            A(["Sequence"]) --> |"BCL"| B["BCL-Convert<br/>(local)"]
            ...
        EOF
        echo '...' | python mmd2img.py
"""

import sys
import argparse
import logging
import base64
import requests

__version__ = "0.1"

# class Mermaid:
#     """
#     Mermaid class
#     """
#     def __init__(self):
#         """
#         Initialize Class
#         """
#         pass


def parse_args():
    """
    Parse command-line options
    """
    parser = argparse.ArgumentParser(description="Convert Mermaid diagrams to image files (PNG)")
    parser.add_argument('mmd', nargs='?', default='-', help="Mermaid code or '-' for stdin")
    # parser.add_argument('-o', '--optional', help="Optional argument")
    # parser.add_argument('-f', '--flag', action="store_true", help="Optional flag")
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


def mmd2img(mmd):
    """
    Exports Mermaid diagram code to PNG
    """
    encoded = base64.urlsafe_b64encode(mmd.encode()).decode()
    url = f"https://mermaid.ink/img/{encoded}"
    img_data = requests.get(url).content
    with open("mmd.png", "wb") as f:
        f.write(img_data)


def main(args):
    """
    Main function
    """
    mmd = sys.stdin.read() if args.mmd == '-' else args.mmd
    mmd2img(mmd)
    print("Done.")
    return 0


if __name__ == '__main__':
    args = parse_args()
    configure_logging(args.level)
    sys.exit(main(args))
