#!/bin/bash
pyenv exec sphinx-apidoc -o source/_FTE_autodoc ../FTE
make clean html
cp -r build/html/* ../docs
