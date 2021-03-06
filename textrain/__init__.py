#!/usr/bin/env python3
import os
import shutil
import tempfile
import contextlib
from xml.etree import ElementTree as ET
from collections import namedtuple

__version__ = '0.0.2'


## UTIL

@contextlib.contextmanager
def tmp():
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        name = tmpdir
        os.chdir(name)
        yield name  # give control to caller scope
    os.chdir(cwd)


def _format(text, replacement):
    return text.replace('MY_OWN_FORMAT_FUNCTION',
                        replacement)

# /UTIL

TEX = """\\nonstopmode
\\documentclass{article}
\\pagenumbering{gobble}
\\begin{document}

MY_OWN_FORMAT_FUNCTION

\\end{document}
"""


def _supligs(word):
    return '{}'.join([w for w in word])  # suppress ligatures


def tex(words):
    return _format(TEX, '\n'.join(['%s' % _supligs(word) for word in words]))


def __quiet(cmd):
    quiet = ' >/dev/null 2>&1'
    if not os.getenv('VERBOSE'):
        cmd += quiet
    return cmd


def __run_raise(cmd, msg=None):
    ret = os.system(__quiet(cmd))
    if ret:
        if msg is None:
            msg = '{} exit with status {}'.format(cmd, ret)
        raise OSError(msg)


def __compile(get_fname):
    cmd = 'pdflatex -interaction=batchmode {}'
    __run_raise(cmd.format(get_fname('tex')))
    __run_raise(cmd.format(get_fname('tex')))  # for references

    return get_fname('pdf')


def __bbox(get_fname):
    cmd = 'pdftotext -bbox {}'.format(get_fname('pdf'))
    __run_raise(cmd)
    root = ET.parse(get_fname('html')).getroot()
    body = root.getchildren()[1]
    doc = body.getchildren()[0]
    return doc

coords = namedtuple('coords', 'left bottom right top')
def __word_coord(page_attrib, word_attrib):
    # left bottom right top
    ph, xMin, yMax, xMax, yMin = (float(v) for v in
                                  (page_attrib['height'],
                                   word_attrib['xMin'],
                                   word_attrib['yMax'],
                                   word_attrib['xMax'],
                                   word_attrib['yMin']))
    return coords( xMin, ph - yMax, xMax, ph - yMin, )

def __extract_imgs(page):
    return {
        word.text : __word_coord(page.attrib,
                            word.attrib)
        for word in page.getchildren()
        }


def generate_pdf(tex_str):
    fname = lambda ext : os.path.abspath('__generated.{}'.format(ext))
    with open(fname('tex'), 'w') as out:
        out.write(tex_str)

    pdf_path = __compile(fname)
    doc = __bbox(fname)
    page = doc.getchildren()[0]

    return page


def __convert_imgs(bboxen):
    crop_cmd = 'pdfcrop -bbox "{left} {bottom} {right} {top}" __generated.pdf'
    conv_cmd = 'pdftoppm __generated-crop.pdf {f} -png'
    for word, bbox in bboxen.items():
        print(word, bbox)
        crop = crop_cmd.format(left=bbox.left, bottom=bbox.bottom-1,
                               right=bbox.right, top=bbox.top+1)
        __run_raise(crop)
        conv = conv_cmd.format(f=word)
        __run_raise(conv)


def run(words):
    tex_content = tex(words)
    home = os.path.abspath(os.getcwd())
    with tmp():
        page = generate_pdf(tex_content)
        lst = __extract_imgs(page)
        __convert_imgs(lst)
        cmd = 'cp *png ' + home
        __run_raise(cmd)


def main():
    from sys import argv
    if len(argv) < 2:
        exit('Usage: textpos word1 word2 ... wordn')

    run(argv[1:])

if __name__ == '__main__':
    main()
