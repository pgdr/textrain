#!/usr/bin/env python3
import os
import shutil
import tempfile
import contextlib

## UTIL

@contextlib.contextmanager
def tmp(path=None, teardown=True):
    """Create and go into tmp directory, returns the path.

    This function creates a temporary directory and enters that directory.  The
    returned object is the path to the created directory.

    If @path is not specified, we create an empty directory, otherwise, it must
    be a path to an existing directory.  In that case, the directory will be
    copied into the temporary directory.

    If @teardown is True (defaults to True), the directory is (attempted)
    deleted after context, otherwise it is kept as is.

    """
    cwd = os.getcwd()
    fname = tempfile.NamedTemporaryFile().name

    if path:
        if not os.path.isdir(path):
            raise IOError('No such directory: %s' % path)
        shutil.copytree(path, fname)
    else:
        # no path to copy, create empty dir
        os.mkdir(fname)

    os.chdir(fname)

    yield fname  # give control to caller scope

    os.chdir(cwd)

    if teardown:
        try:
            shutil.rmtree(fname)
        except OSError as oserr:
            shutil.rmtree(fname, ignore_errors=True)


def _format(text, replacement):
    return text.replace('MY_OWN_FORMAT_FUNCTION',
                        replacement)

# /UTIL


TEX = ''
with open('data/template.tex', 'r') as __tex_in:
    TEX = ''.join(__tex_in.readlines())

def tex(words):
    return _format(TEX, '\n'.join(['\\train{%s}' % word for word in words]))


def generate_tex(tex_str):
    old_cwd = os.getcwd()
    home = lambda f : os.path.abspath(os.path.join(old_cwd, f))
    with tmp():
        fname = lambda ext : '__generated.{}'.format(ext)
        with open(fname('tex'), 'w') as out:
            out.write(tex_str)
        os.system('pdflatex {}'.format(fname('tex')))
        os.system('pdflatex {}'.format(fname('tex')))  # for references
        pdf_path, csv_path =  (os.path.abspath(fname('pdf')),
                               os.path.abspath(fname('csv')))
        os.system('cp {} {}'.format(pdf_path, home('out.pdf')))
        csv_content = ''
        with open(csv_path, 'r') as csv_file:
            csv_content = ''.join(csv_file.readlines())
    return home('out.pdf'), csv_content

def main(words):
    tex_content = tex(words)
    pdf, csv = generate_tex(tex_content)
    print(pdf)
    print(csv)

if __name__ == '__main__':
    from sys import argv
    if len(argv) < 2:
        exit('Usage: textpos word1 word2 ... wordn')
    main(argv[1:])
