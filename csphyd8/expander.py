from cspy.alpha.voids import Voids
import numpy as np

def expand_cryst(cryst, vec=None):

    def expand_lattice(cryst, factor=(1.1, 1.1, 1.1)):
        cryst.aniso_inflate_cell(factor)

    target_void_vol   = 18 # Hard-sphere volume of water molecule.
    exp_lv = 1.0
    exp_max = 1.5
    step = 0.01
    probe_r = 1.0
    grid_s  = 0.3

    unit = np.array([1., 1., 1.])

    v = Voids()
    v.calc_void(cryst, probesize=probe_r, gridsize=grid_s)

    vec = unit

    for i in range(50):

        v_old = vec
        expansion = i*step
        vec = (unit + expansion)/v_old

        expand_lattice(cryst, factor=vec)
        print(f"iter {i}, current expansion level = {unit + i*step}")
        v.calc_void(cryst, probesize=probe_r, gridsize=grid_s)
        if v.voids and (max(v.voids) > target_void_vol):
            break

    if v.voids != []:
        centroids = np.array(v.centroids)
        centroids += (centroids < 0)*1
        print("CENTROIDS TEXT: {}", centroids)
        frac, whole = np.modf(centroids)
        print("CENTROIDS NUMPY: {}", frac)
        centroids = cryst.lattice.to_cartesian(frac)
        #centroids = cryst.lattice.to_cartesian(centroids)
        return(centroids, v, expansion)
    else:
        return 0

if __name__ == '__main__':
    from cspy.alpha.hydCrystal import HydCrystalStructure

    a = HydCrystalStructure()
    a.init_from_res_file('../tests/1-loaders/dipica_min.res')
    c, voids = expand_cryst(a)
    #a.voids.calc_void(probesize=1.0, gridsize=0.3)
    #void_mols = a.voids.as_molecule()
    #a.unique_molecule_list.append(void_mols)
    #a.update_sfac()
    #a.write_res_to_file('void_centroids.res')
