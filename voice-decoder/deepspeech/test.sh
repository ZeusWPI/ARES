#!/bin/bash
if [ $# -lt 1 ]; then
    echo "Needs a .wav file as argument"
    exit 1
fi

sox "$1" --bits 16 --encoding signed-integer -c1 -r 8000 -L -t wav /dev/stdout \
| qemu-arm downloaded_client/md380-emu -e -i /dev/stdin -o /dev/stdout \
| qemu-arm downloaded_client/md380-emu -d -i /dev/stdin -o /dev/stdout \
| sox --buffer 256 -r 8000 -e signed-integer -L -b 16 -c 1 -t raw /dev/stdin -r 16000 -c1 /tmp/audio.wav

deepspeech --model deepspeech-0.9.3-models.tflite --scorer kenlm.scorer --audio /tmp/audio.wav 2>/dev/null
aplay /tmp/audio.wav 2>/dev/null
