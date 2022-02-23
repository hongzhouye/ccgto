r''' The basis set data files provided by this repo are all in the NWChem format.
This script demonstrates how to use them in PySCF.
'''

import numpy as np

from pyscf.pbc import gto, scf
from pyscf.gto.basis import parse_nwchem


if __name__ == '__main__':

# load cc-pvdz for B and N
    basname = 'cc-pvdz'
    fbas = '../basis/gth-hf-rev/%s-lc.dat' % basname
    atms = ['B', 'N']
    basis = {atm:parse_nwchem.load(fbas, atm) for atm in atms}
    print(basis)

# use the loaded basis sets to construct a Cell object
    atom = 'B 0 0 0; N 0.90399994 0.90399994 0.90399994'
    a = np.array([
            [0.        , 1.80799987, 1.80799987],
            [1.80799987, 0.        , 1.80799987],
            [1.80799987, 1.80799987, 0.        ]
        ])
    cell = gto.M(atom=atom, a=a, basis=basis, pseudo='gth-hf-rev')
    cell.mesh = [21,21,21] # save cost
    cell.build()
    cell.verbose = 4

# Gamma point HF calculation
    mf = scf.RHF(cell)
    mf.kernel()
