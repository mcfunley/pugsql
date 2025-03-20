#!/usr/bin/env python
import importlib.metadata
import sys

import pugsql

dver = importlib.metadata.version("pugsql")
initver = pugsql.__version__

if dver != initver:
    print(
        "Version in __init__ (%s) does not match "
        "distribution version (%s)" % (dver, initver)
    )
    sys.exit(1)
