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


TODO: use `pdftotext -bbox` and parse HTML instead of homemade bbox.

1. `pdftotext -bbox in.pdf`
2. Extract `<page>`'s `height` attribute (e.g. `841.89`)
3. Crop pdf to a standalone pdf by using `pdfcrop`: `pdfcrop -bbox "xMin height-yMax xMax height-yMin" in.pdf
4. `pdftoppm in-crop.pdf outputname -png`

Repeat
