import pandas as pd
from keras.utils import to_categorical
from sklearn.utils import shuffle

class DataFrame(object):
    def __init__(self, path_to_input_files,save_path,
                classes,node_classes,systematics,event_category,
                train_variables,
                test_percentage,
                norm_variables = False,
                additional_cut = None,
                lumi = 41.5):

        ''' takes a path to a folder where one h5 per class is located
            the events are cut according to the event_category
            variables in train_variables are used as input variables
            the dataset is shuffled and split into a test and train sample
                according to test_percentage
            for better training, the variables can be normed to std(1) and mu(0) '''

        # loop over all classes and extract data as well as event weights
        class_dataframes = list()
        for cls in classes:
            class_file = path_to_input_files + "/" + cls + "_dnn.h5"
            print("-"*50)
            print("loading class file "+str(class_file))
            with pd.HDFStore( class_file, mode = "r" ) as store:
                cls_df = store.select("data")
                print("number of events before selections: "+str(cls_df.shape[0]))

            # apply event category cut
            cls_df.query(event_category, inplace = True)
            self.event_category = event_category
            print("number of events after selections:  "+str(cls_df.shape[0]))

            # add event weight
            if "data" in cls:
              cls_df = cls_df.assign(total_weight = lambda x: x.Weight_XS * x.Weight_CSV)
            else:
              cls_df = cls_df.assign(total_weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom)

            weight_sum = sum(cls_df["total_weight"].values)
            class_weight_scale = 1.
            if "ttH" in cls: class_weight_scale *= 1.0
            cls_df = cls_df.assign(train_weight = lambda x: class_weight_scale*x.total_weight/weight_sum)
            print("weight sum of train_weight: "+str( sum(cls_df["train_weight"].values) ))

            # add lumi weight
            # if the systematics are btag related, just add the syst.
            # if it is coming from an ntuple, just add it (multiplying by 1)
		#=> in this case, lumi_weight should be equal lumi_weight_syst.
                #=> if it is nominal, this will be the case.
            # if it is not btag related, remove the nominal and add the syst.
            onlyttbarlist=("GenWeight_8","GenWeight_6","GenWeight_9","GenWeight_7"\
                          ,"Weight_LHA_306000_up","Weight_LHA_306000_down","Weight_scale_variation_muR_2p0_muF_1p0","Weight_scale_variation_muR_0p5_muF_1p0","Weight_scale_variation_muR_1p0_muF_2p0","Weight_scale_variation_muR_1p0_muF_0p5"\
                          )
            if "data" in cls:
              cls_df = cls_df.assign(lumi_weight = lambda x: x.Weight_XS * x.Weight_CSV)
            elif ("ttH" in cls or "SingleTop" in cls) and systematics not in onlyttbarlist:
              cls_df = cls_df.assign(lumi_weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi)
              if "Weight_pu69p2" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi)
              elif "Weight_ElectronSFGFS" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi)
              elif "Weight_ElectronSFID" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi)
              elif "Weight_ElectronSFTrigger" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi)
              elif "Weight_MuonSFID" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi)
              elif "Weight_MuonSFIso" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFTrigger * lumi)
              elif "Weight_MuonSFTrigger" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * lumi)
              else:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi)
#              print("old lumi: ", cls_df["lumi_weight"])
#              print("new lumi", cls_df["lumi_weight_syst"])
            elif "ttH" not in cls and "SingleTop" not in cls:
              cls_df = cls_df.assign(lumi_weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal * lumi)
              if "Weight_pu69p2" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal * lumi)
              elif "Weight_ElectronSFGFS" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal *  lumi)
              elif "Weight_ElectronSFID" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal * lumi)
              elif "Weight_ElectronSFTrigger" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal * lumi)
              elif "Weight_MuonSFID" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal * lumi)
              elif "Weight_MuonSFIso" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal * lumi)
              elif "Weight_MuonSFTrigger" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_LHA_306000_nominal * lumi)
              elif "Weight_LHA_306000" in systematics:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * lumi)
              else:
                cls_df = cls_df.assign(lumi_weight_syst = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.eval(systematics) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal * lumi)
#              print("old lumi: ", cls_df["lumi_weight"])
#              print("new lumi", cls_df["lumi_weight_syst"])

            # add data to list of dataframes
            class_dataframes.append( cls_df )
            print("-"*50)

        # concatenating all dataframes
        df = pd.concat( class_dataframes )
        del class_dataframes

        # add class_label translation
        dict_classes = node_classes
        for c in classes:
          if c not in node_classes:
            dict_classes=dict_classes+[c]

        print("dict_classes is: ", dict_classes)
        index = 0
        self.class_translation = {}
        for cls in dict_classes:
            self.class_translation[cls] = index
            index += 1
        self.classes = classes
        self.index_classes = [self.class_translation[c] for c in classes]
        print("the indexes are: ", self.index_classes)

        # add flag for ttH to dataframe
        df["is_ttH"] = pd.Series( [1 if c=="ttHbb" else 0 for c in df["class_label"].values], index = df.index )
        # add index labelling to dataframe
        print('df["class_label"].values is :  ',df["class_label"].values)
        df["index_label"] = pd.Series( [self.class_translation[c] for c in df["class_label"].values], index = df.index )

        # norm weights to mean(1)
        #df["train_weight"] = df["train_weight"]*df.shape[0]/len(classes)

        # save some meta data about network
        self.n_input_neurons = len(train_variables)
        self.n_output_neurons = len(node_classes)

        # shuffle dataframe
        #df = shuffle(df, random_state = 333)

        # norm variables if wanted
        unnormed_df = df.copy()
        normcsv=pd.read_csv(str(save_path)+"/checkpoints/variable_norm.csv", index_col=0)
        if norm_variables:
            norm_csv = pd.DataFrame(index=train_variables, columns=["mu", "std"])
            for v in train_variables:
                norm_csv["mu"][v] = normcsv.loc[v,"mu"]
                norm_csv["std"][v] = normcsv.loc[v,"std"]
            df[train_variables] = (df[train_variables] - norm_csv["mu"])/norm_csv["std"]
            #df[train_variables] = (df[train_variables] - df[train_variables].mean())/df[train_variables].std()
            self.norm_csv = norm_csv

        if additional_cut:
            print("events in dataframe before cut "+str(df.shape[0]))
            df.query( additional_cut, inplace = True )
            print("events in dataframe after cut "+str(df.shape[0]))

        self.unsplit_df = df.copy()
        # split test sample
        n_test_samples = int( df.shape[0]*test_percentage )
        self.df_test = df.head(n_test_samples)
        self.df_train = df.tail(df.shape[0] - n_test_samples )
        self.df_test_unnormed = unnormed_df.head(n_test_samples)

        # print some counts
        print("total events after cuts:  "+str(df.shape[0]))
        print("events used for training: "+str(self.df_train.shape[0]))
        print("events used for testing:  "+str(self.df_test.shape[0]))
        del df

        # save variable lists
        self.train_variables = train_variables
        self.output_classes = node_classes


    # train data -----------------------------------
    def get_train_data(self, as_matrix = True):
        if as_matrix: return self.df_train[ self.train_variables ].values
        else:         return self.df_train[ self.train_variables ]

    def get_train_weights(self):
        return self.df_train["train_weight"].values

    def get_train_labels(self, as_categorical = True):
        if as_categorical: return to_categorical( self.df_train["index_label"].values )
        else:              return self.df_train["index_label"].values


    # test data ------------------------------------
    def get_test_data(self, as_matrix = True, normed = True):
        if not normed: return self.df_test_unnormed[ self.train_variables ]
        if as_matrix:  return self.df_test[ self.train_variables ].values
        else:          return self.df_test[ self.train_variables ]

    def get_test_weights(self):
        return self.df_test["total_weight"].values
    def get_lumi_weights(self):
        return self.df_test["lumi_weight"].values
    def get_lumi_weights_syst(self):
        return self.df_test["lumi_weight_syst"].values

    def get_test_labels(self, as_categorical = True):
        if as_categorical: return to_categorical( self.df_test["index_label"].values )
        else:              return self.df_test["index_label"].values

    def get_class_flag(self, class_label):
        return pd.Series( [1 if c==class_label else 0 for c in self.df_test["class_label"].values], index = self.df_test.index ).values

    def get_ttH_flag(self):
        return self.df_test["is_ttH"].values

    # full sample ----------------------------------
    def get_full_df(self):
        return self.unsplit_df[self.train_variables]
