#!/bin/bash
pyinstaller --noconsole --name epidem.io --onefile src/ihm.py --distpath ./src/bin
rm -r ./build
rm epidem.io.spec