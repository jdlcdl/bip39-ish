"""
A BIP-39 4-CHAR-per-word table w/ row+column hex labels to index each english word
"""

import requests

from embit.bip39 import WORDLIST as embit_WORDS		# pip3 install embit
from bip39 import INDEX_TO_WORD_TABLE as bip39_WORDS	# pip3 install bip39
github_WORDS = tuple(requests.get(
    'https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt'
).text.split())

# everyone uses the same english BIP-39 words list
assert tuple(embit_WORDS) == bip39_WORDS == github_WORDS
WORDS = github_WORDS

# four characters are enough to uniquely identify each BIP-39 word
assert len(set([word[:4] for word in WORDS])) == len(WORDS)

# Use the row label as the first two nibbles -- and the column label as the last nibble
# of a 3-nibble hex number to index each word in the BIP-39 words list.
col_labels = 'BIP-39' + ' '.join([' __{:X}'.format(i) for i in (range(16))])
for row in range(128):
    if row % 64 == 0:
        print('\n' + col_labels)
    row_label = '0x{:02X}_ '.format(row)
    i, j = row*16, row*16+16
    print(row_label + ' '.join(['{:4s}'.format(word[:4]).upper() for word in WORDS[i:j]]))

