import numpy as np
import pandas as pd
import uproot as root
import re
import glob
import os
import shutil 
import matplotlib.pyplot as plt

import variable_info

class Sample:
    def __init__(self, sampleName, ntuples, selections = None, MEMs = None, CNNmaps = None):
        self.sampleName = sampleName
        self.ntuples    = ntuples
        self.selections = selections
        self.MEMs       = MEMs
        self.CNNmaps    = CNNmaps


class Dataset:
    def __init__(self, outputdir, naming = "", addCNNmap = False, addMEM = False):
        # settings for paths
        self.outputdir  = outputdir
        self.naming     = naming
        
        # settings for dataset
        self.addCNNmap  = addCNNmap
        self.addMEM     = addMEM

        # default values for some configs
        self.baseSelection  = None
        self.samples        = {}
    
    def addBaseSelection(self, selection):
        self.baseSelection = selection

    def addSample(self, **kwargs):
        print("adding sample: "+str(kwargs["sampleName"]))
        self.samples[kwargs["sampleName"]] = Sample(**kwargs)


    




def ask_yes_no(question):
    yes = ['yes','y', 'ye', '']
    no = ['no','n']

    print(question)
    choice = raw_input().lower()
    if choice in yes:  return True
    elif choice in no: return False
    else: 
        print("please respond with 'yes' or 'no'")
        return ask_yes_no(question)






def create_datasets(df, class_label, out_path):
    ''' write dataset with events of given classlabel to workdir '''
    cut_df = df.query("(class_label == '"+str(class_label)+"')")
    print("creating dataset for class label {} with {} entries".format(class_label, cut_df.shape[0]))

    with pd.HDFStore(out_path, "a") as store:
        store.append("data", cut_df, index = False)

def create_mem_dataset(df, out_path):
    ''' write mem variables to workdir '''
    # reset index of dataframe
    df.set_index(["run", "lumi", "event"], inplace = True, drop = True)

    # append data to file
    with pd.HDFStore(out_path, "a") as store:
        store.append("MEM_data", df, index = False)

def apply_cut(df, condition, additional_condition, drop_variables = None):
    ''' apply cut to data
        optionally drop variables from dataframe if it is not needed anymore '''
    
    # cut by given condition
    cut_df = df.query(condition)
    # apply additional condition if neccesary
    if additional_condition:
        cut_df = cut_df.query(additional_condition)

    # drop cut variables if not further specified
    if drop_variables:
        cut_df.drop(drop_variables, axis = 1, inplace = True)
    return cut_df

def add_class_labels(df, is_ttH = False):
    ''' add column of class labels for higgs and ttbar events '''
    print("adding class labels to df...")

    if is_ttH:
        df["class_label"] = pd.Series( ["ttHbb"]*df.shape[0], index = df.index )
    else:
        # split ttbar processes
        ttbb_df = df.query("(GenEvt_I_TTPlusBB == 3 and GenEvt_I_TTPlusCC == 0)")
        ttbb_df["class_label"] = pd.Series( ["ttbb"]*ttbb_df.shape[0], index = ttbb_df.index )

        tt2b_df = df.query("(GenEvt_I_TTPlusBB == 2 and GenEvt_I_TTPlusCC == 0)")
        tt2b_df["class_label"] = pd.Series( ["tt2b"]*tt2b_df.shape[0], index = tt2b_df.index )

        ttb_df = df.query("(GenEvt_I_TTPlusBB == 1 and GenEvt_I_TTPlusCC == 0)")
        ttb_df["class_label"] = pd.Series( ["ttb"]*ttb_df.shape[0], index = ttb_df.index )

        ttcc_df = df.query("(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 1)")
        ttcc_df["class_label"] = pd.Series( ["ttcc"]*ttcc_df.shape[0], index = ttcc_df.index )

        ttlf_df = df.query("(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 0)")
        ttlf_df["class_label"] = pd.Series( ["ttlf"]*ttlf_df.shape[0], index = ttlf_df.index )

        # concatenate them
        df = pd.concat( [ttbb_df, tt2b_df, ttb_df, ttcc_df, ttlf_df] )
    
    df.drop(["GenEvt_I_TTPlusBB", "GenEvt_I_TTPlusCC"], axis = 1, inplace = True)
    return df

def add_cnn_variables(df, cnn_df):
    ''' search cnn file for events in df and add cnn maps to variables '''
    print("adding CNN maps to dataframe ...")
    # add entry to dataframe to indicate whether a cnn map is found
    cnn_df["has_cnn"]   = pd.Series([True]*cnn_df.shape[0], index = cnn_df.index)

    # get dictionary of column datatypes to recast them later
    cnn_columns = cnn_df.columns.values
    dtype_dict = {v: cnn_df[v].dtype for v in cnn_columns if not v == "has_cnn"}

    # reset index of dataframe
    #df.set_index(["Evt_Run", "Evt_Lumi", "Evt_ID"], inplace = True, drop = True)

    # add cnn variables
    df = df.join(cnn_df, how = "left")

    # only return events where a CNN map has been found
    new_df = df.query("has_cnn == True")
    n_evts = new_df.shape[0]
    n_evts_before = df.shape[0]
    print("matched {} events with CNN maps".format(n_evts))
    print("{} events were not matched".format(n_evts_before - n_evts))
    new_df.drop("has_cnn", axis = 1, inplace = True)

    # recast datatypes to save disk
    new_df = new_df.astype(dtype = dtype_dict)
    
    return new_df


def add_mem_variables(df, mem_df, mem_var = "mem_p"):
    ''' search mem file for events in df and add mem values to variables '''
    print("adding MEM to dataframe ...")
    # creating variable with default value
    df["memDBp"] = pd.Series([-1]*df.shape[0], index = df.index)

    # reset index of dataframe
    #df.set_index(["Evt_Run", "Evt_Lumi", "Evt_ID"], inplace = True, drop = True)

    # add mem_var from mem_df
    df.update( mem_df[mem_var].rename("memDBp") )

    # check if some mems could not be set
    if not df.query("memDBp == -1").empty:
        print("ATTENTION: SOME ENTRIES COULD NOT FIND A MATCHING MEM - SET TO -1")
        n_entries_before = df.shape[0]
        df = df.query("memDBp != -1")
        print("{} events found without mem".format(n_entries_before - df.shape[0]))
    return df

def generate_mem_h5(mem_files, output_mem_h5_file):
    ''' generate and load mem lookup table '''
    mem_vars = ["event", "lumi", "run", "mem_p"]

    print("-"*50)
    if isinstance(mem_files, basestring):
        print("using old mem file")
        mem_h5_file = mem_files    
    else:
        for mf in mem_files:
            print("loading mem file "+str(mf))
            # open root file
            with root.open(mf) as rf:
                # get tree
                tree = rf["tree"]

                # convert tree to dataframe but only extract the variables needed
                df = tree.pandas.df(mem_vars)

                # save data
                create_mem_dataset(df, output_mem_h5_file)
                mem_h5_file = output_mem_h5_file
    
    print("saved all mem variables for chosen process")
    print("reopening concatenated dataframe")
    with pd.HDFStore(mem_h5_file, "r") as store:
        mem_df = store.select("MEM_data")
    print("-"*50)
    
    return mem_df


# =================================================================================================
def process_files(files, mem_files, mem_name, vars, vecvars, sel, workdir, additional_selection = None, sel_vars = None, is_ttH = False, cnn_map = False):
    ''' create dataframes from files
        - loop over globbed input files
            - load tree
            - create dataframe
            - manage vector variables 
            - apply trigger and eventselection cuts 
            - write data to output directory '''

    # determine mem file location
    mem_path = workdir + "/MEM/"
    if not os.path.exists(mem_path):
        os.makedirs(mem_path)
    h5_mem_file = mem_path + "/" + str(mem_name) +".h5"

    # get mem dataframe
    mem_df = generate_mem_h5(mem_files, h5_mem_file)

    # load cnn data if needed and determine output path
    if cnn_map:
        print("loading cnn dataframe")
        cnn_df = pd.read_hdf(cnn_map, "data")
        print("cnn dataframe has {} entries".format(cnn_df.shape[0]))
        naming = "_cnn.h5"
    else:
        naming = "_dnn.h5"

    # initializing loop over ntuple files
    n_entries = 0
    max_entries = 50000
    concat_df = pd.DataFrame()
    n_files = len(files)

    # loop over files
    for i_file, f in enumerate(files):
        print("({}/{}) loading file {}".format(i_file+1,n_files,f))
        # open root file
        with root.open(f) as rf:
            # get MVATree
            tree = rf["MVATree"]
    
            # convert tree to dataframe but only extract the variables needed
            df = tree.pandas.df(vars)

            # handle vector variables, loop over them
            for vecvar in vecvars:
                # load dataframe with vector variable
                vec_df = tree.pandas.df(vecvar)

                # loop over indices in vecvar list
                for idx in vecvars[vecvar]:
                    # slice the index
                    idx_df = vec_df.loc[ (slice(None), slice(idx,idx)), :]
                    # define name for column in df
                    col_name = str(vecvar)+"["+str(idx)+"]"
                    # append column to original dataframe
                    df[col_name] = pd.Series( idx_df[vecvar].values, index = df.index )

        # apply event selection
        df = apply_cut(df, sel, additional_selection, drop_variables = sel_vars + ["Evt_Odd"])

        # concat dfs
        if concat_df.empty: concat_df = df
        else:               concat_df = concat_df.append(df)
        
        # add entries to counter
        n_entries += df.shape[0]

        # if number of entries exceeds max threshold, add labels and mem and save dataframe
        if (n_entries > max_entries or f == files[-1]):
            print("*"*50)
            print("max_entrires reached ...")
            # add class labels
            concat_df = add_class_labels(concat_df, is_ttH = is_ttH)
            # add indexing
            concat_df.set_index(["Evt_Run", "Evt_Lumi", "Evt_ID"], inplace = True, drop = True)
            # add mem variables
            concat_df = add_mem_variables(concat_df, mem_df)
            # add cnn variables
            if cnn_map:
                concat_df = add_cnn_variables(concat_df, cnn_df)

            # write data to file
            if is_ttH:
                out_path = workdir + "/ttHbb"+naming
                create_datasets(concat_df, class_label = "ttHbb", out_path = out_path)
            else:
                out_path = workdir + "/ttbb"+naming
                create_datasets(concat_df, class_label = "ttbb", out_path = out_path)
                out_path = workdir + "/tt2b"+naming
                create_datasets(concat_df, class_label = "tt2b", out_path = out_path)
                out_path = workdir + "/ttb"+naming
                create_datasets(concat_df, class_label = "ttb",  out_path = out_path)
                out_path = workdir + "/ttcc"+naming
                create_datasets(concat_df, class_label = "ttcc", out_path = out_path)
                out_path = workdir + "/ttlf"+naming
                create_datasets(concat_df, class_label = "ttlf", out_path = out_path)

            print("*"*50)
            # reset counters
            n_entries = 0
            concat_df = pd.DataFrame()

    print("done.")




def preprocess_single_sample(sample, old_mem_files, variables, vecvars, base_selection, workdir, additional_selection, trigger_variables, is_ttH, add_cnn):
    ''' handle preprocessing of a single file
        - glob files
        - create MEM df or use old MEM df
        - call function to create df for that file '''

    ntuple_files = glob.glob(sample["ntuples"])
    mem_files    = glob.glob(sample["MEM"])
    sample_name  = sample["name"]
    mem_name     = sample_name+"_MEM"

    print("="*100)
    print("now handling ntuples from "+str(sample_name))
    print("location: "+str(ntuple_files))
    print("mems:     "+str(mem_files))
    if add_cnn: 
        add_cnn = sample["CNN"]
        print("CNN maps: "+str(add_cnn))
    print("="*100)

    # check if mem file exists and remove if wanted
    for f in old_mem_files:
        if mem_name in f:
            print("found old MEM file in directory: "+str(f))
            if ask_yes_no("should the old MEM file be used?"):
                mem_files = f
            else: os.remove(f)

    # process those files
    process_files(
        ntuple_files,
        mem_files,
        mem_name,
        variables,
        vecvars,
        base_selection,
        workdir,
        additional_selection,
        trigger_variables,
        is_ttH,
        cnn_map = add_cnn)


def preprocess_data(ttH_samples, ttbar_samples, base_selection, ttbar_selection, workdir, add_cnn = False):
    ''' handle all preprocessing files
        - remove old data
        - get variables
        - loop over all ttH and ttbar samples '''

    # remove old h5 files
    if not os.path.exists(workdir):
        os.makedirs(workdir)

    if add_cnn: out_path = workdir+"/*_cnn.h5"
    else:       out_path = workdir+"/*_dnn.h5"
    old_h5_files = glob.glob(out_path)
    for f in old_h5_files: os.remove(f)

    mem_path = workdir + "/MEM/*.h5"
    old_mem_files = glob.glob(mem_path)
    
    # get variable lists
    variables, vecvars, trigger_variables = get_variable_lists()

    # loop over ttH files:
    for sample in ttH_samples:
        preprocess_single_sample(
            sample, 
            old_mem_files, 
            variables, 
            vecvars, 
            base_selection, 
            workdir, 
            additional_selection = "(Evt_Odd == 1)", 
            trigger_variables = trigger_variables, 
            is_ttH = True,
            add_cnn = add_cnn)

    # loop over ttbar files:
    for sample in ttbar_samples:
        preprocess_single_sample(
            sample, 
            old_mem_files, 
            variables, 
            vecvars, 
            base_selection, 
            workdir, 
            additional_selection = ttbar_selection,
            trigger_variables = trigger_variables, 
            is_ttH = False,
            add_cnn = add_cnn)


# =========================================================
# handle vector variables:
def get_vars_and_vecvars(varlist):
    # list for variables
    variables = []
    # dictionary for vector variables
    vector_variables = {}

    # loop over variables in list
    for var in varlist:

        # search for index in name (dummyvar[index])
        found_vector_variable = re.search("\[\d+?\]$", var)
        # append variable to list if not a vector variable
        if not found_vector_variable:
            variables.append(var)
        # add index information to dictionary if it is a vector variable
        else:
            index = found_vector_variable.group(0)
            var_name = var[:-len(index)]
            var_index = int(index[1:-1])
            if var_name in vector_variables:
                vector_variables[var_name].append( var_index )
            else:
                vector_variables[var_name] = [var_index]
            
    return variables, vector_variables


def get_variable_lists():
    ''' define which variables to load '''

    # import variable infos
    variable_list = variable_info.all_variables_list

    # get variables and dictionary of vector variables
    variables, vecvars = get_vars_and_vecvars(variable_list)

    # mem variable is not in ntuples so remove it from list and add it via mem dataframes
    if "MEM" in variables: variables.remove("MEM")
    # add some more variables needed
    # append variables for class labels
    variables += ['GenEvt_I_TTPlusBB', 'GenEvt_I_TTPlusCC']

    # variables for category cutting
    variables += ["N_Jets", "N_BTagsM"]

    # append variables for prenet-targets
    variables += [
        "GenAdd_BB_inacceptance_part",
        "GenAdd_B_inacceptance_part",
        "GenHiggs_BB_inacceptance_part",
        "GenHiggs_B_inacceptance_part",
        "GenTopHad_B_inacceptance_part",
        "GenTopHad_QQ_inacceptance_part",
        "GenTopHad_Q_inacceptance_part",
        "GenTopLep_B_inacceptance_part",
        "GenAdd_BB_inacceptance_jet",
        "GenAdd_B_inacceptance_jet",
        "GenHiggs_BB_inacceptance_jet",
        "GenHiggs_B_inacceptance_jet",
        "GenTopHad_B_inacceptance_jet",
        "GenTopHad_QQ_inacceptance_jet",
        "GenTopHad_Q_inacceptance_jet",
        "GenTopLep_B_inacceptance_jet",
            ]
    # append variable for train/test splitting
    variables += ["Evt_Odd"]

    # variables for weighting events
    variables += [
        "Weight_XS", 
        "Weight_CSV", 
        #"Weight_DeepCSV", # not existing
        "Weight_GEN_nom"]

    # append variables for MEM matching
    variables += ["Evt_ID", "Evt_Run", "Evt_Lumi"]

    # variables for triggering ------
    # append variables for category cutting
    # variables for mcTriggerWeights
    trigger_variables = [
        "N_LooseMuons", 
        "N_TightElectrons", 
        "N_LooseElectrons", 
        "N_TightMuons",    
        "Triggered_HLT_Ele35_WPTight_Gsf_vX", 
        "Triggered_HLT_Ele28_eta2p1_WPTight_Gsf_HT150_vX",
        "Muon_Pt",
        "Triggered_HLT_IsoMu27_vX",
        "Evt_Pt_MET",
        ]

    # additional ttbar triggers
    trigger_variables += [
        "Weight_scale_variation_muR_0p5_muF_0p5",
        "Weight_scale_variation_muR_0p5_muF_1p0",
        "Weight_scale_variation_muR_0p5_muF_2p0",
        "Weight_scale_variation_muR_1p0_muF_0p5",
        "Weight_scale_variation_muR_1p0_muF_1p0",
        "Weight_scale_variation_muR_1p0_muF_2p0",
        "Weight_scale_variation_muR_2p0_muF_0p5",
        "Weight_scale_variation_muR_2p0_muF_1p0",
        "Weight_scale_variation_muR_2p0_muF_2p0"
        ]
    variables += trigger_variables
    # --------------------------------------------------------
    return variables, vecvars, trigger_variables
# =========================================================