from cspy.alpha.hydCrystal import HydCrystalStructure
from cspy.alpha.molecule import Molecule
import numpy as np

def make_supercell(cryst: HydCrystalStructure, exp_lv: int=2, labels: bool=False):
    """Generates a crystal supercell against which to test for molecular
    overlap

    Parameters
    ----------

    Returns
    -------

    Raises
    ------
    """

    bonds_dictionary = Molecule.bonds_dictionary

    from copy import deepcopy
    p1_lat = deepcopy(cryst)
    p1_lat.expand_to_full_unit_cell()
    p1_lat.move_all_molecules_into_uc()
    superc = p1_lat.generate_supercell(size=exp_lv)

    xyz = []
    rad = []
    lab = []

    for mol in superc:
        for atom in mol.atoms:
            xyz.append(np.array(atom.xyz))
            rad.append([bonds_dictionary[(atom.clean_label(), l)] for l in
                                         ["O","H","H"]])
            lab.append(atom.clean_label())

    xyz = np.stack(xyz,axis=0).T
    rad = np.array(rad, dtype=np.double)

    if not labels:
        return xyz, rad
    else:
        return xyz, rad, lab

if __name__ == '__main__':

    def make_xyz(xyz, lab):
        f = open('../tests/3-supercell/supercell.xyz', 'w')
        nat = len(lab)
        f.write(str(nat) + '\n\n')
        for i in range(nat):
            f.write('{}\t{:.6f} {:.6f} {:.6f}\n'.format(lab[i], *xyz[:,i]))
        f.close()

    test = HydCrystalStructure()
    test.init_from_res_file('../tests/3-supercell/dipica_min.res')
    xyz, rad, lab = make_supercell(test, labels=True)
    #make_xyz(xyz, lab)

