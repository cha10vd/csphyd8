from cspy.alpha.crystal import CrystalStructure
from cspy.alpha.molecule import Molecule
from copy import deepcopy

def make_mol(xyz_list, molecule):
    molecules = []
    nat = molecule.num_atoms()
    for trial_id in range(xyz_list.shape[2]):
        try:
            mol = deepcopy(molecule)
            xyz = xyz_list[:,:,trial_id].T

            for i in range(nat):
                mol.atoms[i].xyz = xyz[i,:]
            molecules.append(mol)
        except:
            pass

    return molecules

def make_cryst(cryst, mol, xyz, idx):
    molecules = make_mol(xyz, mol)
    crystals = []
    for i, mol in enumerate(molecules):
        try:
            c = deepcopy(cryst)
            c.unique_molecule_list.append(mol)
            c.name += ' insert {}'.format(str(idx[i]))
            c.update_sfac()
            crystals.append(c)
        except:
            pass

    return crystals

