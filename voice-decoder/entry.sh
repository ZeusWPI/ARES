#!/bin/bash
WATCHPATH="${1:-/app/shared}"


inotifywait -m "$WATCHPATH" -e create -e moved_to |
    while read dir action file; do
        FULLPATH="$dir$file"
        WORDS=$(deepspeech --model deepspeech/deepspeech-0.9.3-models.tflite --scorer deepspeech/kenlm.scorer --audio "$FULLPATH")
        python3 verify.py "$WORDS" "$file" secrets.json
        rm "$FULLPATH"
    done
