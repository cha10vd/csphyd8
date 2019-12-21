import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

def check_overlap( host_xyz, host_rad, guest_xyz, guest_rad, scale):

    hits = []

    ndim, nat, ntrial = guest_xyz.shape
    print(host_rad.shape)
    print(guest_rad.shape)

    nh = 0

    for trial in range(ntrial):
        overlap = 0
        for at in range(nat):
            dist_vecs = np.subtract(host_xyz, guest_xyz[:,at,trial][:,None])
            #threshold = np.add(host_rad, guest_rad[at]) * scale
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

def check_overlap2(host_xyz, host_rad, guest_xyz, guest_rad, scale):

    hits = []

    print(host_rad.shape)
    print(guest_rad.shape)

    for trial in range(guest_xyz.shape[2]):
        nh = 0
        overlap = 0
        for at in range(guest_xyz.shape[1]):
            dist_vecs = np.subtract(host_xyz[:,:,trial], guest_xyz[:,at,trial][:,None])
            threshold = host_rad[:,at] * scale
            distances = np.subtract(np.linalg.norm(dist_vecs, axis=0),\
                                        threshold)
            min_dist  = np.min(distances)
            if min_dist < 0.0:
                overlap = 1
                break

        if overlap == 0:
            hits.append(trial)
            nh += 1

    return hits

