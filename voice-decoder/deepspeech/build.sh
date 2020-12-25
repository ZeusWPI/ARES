#!/bin/bash
python3 generate_vocab.py
python3 downloaded_client/generate_lm.py --input_txt vocab.txt --output_dir output_model --top_k 500000 --kenlm_bins /usr/bin/ --arpa_order 5 --max_arpa_memory "85%" --arpa_prune "0|0|1" --binary_a_bits 255 --binary_q_bits 8 --binary_type trie --discount_fallback
./downloaded_client/generate_scorer_package --alphabet ./alphabet.txt --lm output_model/lm.binary --vocab output_model/vocab-500000.txt --package kenlm.scorer --default_alpha 0.931289039105002 --default_beta 1.1834137581510284
