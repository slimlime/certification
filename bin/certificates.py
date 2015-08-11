#!/usr/bin/env python

'''
Generate a certificate from a template.  On a Mac, a typical command line is

python bin/certificates.py \
       -i /Applications/Inkscape.app/Contents/Resources/bin/inkscape \
       -s $HOME/certification/instructor.svg \
       -o $HOME/certification/instructor/turing.alan.pdf \
       date='January 24, 1924' \
       instructors='Ada Lovelace' \
       name='Alan Turing'
'''

import sys
import os
import re
from optparse import OptionParser
import tempfile
import subprocess
import unicodedata

def main():
    args = parse_args()
    template = open(args.svg_file).read()
    check(template, args.params)
    tempfile = create_svg(template, args.params)
    svg_to_pdf(args.inkscape, tempfile, args.out_file)

def parse_args():
    '''Get command-line arguments.'''

    parser = OptionParser()
    parser.add_option('-s', '--svg', default=None, dest='svg_file', help='SVG template filename')
    parser.add_option('-i', '--ink', default='/Applications/Inkscape.app/Contents/Resources/bin/inkscape',
                      dest='inkscape', help='Path to Inkscape')
    parser.add_option('-o', '--out', default=None, dest='out_file', help='Output filename')

    args, extras = parser.parse_args()
    assert args.svg_file is not None, 'No SVG template filename given (use -s/--svg)'
    assert args.inkscape is not None, 'Path to Inkscape not given (use -i/--ink)'
    assert args.out_file is not None, 'No output filename given (use -o/--out)'

    args.params = extract_parameters(extras)
    return args

def extract_parameters(args):
    '''Extract key-value pairs (checking for uniqueness).'''
    result = {}
    for a in args:
        fields = a.split('=')
        assert len(fields) == 2, 'Badly formatted key-value pair "{0}"'.format(a)
        key, value = fields
        assert key not in result, 'Duplicate key "{0}"'.format(key)
        result[key] = value
    return result

def check(template, params):
    '''Check that all values required by template are present.'''
    expected = re.findall(r'\{\{([^}]*)\}\}', template)
    missing = set(expected) - set(params.keys())
    assert not missing, 'Missing parameters required by template: {0}'.format(' '.join(missing))

def create_svg(template, params):
    '''Create a new SVG file from the template.'''

    svg = template
    for key, value in params.items():
        pattern = '{{' + key + '}}'
        svg = svg.replace(pattern, value)

    tmp = tempfile.NamedTemporaryFile(suffix='.svg')
    tmp.write(svg)
    tmp.flush()

    return tmp

def svg_to_pdf(inkscape, tempfile, output_file):
    '''Convert SVG certificate (filled in) to PDF.'''

    subprocess.call([inkscape,
                     '--export-pdf', output_file,
                     tempfile.name,
                     '--export-dpi', '600'])

if __name__ == '__main__':
    main()
