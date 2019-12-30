from loaders import load_molecule, load_crystals
from expander import expand_cryst
from perturbator import perturb_mol
from check_overlap_slow import check_overlap, check_overlap2
from supercell import make_supercell
from symmetry  import cartesian_symm_ops, make_images
from make_cspy_obj import make_mol, make_cryst
import numpy as np
from copy import deepcopy

#from distributed import Client, LocalCluster

def reoptimize(trial):
    with open(trial.name, 'a') as f:
        f.write(trial.res_string_form())


def gen_guests(structure, guest, trial_xyz, trial_rad):

    def filter_hits(xyz, hits):
        xyz = xyz[:,:,hits]
        return xyz

    voids, v, expansion = expand_cryst(structure)
    if voids is 0:
        return []
    # 1. Make supercell of original crystal and get
    #    their respective symmetry operations.
    sc_xyz, sc_rad = make_supercell(structure)
    symm_ops  = cartesian_symm_ops(structure)
    # 2. Shift all trials to crystal space.
    nVoids = len(voids)
    trials = np.array_split(trial_xyz, nVoids, axis=-1)
    for i, void in enumerate(voids):
        trials[i]    = trials[i] + np.array(void])[:,None,None]
    trials = np.dstack(trials)
    # 3. Check for host-guest overlap and filter results
    hits      = check_overlap(sc_xyz, sc_rad, trials, trial_rad, 1.1)
    print(hits)
    trials    = filter_hits(trials, hits)
    # 4. Generate symmetry related copies of accepted 
    #    guests and check guest-image overlap
    sc_xyz, sc_rad = make_images(trials, trial_rad, symm_ops)
    hits      = check_overlap2(sc_xyz, sc_rad, trials, trial_rad, 1.1)
    trials    = filter_hits(trials,hits)

    return structure, expansion, trials

def insert_guests(structure, trials):
    crystals =  make_cryst(structure, guest, trials)

def reoptimize_inserts(crystal_list, fname):

    _MF_ROOT = '/scratch/vdn1m17/multipoles/'

    for crystal in crystal_list:
        crystal.neighcrys_args['multipole_file'] = _MF_ROOT + fname
        crystal.stdMin()

    return crystal_list

def make_res_file(structure_list, fname='inserts.res'):
    res_str = ''
    for structure in structure_list:
        res_str += structure.res_string_form() + '\n\n'

    with open(fname, 'w') as f:
        f.write(res_str)

if __name__ == '__main__':

    guest = load_molecule('../tests/6-complete/h2o.xyz')
    trial_xyz, trial_rad  = perturb_mol(guest)
    structures = load_crystals('../tests/6-complete/dipica_mixed_anhyd.res')


    for structure in structures[5:6]:
        guests = gen_guests(structure, guest, trial_xyz, trial_rad)
    make_res_file(guests)
    #structures = minimize_structures()
