# textrain

Generate pdf document and get bounding boxes for words.

The `textrain` module can be run as follows

```bash
python -m textrain word1 word2 ... wordn
```

which generates a PDF file `out.pdf` and outputs the following CSV:

```csv
word,posx,posy,depth
word1,8799518,47171296,0.0pt
word2,11750462,46515936,0.0pt
ellipsis,13718366,46515936,1.94444pt
wordn,15837366,46515936,0.0pt
```

The `x` and `y` positions can be used to get the bounding box of each word in
the PDF document.
