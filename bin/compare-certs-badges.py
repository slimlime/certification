#!/usr/bin/env python

'''Compare certificates with badges and report mis-matches.'''

import sys
import os
import glob

def main():
    assert len(sys.argv) == 3, \
           'Usage: {0} /path/to/certificates/root /path/to/site/root'.format(sys.argv[0])

    cert_root = sys.argv[1]
    site_root = sys.argv[2]

    for flavor in ['instructor']:
        certs = get(os.path.join(cert_root, flavor), '.pdf')
        badges = get(os.path.join(site_root, 'badges', flavor), '.json')
        report(flavor, 'certificates without badges', certs - badges)
        report(flavor, 'badges without certificates', badges - certs)

def get(path, suffix):
    return set([os.path.splitext(os.path.split(x)[1])[0] for x in glob.glob(path + '/*' + suffix)])

def report(flavor, title, entries):
    if entries:
        print '{0}: {1}'.format(flavor, title)
        for e in sorted(list(entries)):
            print '  {0}'.format(e)

if __name__ == '__main__':
    main()
