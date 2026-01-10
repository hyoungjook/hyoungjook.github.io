#!/bin/bash

rm -rf .git/ && \
git init && \
git add -A && \
git commit -m "update" && \
git remote add origin https://github.com/hyoungjook/hyoungjook.github.io.git && \
git push --force origin main
