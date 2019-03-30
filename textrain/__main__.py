#!/usr/bin/env python

import textrain

def main(args):
    textrain.main(args)

if __name__ == '__main__':
    from sys import argv
    if len(argv) < 2:
        exit('Usage: textrain word1 word2 ... wordn')
    main(argv[1:])
