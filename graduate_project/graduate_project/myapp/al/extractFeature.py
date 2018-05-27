import math
from ..logconfig import logger
import networkx as nx
import random


class SimplifiedFeature(object):
    def __init__(self, socialnetwork):
        self.four_G = socialnetwork.four_G   # 有向图
        self.tw_G = socialnetwork.tw_G       # 有向图
        self.socialnetwork = socialnetwork
        self.y = []
        self.x = []    # 正负比例是1：100
        self.yt = []
        self.xt = []
        self.name = []
        self.set_feature()

    def del_dur(self, location):
        s = location.split(',')[0:-1]
        l = list(set(s))
        if 'None' in l:
            l.remove('None')
        return l

    def location_partition(self, f_location, t_location):
        s = set(f_location).intersection(t_location)
        return len(s)

    def get_social_feature(self, four_G, item, tw_G, f_anchor_known_list, t_anchor_known_list, item1):
        f_real_nei = list(four_G.neighbors(item))
        f_nei = []
        com_nei = []
        for i in f_real_nei:
            if i in f_anchor_known_list:  # foursquare中哪些是已知的
                f_nei.append(four_G.node[i]["twitterID"])
                com_nei.append(i)
        t_nei = []
        t_real_nei = list(tw_G.neighbors(item1))
        for i in t_real_nei:
            if i in t_anchor_known_list:  # foursquare中哪些是已知的
                t_nei.append(i)
        result = [v for v in t_nei if v in f_nei]  # 共同的twitter已知的neighbor的多少
        length = len(com_nei)
        res_four = []
        for i in range(0, length):
            if f_nei[i] in result:
                res_four.append(com_nei[i])
        CN = len(result)
        if (len(f_real_nei) + len(t_nei) - CN) > 0:
            JC = CN / (len(f_real_nei) + len(t_nei) - CN)
        else:
            JC = 0
        AA = 0
        for i in res_four:
            jh = len(list(four_G.neighbors(i))) + len(list(tw_G.neighbors(four_G.node[i]["twitterID"])))
            if jh != 2 and jh != 0:
                AA = AA + 1 / math.log(jh / 2)
        social_feature = (CN + JC + AA) / 3
        return social_feature

    def set_feature(self):
        logger.debug("set_feature of node pairs")
        page_rank_tw = nx.pagerank(self.tw_G)
        page_rank_four = nx.pagerank(self.four_G)
        l_no = 0
        for item in self.four_G.nodes(data=True):
            for item1 in self.tw_G.nodes(data=True):
                f_location = self.del_dur(dict(item[1])["location"])
                t_location = self.del_dur(dict(item1[1])["location"])
                l = self.location_partition(f_location, t_location)
                if l == 0:
                    l_no = l_no + 1
                if l > 0 or len(f_location) == 0 or len(t_location) == 0:
                    social_Di_feature = self.get_social_feature(self.four_G, item[0], self.tw_G, self.socialnetwork.f_anchor_known_list, self.socialnetwork.t_anchor_known_list,
                                                        item1[0])
                    social_feature = self.get_social_feature(self.four_G.to_undirected(), item[0], self.tw_G.to_undirected(), self.socialnetwork.f_anchor_known_list, self.socialnetwork.t_anchor_known_list, item1[0])
                    t = (page_rank_tw[item1[0]] - page_rank_four[item[0]]) ** 2
                    label = 0
                    if item1[0] == item[1]["twitterID"]:
                        label = 1
                    if label == 1:
                        if item[0] in self.socialnetwork.f_anchor_known_list:
                            self.y.append(1)
                            self.x.append([social_feature, social_Di_feature, t, l])
                        else:
                            self.xt.append([social_feature, social_Di_feature, t, l])
                            self.name.append(item[0] + ';' + item1[0])
                    else:
                        if item[0] in self.socialnetwork.f_anchor_known_list or item1[0] in self.socialnetwork.t_anchor_known_list:
                            self.y.append(0)
                            self.x.append([social_feature, social_Di_feature, t, l])
                        else:
                            self.xt.append([social_feature, social_Di_feature, t, l])
                            self.name.append(item[0] + ';' + item1[0])

        k = len([j for j in self.y if j == 1])
        select_num = random.sample(range(0, len(self.x) - k), k * 100)  # 1:100的比列
        num = 0
        select_i = list()
        for i in range(0, len(self.x)):
            if self.y[i] == 0:
                if num in select_num:
                    select_i.append(i)
                num = num + 1
            else:
                select_i.append(i)
        x1 = [self.x[l] for l in range(0, len(self.x)) if self.y[l] == 1 or l in select_i]
        y1 = [self.y[l] for l in range(0, len(self.y)) if self.y[l] == 1 or l in select_i]
        self.x = x1
        self.y = y1
