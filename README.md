Correlation consistent Gaussian basis sets for solids
=====================================================

- [How to use](#how-to-use)
- [How to cite](#how-to-cite)
- [Contact](#contact)
- [Background](#background)

How to use
----------

The basis set data files for different pseudopotentials/effective core potentials can be found in the [basis](basis) folder. 
The following are currently available.

| PP/ECP | cc-pVXZ  | Elements |
| ------ | -------- | -------- |
| GTH-HF | DZ ~ QZ  | H ~ Ar   |
| ccECP  | DZ ~ QZ  | H ~ Ar   |

| PP/ECP | aug-cc-pVXZ  | Elements |
| ------ | ------------ | -------- |
| GTH-HF | DZ ~ QZ      | He,Ne,Ar |
| ccECP  | DZ ~ QZ      | Currently not available |

All basis sets are provided in the NWChem format, which is recognizable by most quantum chemistry software packages.
An example of their use with [PySCF](https://github.com/pyscf/pyscf) can be found in [example](example).

How to cite
-----------

Please cite the following work in publications utilizing our basis sets:

- [Correlation-Consistent Gaussian Basis Sets for Solids Made Simple](https://pubs.acs.org/doi/10.1021/acs.jctc.1c01245), H.-Z. Ye and T. C. Berkelbach, *J. Chem. Theory Comput.*, (2022). doi: [10.1021/acs.jctc.1c01245](https://doi.org/10.1021/acs.jctc.1c01245)

Contact
-------

For bug report and feature request, please contact
- Hong-Zhou Ye, hzyechem@gmail.com

Background
----------

The following is a short introduction of Gaussian basis sets in general and their application in solid materials calculations in particular. For more details, see our [paper](#how-to-cite).

* Gaussian basis set: what and what for?

In the quantum mechanical simulation of chemical systems, the electronic wave function is expanded in a set of single-particle basis functions called a basis set. The basis functions are often chosen to be *atom-centered Gaussian-type orbitals*, and the correpsonding basis set is called *Gaussian basis set*. Decades of studies have shown that Gaussian basis sets are compact and fast convergent to the complete basis set limit for chemical applications, especially in correlated wave function calculations. For molecular systems, well-established Gaussian basis sets have been developed, benchmarked, and widely used for decades. They are available from e.g., the [Basis Set Exchange](https://www.basissetexchange.org/) website. Of special interest is the correlation consistent Gaussian basis set, the `cc-pVXZ` series due to [Dunning's work](https://aip.scitation.org/doi/10.1063/1.456153) in 1989, which is the go-to choice for correlated wave function calculations.

* Why re-development is needed for solids?

For solids or other periodic systems where atoms are *densely* packed, the overlap matrix of the basis set can become highly singular (condition number greater than e.g., 10^10), leading to numerical issues such as convergence issues in self-consistent field (SCF), discontinuities in correlated calculations, etc.. Proposed fixes in the literature include discarding the few most diffuse functions or re-optimizing the basis set parameters for solids, which will necessarily degrade the quality of the original basis set and/or lose its transferability. A more systematic scheme is thus needed that can eventually lead to a standard library of Gaussian basis sets for solids.

* Our approach

Our approach towards solving this problem follows closely Dunning's construction of the correlation consistent Gaussian basis set family. Specifically, we avoid the high linear dependency issue of the original `cc-pVXZ` basis sets by *limiting the length of the valence basis*. The correlation consistency of the basis sets is maintained by keeping the structure of the polarization functions unchanged (e.g., `1d` for DZ, `2d1f` for TZ, `3d2f1g` for QZ etc.). The resulting basis sets have been benchmarked to show fast convergence to the complete basis set limit in both mean-field and correlated simulation of solids (see our [paper](#how-to-cite) for details).
