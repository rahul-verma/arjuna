
def init_session(my):
    my.evars['is_evar'] = 11

def end_session(my):
    my.evars['es_evar'] = 12

def init_each_stage(my):
    my.evars['ist_evar'] = 13

def end_each_stage(my):
    my.evars['est_evar'] = 14

def init_stage_1(my):
    my.evars['is1_evar'] = 15

def end_stage_1(my):
    my.evars['is1_evar'] = 16

def init_each_group(my):
    my.evars['ieg_evar'] = 17

def end_each_group(my):
    my.evars['eeg_evar'] = 18

def init_gp1(my):
    my.evars['igp1_evar'] = 19

def end_gp1(my):
    my.evars['egp1_evar'] = 20

def init_each_module(my):
    my.evars['iem_evar'] = 21

def end_each_module(my):
    my.evars['eem_evar'] = 22