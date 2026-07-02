#!/usr/bin/env python3
"""Import smoke test for the xmcinter package."""

import importlib


MODULES = [
    "xmcinter.xmcfiles",
    "xmcinter.wrangle",
    "xmcinter.xmcmap",
    "xmcinter.plots",
    "xmcinter.diagnostics",
]


def main():
    for module in MODULES:
        importlib.import_module(module)
        print(module + " ok")


if __name__ == "__main__":
    main()
