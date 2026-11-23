#!/bin/bash
# render a list of 1-based reference frame numbers (single sub-frame unless N given) into film/out
N=${N:-1}
for f in "$@"; do k=$((f-1)); node tools/render_film.js $k $k $N | python3 tools/avg.py film/out; done
