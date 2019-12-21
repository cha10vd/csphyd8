import numpy as np
import itertools

def cartesian_symm_ops(cryst):

    to_cart  = cryst.lattice.direct_matrix()
    to_frac  = cryst.lattice.inverse_matrix()
    symm_ops = []

    for op in cryst.spacegroup.operations:
        op0 = to_frac @ op.matrix_form()[0] @ to_cart
        op1 = cryst.lattice.to_cartesian(op.matrix_form()[1])
        symm_ops.append((op0, op1))

    images = []

    translations = np.array(list(itertools.product([0,-1,1], repeat=3)))
    translations = translations @ to_cart

    expanded = []
    for op in symm_ops:
        for trans in translations:
            expanded.append((op[0], op[1] + trans))

    symm_ops = expanded

    return symm_ops

def make_images(trials, radii, symm_ops):
    images = []

    for op in symm_ops[:]:
        nat, nmol = trials.shape[1:]
        im = trials.reshape(3,nat*nmol).T
        im = np.dot(im, op[0]).T
        im += op[1][:,None]
        im = im.reshape(3,nat,nmol)
        images.append(im)

    images = np.concatenate(images[1:], axis=1) # Skip identity of 1st mol.

    #for atom in range(images[:,:,0].shape[1]):
    #    print(self.lab[atom%4], *images[:,atom,0])

    radii  = np.tile(radii, len(symm_ops)-1).reshape((-1,3))
    return images, radii

if __name__ == '__main__':
    from cspy.alpha.hydCrystal import HydCrystalStructure
    from cspy.alpha.molecule import Molecule
    from perturbator import perturb_mol

    cryst = HydCrystalStructure()
    cryst.init_from_res_file('../tests/4-symmetry/dipica_min.res')
    cryst.generate_symmetry_operation()

    mol  = Molecule()
    mol.init_from_xyz('../tests/4-symmetry/h2o.xyz')

    symm_ops = cartesian_symm_ops(cryst)
    trials, radii, labels = perturb_mol(mol, ntrials=10, labels=True)

    images, rad_i = make_images(trials, radii, symm_ops)

    with open('../tests/4-symmetry/images.xyz', 'w') as f:
        for trial in range(10):
                xyz_list = images[:,:,trial].T

                f.write(str(xyz_list.shape[0]) + '\n\n')
                for i in range(xyz_list.shape[0]):
                    TEMPLATE = '{}\t' + ' {:.4f}'*3 + '\n'
                    f.write(TEMPLATE.format(labels[i%3], *xyz_list[i,:]))
