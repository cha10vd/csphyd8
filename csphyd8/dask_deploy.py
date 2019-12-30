from dask.distributed import Client, fire_and_forget
from dask_jobqueue import SLURMCluster
from dask import bag as db
from dask import delayed

cluster = SLURMCluster(cores=40,
                       processes=40,
                       memory='250GB',
                       queue='scavenger',
                       walltime='02:00')

cluster.start_workers(2)
client = Client(cluster)

if __name__ == '__main__':

    guest = load_molecule('aaa.res')
    trial_xyz, trial_rad = perturb_mol(guest)
    trial_xyz = delayed(trial_xyz)
    trial_rad = delayed(trial_rad)
    structures = load_crystals()

    bag = db.from_sequence([(structure, trial_xyz, trial_rad) for
                            structure in structures], partition_size=40)

    guest_hits = client.map(gen_guests, bag)

    fire_and_forget(save_expansion, guest_hits)

    inserts = client.map(insert_guests, guest_hits)

    reopts = client.map(reoptimize_inserts, inserts)
