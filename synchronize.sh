#!/bin/bash

python3 cv/generate_tex.py && \
cd cv && pdflatex hyoungjookim.tex && cd ..
