from expander import expand_cryst
from loaders import load_molecule, load_crystals
from perturbator import perturb_mol
from supercell import make_supercell
from symmetry import make_images, cartesian_symm_ops
from check_overlap_slow import check_overlap

if __name__ == '__main__':

    def xyz_print(host, host_lab, guest, guest_lab):
        nAt = 0
        FMT = '{}\t {:.4f} {:.4f} {:.4f}\n'
        xyz_string = ''
        for h in range(host.shape[1]):
            nAt += 1
            xyz_string += FMT.format(host_lab[h], *host[:,h])
        for g in range(guest.shape[1]):
            nAt += 1
            xyz_string += FMT.format(guest_lab[g%len(guest_lab)], *guest[:,g])

        xyz_string = str(nAt) + '\n\n' + xyz_string
        return xyz_string

    guest = load_molecule('../tests/5-simple_insertion/h2o.xyz')
    trial_xyz, trial_rad, trial_lab = perturb_mol(guest)

    structure = load_crystals('../tests/5-simple_insertion/expanded_dipica_min.res')[0]
    voids = expand_cryst(structure)
    structure.write_res_to_file('expanded_dipica_min.res')
    trial_xyz = trial_xyz + voids[0][:,None,None]


    sc_xyz, sc_rad, sc_lab = make_supercell(structure, labels=True)

    print(trial_xyz[:,:,0:2])

    hits = check_overlap(sc_xyz, sc_rad, trial_xyz[:,:,0:2], trial_rad, 1.0)
    print(hits)


    symm_ops = cartesian_symm_ops(structure)
    im_xyz, im_rad = make_images(trial_xyz, trial_rad, symm_ops)

    xyz_list = []
    for t in range(trial_xyz.shape[-1]):
        xyz_list.append(xyz_print(sc_xyz, sc_lab, trial_xyz[:,:,t], trial_lab))

    xyz_final = ''.join(xyz_list)
    with open('../tests/5-simple_insertion/inserts.xyz', 'w') as f:
        f.write(xyz_final)

