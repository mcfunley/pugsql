#!/usr/bin/env python
import pkg_resources
import pugsql
import sys

dver = pkg_resources.get_distribution('pugsql').version
initver = pugsql.__version__

if dver != initver:
    print('Version in __init__ (%s) does not match '
          'distribution version (%s)' % (dver, initver))
    sys.exit(1)
