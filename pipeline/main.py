#!/user/bin/python

from metaruns_class import *

if __name__ == "__main__":
    ###
    SCRIPTS_DIR = "scripts/"
    #fofn = "/home/artic/Desktop/mngs_deployment/rlists/PED-ENNGS_103045-001-068.fofn"
    fofn= "/home/artic/Desktop/mngs_deployment/rlists/Viral_encephalitis-GOSHmeta1.fofn"
    #fofn= "/home/artic/Desktop/mngs_deployment/rlists/TEST_DATASETS_DT04_S1.fofn"
    #fofn= "/home/artic/Desktop/mngs_deployment/rlists/TEST_DATASETS-DATASET01.fofn"
    ###
    event= meta_orchestra(sup= 1, down=1, odir= "RUNS_debug/")
    event.sup_deploy(fofn)
    event.low_deploy()
    event.record_runs()
    #event.clean(delete= False)

    ###
    #event= metaclass_run(rdir= "RUNS_debug/TEST_DATASETS-DATASET01.fofn/run_0-1/",
    #                     child= "child_1-0")
    #event.run_main()
    #print(event.id)
