#!/bin/bash
# composite every frame, encode final.mp4, side-by-sides, QC
set -e
mkdir -p out/desk
# (composite already up to date when called with SKIP_COMP=1)
[ -z "$SKIP_COMP" ] && { for r in "0 89" "90 179" "180 269" "270 359"; do set -- $r; python3 tools/${COMPOSITOR:-composite_photo}.py $1 $2 & done; wait; }
ffmpeg -v error -y -framerate 30 -i out/desk/%04d.png -i out/audio_norm.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -profile:v high -r 30 -c:a aac -b:a 192k -shortest -movflags +faststart out/final.mp4
# reference left, mine right (both 1080x1920), my audio
ffmpeg -v error -y -i ref/reference.mp4 -i out/final.mp4 -filter_complex "[0:v]scale=1080:1920:flags=lanczos,tpad=stop_mode=clone:stop_duration=1,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]hstack=inputs=2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='REFERENCE':x=40:y=1850:fontsize=40:fontcolor=white@0.8,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='CYWEB':x=1120:y=1850:fontsize=40:fontcolor=white@0.8[v]" -map "[v]" -map 1:a -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -t 12 -movflags +faststart out/side_by_side.mp4
# flat screen films: reference unwarped left, mine right
ffmpeg -v error -y -framerate 30 -i ref/flat/%04d.png -framerate 30 -i film/out/%04d.png -filter_complex "[0:v]scale=960:540[a];[1:v]scale=960:540[b];[a][b]hstack=inputs=2[v]" -map "[v]" -c:v libx264 -crf 18 -pix_fmt yuv420p out/side_by_side_screen.mp4
python3 tools/qc.py
