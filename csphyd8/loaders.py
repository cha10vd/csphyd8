from cspy.alpha.molecule import Molecule  # type: ignore
from cspy.alpha.hydCrystal import HydCrystalStructure  # type: ignore
from typing import List


def load_molecule(fname: str) -> Molecule:
    """Function used to load guest molecule used in insertion
    algorithms.

    Parameters
    ----------
    fname: str
        input `.xyz` filename.

    Returns
    -------
    mol: Molecule
        CSPY ``Molecule``-type object.

    Raises
    ------
    IOError
        Raised when file not found based on path provided.
    """
    mol = Molecule()
    mol.init_from_xyz(fname)
    mol.center()

    print('Centroid: ', mol.centroid())

    return mol


def load_crystals(fname: str) -> List[HydCrystalStructure]:
    """Takes in a `.res` file, potentially with many structures and
    instantiates a ``HydCrystalStructure`` object for each, generating
    the correct symmetry operation list for each molecule along the
    way.

    Parameters
    ----------
    fname: str
        input `.res` filename.

    Returns
    -------
    structures: List[HydCrystalStructure]
        List containing all structures for guest insertion.

    Raises
    ------
    IOError
        Raised when file not found based on path provided.
    """
    structures: List[HydCrystalStructure] = []

    with open(fname, 'r') as f:
        raw_data: str = f.read()

    data: List[str] = raw_data.split('\n\n')

    for i, entry in enumerate(data):
        if not entry.isspace():
            tmp = HydCrystalStructure()
            tmp.init_from_res_string(entry)
            tmp.generate_symmetry_operation()
            tmp.name = str(i)
            structures.append(tmp)

    return structures


if __name__ == '__main__':

    TESTROOT = '../tests/'
    TESTNAME = '1-loaders/'

    TESTDIR = TESTROOT + TESTNAME

    guest_file = TESTDIR + 'h2o.xyz'
    host_file = TESTDIR + 'dipica_min.res'

    molecule = load_molecule(guest_file)
    crystals = load_crystals(host_file)
