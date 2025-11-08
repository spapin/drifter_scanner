"""
Entry point for running drifter_scanner as a module.
"""
import sys
from drifter_scanner.daemon import main

if __name__ == "__main__":
    sys.exit(main())
