#-*-coding:utf8-*-
import copy, os

from gen_conf_file import *
from dataset_cfg import *

def gen_match_lstm(d_mem, init, lr, dataset, l2, lstm_norm2, is_pretrain, pretrain_run_no, model_no, epoch_no):
    # print "ORC: left & right lstm share parameters"
    net = {}

    ds = DatasetCfg(dataset)
    g_filler    = gen_uniform_filter_setting(init)
    zero_filler = gen_zero_filter_setting()
    g_updater   = gen_adagrad_setting(lr = lr, l2 = l2, batch_size = ds.train_batch_size)
    zero_l2_updater   = gen_adagrad_setting(lr = lr, batch_size = ds.train_batch_size)

    g_layer_setting = {}
    g_layer_setting['no_bias'] = False
    g_layer_setting['w_filler'] = g_filler 
    g_layer_setting['u_filler'] = g_filler
    g_layer_setting['b_filler'] = zero_filler
    g_layer_setting['w_updater'] = g_updater
    g_layer_setting['u_updater'] = g_updater
    g_layer_setting['b_updater'] = g_updater
    g_layer_setting['w_g_filler'] = g_filler 
    g_layer_setting['u_g_filler'] = g_filler
    g_layer_setting['b_g_filler'] = zero_filler
    g_layer_setting['w_c_filler'] = g_filler 
    g_layer_setting['u_c_filler'] = g_filler
    g_layer_setting['b_c_filler'] = zero_filler
    g_layer_setting['w_g_updater'] = g_updater
    g_layer_setting['u_g_updater'] = g_updater
    g_layer_setting['b_g_updater'] = g_updater
    g_layer_setting['w_c_updater'] = g_updater
    g_layer_setting['u_c_updater'] = g_updater
    g_layer_setting['b_c_updater'] = g_updater


    net['net_name'] = 'match_bilstm_sim_dpool'
    net['need_reshape'] = False
    net_cfg_train, net_cfg_valid, net_cfg_test = {}, {}, {}
    net['net_config'] = [net_cfg_train, net_cfg_valid, net_cfg_test]
    net_cfg_train["tag"] = "Train"
    net_cfg_train["max_iters"] = ds.train_max_iters 
    net_cfg_train["display_interval"] = ds.train_display_interval
    net_cfg_train["out_nodes"] = ['loss', 'acc']
    net_cfg_valid["tag"] = "Valid"
    net_cfg_valid["max_iters"] = ds.valid_max_iters 
    net_cfg_valid["display_interval"] = ds.valid_display_interval 
    net_cfg_valid["out_nodes"] = ['loss','acc']
    net_cfg_test["tag"] = "Test"
    net_cfg_test["max_iters"]  = ds.test_max_iters 
    net_cfg_test["display_interval"] = ds.test_display_interval
    net_cfg_test["out_nodes"]  = ['loss','acc']
    layers = []
    net['layers'] = layers

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = []
    layer['top_nodes'] = ['x', 'y']
    layer['layer_name'] = 'train_data'
    layer['layer_type'] = 71
    layer['tag'] = ['Train']
    setting = {}
    layer['setting'] = setting
    setting['batch_size'] = ds.train_batch_size
    setting['data_file'] = ds.train_data_file
    setting['max_doc_len'] = ds.max_doc_len
    setting['min_doc_len'] = ds.min_doc_len

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = []
    layer['top_nodes'] = ['x', 'y']
    layer['layer_name'] = 'valid_data'
    layer['layer_type'] = 71
    layer['tag'] = ['Valid']
    setting = {}
    layer['setting'] = setting
    setting['batch_size'] = ds.valid_batch_size
    setting['data_file'] = ds.valid_data_file
    setting['max_doc_len'] = ds.max_doc_len
    setting['min_doc_len'] = ds.min_doc_len

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = []
    layer['top_nodes'] = ['x', 'y']
    layer['layer_name'] = 'test_data'
    layer['layer_type'] = 71
    layer['tag'] = ['Test']
    setting = {}
    layer['setting'] = setting
    setting['batch_size'] = ds.test_batch_size
    setting['data_file'] = ds.test_data_file
    setting['max_doc_len'] = ds.max_doc_len
    setting['min_doc_len'] = ds.min_doc_len

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = ['x']
    layer['top_nodes'] = ['word_rep_seq']
    layer['layer_name'] = 'embedding'
    layer['layer_type'] = 21
    setting = copy.deepcopy(g_layer_setting)
    layer['setting'] = setting
    setting['embedding_file'] = ds.embedding_file
    print "ORC: update all words"
    # setting['update_indication_file'] = ds.update_indication_file
    setting['feat_size'] = ds.d_word_rep
    setting['word_count'] = ds.vocab_size
    print "ORC: not use l2 for embedding"
    setting['w_updater'] = zero_l2_updater

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = ['word_rep_seq']
    layer['top_nodes'] = ['l_lstm_seq']
    layer['layer_name'] = 'l_lstm'
    # layer['layer_type'] = 24
    layer['layer_type'] = 1006 # gru
    setting = copy.deepcopy(g_layer_setting)
    layer['setting'] = setting
    setting['d_mem'] = d_mem
    setting['grad_norm2'] = lstm_norm2
    setting['grad_cut_off'] = 100
    setting['max_norm2'] = 100
    setting['reverse'] = False
    setting['f_gate_bias_init'] = 0.
    setting['o_gate_bias_init'] = 0.
    if is_pretrain:
        setting['param_file'] = "/home/wsx/exp/match/wiki_lm/run.{0}/model/l_lstm.params.{1}.{2}".format(str(pretrain_run_no), str(model_no), str(epoch_no))
        print setting['param_file']

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = ['word_rep_seq']
    layer['top_nodes'] = ['r_lstm_seq']
    layer['layer_name'] = 'r_lstm'
    # layer['layer_type'] = 24
    layer['layer_type'] = 1006 # gru
    setting = copy.deepcopy(g_layer_setting)
    layer['setting'] = setting
    setting['d_mem'] = d_mem
    setting['grad_norm2'] = lstm_norm2
    setting['reverse'] = True 
    setting['grad_cut_off'] = 100
    setting['max_norm2'] = 100
    setting['f_gate_bias_init'] = 0.
    setting['o_gate_bias_init'] = 0.
    if is_pretrain:
        setting['param_file'] = "/home/wsx/exp/match/wiki_lm/run.{0}/model/r_lstm.params.{1}.{2}".format(str(pretrain_run_no), str(model_no), str(epoch_no))
        print setting['param_file']
    # if is_share:
    #     print "ORC: share parameters."
    #     share_setting_w = {}
    #     share_setting_w['param_id'] = 0
    #     share_setting_w['source_layer_name'] = 'l_lstm'
    #     share_setting_w['source_param_id'] = 0
    #     share_setting_u = {}
    #     share_setting_u['param_id'] = 1
    #     share_setting_u['source_layer_name'] = 'l_lstm'
    #     share_setting_u['source_param_id'] = 1
    #     share_setting_b = {}
    #     share_setting_b['param_id'] = 2
    #     share_setting_b['source_layer_name'] = 'l_lstm'
    #     share_setting_b['source_param_id'] = 2
    #     setting['share'] = [share_setting_w, share_setting_u, share_setting_b]

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = ['l_lstm_seq', 'r_lstm_seq']
    layer['top_nodes'] = ['bi_lstm_seq']
    layer['layer_name'] = 'concat'
    layer['layer_type'] = 18
    setting = copy.deepcopy(g_layer_setting)
    layer['setting'] = setting
    setting['bottom_node_num'] = 2
    setting['concat_dim_index'] = 3

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = ['bi_lstm_seq']
    layer['top_nodes'] = ['l_sentence', 'r_sentence']
    layer['layer_name'] = 'sentence_split'
    layer['layer_type'] = 20 
    setting = {}
    layer['setting'] = setting

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = ['l_sentence', 'r_sentence']
    layer['top_nodes'] = ['dot_similarity']
    layer['layer_name'] = 'match'
    layer['layer_type'] = 23 
    print "ORC: use MUL operation for similarity"
    layer['setting'] = {'op':'mul'}

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = ['dot_similarity', 'l_sentence', 'r_sentence']
    layer['top_nodes'] = ['dpool_rep']
    layer['layer_name'] = 'dynamic_pooling'
    layer['layer_type'] = 43
    layer['setting'] = {'row':5, 'col':5}

    # layer = {}
    # layers.append(layer) 
    # layer['bottom_nodes'] = ['dpool_rep']
    # layer['top_nodes'] = ['hidden_trans']
    # layer['layer_name'] = 'mlp_hidden'
    # layer['layer_type'] = 11 
    # setting = copy.deepcopy(g_layer_setting)
    # layer['setting'] = setting
    # setting['num_hidden'] = d_mem * 4

    # layer = {}
    # layers.append(layer) 
    # layer['bottom_nodes'] = ['hidden_trans']
    # layer['top_nodes'] = ['hidden_rep']
    # layer['layer_name'] = 'hidden_nonlinear'
    # layer['layer_type'] = 1 
    # setting = {}
    # layer['setting'] = setting
    # 
    # layer = {}
    # layers.append(layer) 
    # layer['bottom_nodes'] = ['hidden_rep']
    # layer['top_nodes'] = ['hidden_drop_rep']
    # layer['layer_name'] = 'dropout'
    # layer['layer_type'] =  13
    # ds.dp_rate = 0.
    # print "ORC, dp rate:", ds.dp_rate
    # setting = {'rate':ds.dp_rate}
    # layer['setting'] = setting

    layer = {}
    layers.append(layer) 
    # layer['bottom_nodes'] = ['hidden_drop_rep']
    # layer['bottom_nodes'] = ['hidden_drop_rep']
    layer['bottom_nodes'] = ['dpool_rep']
    layer['top_nodes'] = ['softmax_prob']
    layer['layer_name'] = 'softmax_fullconnect'
    layer['layer_type'] = 11 
    setting = copy.deepcopy(g_layer_setting)
    layer['setting'] = setting
    setting['num_hidden'] = ds.num_class
    # setting['no_bias'] = False
    setting['w_filler'] = zero_filler

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = ['softmax_prob', 'y']
    layer['top_nodes'] = ['loss']
    layer['layer_name'] = 'softmax_activation'
    layer['layer_type'] = 51 
    setting = {}
    layer['setting'] = setting

    layer = {}
    layers.append(layer) 
    layer['bottom_nodes'] = ['softmax_prob', 'y']
    layer['top_nodes'] = ['acc']
    layer['layer_name'] = 'accuracy'
    layer['layer_type'] = 56 
    setting = {'topk':1}
    layer['setting'] = setting
    return net

run = 4
l2 = 0.
# for dataset in ['paper']:
for dataset in ['qa_balance']:
    for d_mem in [80]:
        idx = 0
        # for model_no in [0,1,2,3,4,5,6,7,8]:
        #     for epoch_no in [20000, 40000, 80000]:
        for model_no in [2]:
            #  for epoch_no in [0, 10000, 25000]:
            for epoch_no in [0]:
                # for init in [0.5, 0.3, 0.1]:
                for init in [0.1, 0.03, 0.01]:
                    for lr in [0.3, 0.1, 0.03]:
                        # for l2 in [0.00001, 0.0001]:
                        for l2 in [0]:
                            pretrain_run_no = 18
                            lstm_norm2 = 10000 
                            net = gen_match_lstm(d_mem=d_mem,init=init,lr=lr,dataset=dataset,l2=l2,lstm_norm2=lstm_norm2,  \
                                                 is_pretrain=False,pretrain_run_no=pretrain_run_no,model_no=model_no,epoch_no=epoch_no)
                            net['log'] = 'log.match.bilstm_sim_dpool.{0}.d{1}.run{2}.{3}'.format\
                                         (dataset, str(d_mem), str(run), str(idx))
                            gen_conf_file(net, '/home/wsx/exp/match/{0}/bilstm_sim_dpool/run.{1}/'.format(dataset,str(run)) + \
                                               'model.match.bilstm_sim_dpool.{0}.d{1}.run{2}.{3}'.format\
                                               (dataset, str(d_mem), str(run), str(idx)))
                            idx += 1
