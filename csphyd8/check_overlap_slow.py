import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

def check_overlap( host_xyz, host_rad, guest_xyz, scale):

    hits = []

    ndim, nat, ntrial = guest_xyz.shape

    nh = 0

    for trial in range(ntrial):
        overlap = 0
        for at in range(nat):
            dist_vecs = np.subtract(host_xyz, guest_xyz[:,at,trial][:,None])
            threshold = host_rad[:,at] * scale
            distances = np.subtract(np.linalg.norm(dist_vecs, axis=0),\
                                        threshold)
            fails = np.where(distances < 0.0)
            min_dist  = np.min(distances)
            if min_dist < 0.0:
                overlap = 1
                break
        if overlap == 0:
            hits.append(trial)
            nh += 1

    print('Number of hits identified: {}'.format(nh))

    return hits

def check_overlap2(host_xyz, host_rad, guest_xyz, scale):

    hits = []

    ndim, nat, ntrial = guest_xyz.shape

    nh = 0

    thresh_rad = host_rad * scale

    for trial in range(ntrial):
        overlap = 0
        for at in range(nat):
            dist_vecs = np.subtract(host_xyz[:,:,trial], guest_xyz[:,at,trial][:,None])
            threshold = thresh_rad[:,at]
            distances = np.subtract(np.linalg.norm(dist_vecs, axis=0),\
                                        threshold)
            #distances = np.subtract(np.linalg.norm(dist_vecs, axis=0).reshape((3,-1)),\
            #        threshold[:,None]).reshape(-1)
            min_dist  = np.min(distances)
            if min_dist < 0.0:
                overlap = 1
                break

        if overlap == 0:
            hits.append(trial)
            nh += 1

    print('Number of hits identified: {}'.format(nh))

    return hits

