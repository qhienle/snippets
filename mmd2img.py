#!/usr/bin/env python3
"""
Convert [Mermaid code](https://mermaid.ai/open-source/intro/) to an image file (PNG).

USAGE:  python mmd2img.py --help
        echo '...' | python mmd2img.py
        python mmd2img.py << 'EOF'
        flowchart LR
            A(["start"]) --> |"do stuf (...)"| B["end"]
        EOF
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
    parser.add_argument('code', nargs='?', default='-', help="Mermaid code or '-' for STDIN")
    parser.add_argument('--output-file', '-o', dest='output_file', default='mmd.png', help="Optional argument")
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


def mmd2img(mmd:str, output_file) -> 0:
    """
    Exports Mermaid diagram code to PNG
    - `mmd`  : Mermaid code. Ex.: "flowchart TD
                                       A['start'] --> B['end']"
    - Returns: PNG file (exit 0)
    """
    logging.debug(f"Encode code to convert {mmd}")
    encoded = base64.urlsafe_b64encode(mmd.encode()).decode()
    url = f"https://mermaid.ink/img/{encoded}"
    img_data = requests.get(url).content
    with open(output_file, "wb") as f:
        f.write(img_data)
    logging.debug(f"Wrote file {output_file}")
    return 0


def main(args):
    """
    Main function
    """
    mmd = sys.stdin.read() if args.code == '-' else args.code
    mmd2img(mmd, output_file=args.output_file)
    logging.info("Done.")
    return 0


if __name__ == '__main__':
    args = parse_args()
    configure_logging(args.level)
    sys.exit(main(args))
