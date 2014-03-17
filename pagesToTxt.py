#!/usr/bin/env python2

from __future__ import print_function
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

CONVERSION_CMD = 'pdftotext'
PDF_PATH = 'QuickLook/Preview.pdf'

def main():
    for f in sys.argv[1:]:
        convert_file(f)


def convert_file(path):
    if not os.path.isfile(path):
        print('Given path,', path + ',', 'is not a valid file.',
              file=sys.stderr)
        return

    try:
        zip_file = zipfile.ZipFile(path, 'r')
    except zipfile.BadZipfile as e:
        print('Given file,', path + ',', 'is not a valid pages file.',
              file=sys.stderr)
    else:
        with zip_file.open(PDF_PATH) as pdf, tempfile.NamedTemporaryFile() as tmp_file:
            shutil.copyfileobj(pdf, tmp_file.file)
            tmp_file.file.seek(0)
            convert_pdf_to_txt(tmp_file.name, path + '.txt', path)


def convert_pdf_to_txt(pdf_path, txt_path, original_name):
    try:
        subprocess.check_call([CONVERSION_CMD, pdf_path, txt_path])
    except subprocess.CalledProcessError as e:
        print('Unable to convert file,', original_name + '.', e,
              file=sys.stderr)


if __name__ == '__main__':
    main()
