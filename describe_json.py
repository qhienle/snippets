#!/usr/bin/env python3
"""
describe_json

Describe the schema of a JSON file.

USAGE:
    describe_json.py [--indent\-i=4] path/to/file.json
    describe_json.py file.json
    describe_json.py --help
"""

import sys
import argparse
import json
from genson import SchemaBuilder

__version__ = "0.1"

def parse_args():
    """
    Parse command-line options
    """
    parser = argparse.ArgumentParser(description="Describe the schema of a JSON file")
    parser.add_argument('file', help="Path to JSON file [REQUIRED]")
    parser.add_argument('--indent', '-i', default=4, help="[int] whitespace for indentation. Default=4")
    return parser.parse_args()


def main(args):
    args = parse_args()
    with open(args.file) as fh:
        SchemaBuilder().add_object(json.load(fh))
    print(SchemaBuilder().to_json(indent=4))

if __name__ == '__main__':
    sys.exit(main())

"""
---
references:
  - "File: /describe_json.py"
generationTime: 2026-06-10T19:50:35.584Z
---
flowchart TD
    A(["Start"]) --> B["parse_args()"]
    B --> C{{"File argument provided?"}}
    C -->|No| D["Display help/error"]
    D --> E(["Exit with error"])
    C -->|Yes| F["Open JSON file"]
    F --> G{{"File opens successfully?"}}
    G -->|No| H["Log file error"]
    H --> E
    G -->|Yes| I["Read JSON content"]
    I --> J["Create SchemaBuilder instance"]
    J --> K["Add JSON object to builder"]
    K --> L["Generate schema"]
    L --> M["Format with indent=4"]
    M --> N["Print schema to stdout"]
    N --> O(["Exit with success"])
"""
