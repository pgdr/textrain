# textrain

Get png images for words

The `textrain` module can be run as follows

```bash
python -m textrain word1 word2 ... wordn
```

which generates one png file for each word.

## Example

Running

```bash
python -m textrain kristian flikka lol
```

generates three images:

* `kristian-1.png`
* `flikka-1.png`
* `lol-1.png`

![kristian-1](https://raw.githubusercontent.com/pgdr/textrain/master/assets/kristian-1.png)
![flikka-1](https://raw.githubusercontent.com/pgdr/textrain/master/assets/flikka-1.png)
![lol-1](https://raw.githubusercontent.com/pgdr/textrain/master/assets/lol-1.png)


Generating a pangram:
```
python -m textrain the quick brown fox jumps over the lazy dog
```

To generate all the letters in the alphabet, you might have to do a silly hack.
The command `textrain a b c d e` will unfortunately interpret "abcde" as the
only word, instead of three 1-letter words.  This can be circumvented by running
`textrain omg a b c d e ...`
