''' Turn NWChem basis into CP2K format.

This script does NOT require PySCF installation.
'''


import sys
import numpy as np

LSTRS = 'SPDFGHIKLMN'


def parse_nwchem(fbas):
    fdata = open(fbas, 'r').read().rstrip('\n').split('\n')
    loc = np.asarray([i+1 for i,dat in enumerate(fdata) if dat.startswith('#BASIS SET')] +
                     [len(fdata)+1])
    nset = len(loc) - 1
    basis_data = ['\n'.join(fdata[loc[i]:loc[i+1]-1]) for i in range(nset)]
    return basis_data


'''
He DZVP-GTH
  2
  1  0  0  5  2
       13.1305278312  -0.0500802904   0.0000000000
        4.1977275150  -0.1474339352   0.0000000000
        1.3647725570  -0.3245281495   0.0000000000
        0.4549715461  -0.4365284986   0.0000000000
        0.1513197845  -0.2164629317   1.0000000000
  2  1  1  1  1
        1.2750000000   1.0000000000
'''

def to_cp2k(basis_str, basisname):
    bdata = basis_str.lstrip('\n').rstrip('\n').split('\n')
    atm = bdata[0].split()[0]
    loc = np.asarray([i for i,x in enumerate(bdata) if x.startswith(atm)] + [len(bdata)])
    nseg = len(loc) - 1
    sout = [f'{atm} {basisname}', f'{nseg}']
    for iseg in range(nseg):
        ANGL = bdata[loc[iseg]].split()[1]
        try:
            l = LSTRS.index(ANGL)
        except:
            raise RuntimeError('Unknown angular momentum symbol %s' % ANGL)
        i0 = loc[iseg]+1
        i1 = loc[iseg+1]
        nprim = i1 - i0
        nctr = len(bdata[i0].split()) - 1
        segtitle = f'{iseg+1} {l} {l} {nprim} {nctr}'
        sout.append( segtitle )
        sout.append( '\n'.join(bdata[i0:i1]) )
    sout = '\n'.join(sout)
    return sout

def format_cp2k(basis_data, basisname, elements=None):
    sout = []
    atms = [x.split()[0] for x in basis_data]
    if elements is None:
        elements = atms
    for atm,basis in zip(atms,basis_data):
        if atm not in elements:
            continue
        sout.append( '#BASIS SET' )
        sout.append( to_cp2k(basis, basisname) )
    sout = '\n'.join(sout)
    return sout


if __name__ == '__main__':
    try:
        input_nwchemfile = sys.argv[1]
        output_cp2kfile = sys.argv[2]
        assert( output_cp2kfile.endswith('.dat') )
        elements = sys.argv[3:]
        if len(elements) == 0:
            elements = None
    except:
        print('Usage: input_nwchemfile, output_cp2kfile [, element1, element2, ...]')
        print()
        print('Parse basis sets for specified elements from `input_nwchemfile`, format them into the CP2K format, and dump into `output_cp2kfile`.')
        print('NOTE: `output_cp2kfile` must end with \'.dat\'.')
        print()
        print('Example 1:')
        print('> python to_cp2k_format.py ../basis/gth-hf-rev/cc-pvdz-lc.dat cc-pvdz-lc.dat')
        print('# Leave `elements` blank --> parse ALL elements in the basis file')
        print()
        print('Example 2:')
        print('> python to_cp2k_format.py ../basis/gth-hf-rev/cc-pvdz-lc.dat cc-pvdz-lc.dat C N O Al Mg')
        print('# Parse specified elements from the basis file only')
        sys.exit(1)

    print('Command-line arguments:')
    print('input_nwchemfile= %s' % input_nwchemfile)
    print('output_cp2kfile= %s' % output_cp2kfile)
    print('elements= %s' % elements)

    basis_data = parse_nwchem(input_nwchemfile)
    bname = output_cp2kfile.replace('.dat', '')
    sout = format_cp2k(basis_data, bname, elements)
    open(output_cp2kfile, 'w').write(sout+'\n')
