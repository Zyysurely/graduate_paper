from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import networkx as nx
import random
from .logconfig import logger
from django.views.decorators.http import require_http_methods
from django.core import serializers
import os
import threading
import time
from .models import message, task, dataset
from .al import classifier, extractFeature, strictMatching
import datetime
import os
from .config import DATAPATH, DATASETPATH



class SocialNetwork(object):
    def __init__(self, tw_G, four_G):
        self.four_G = four_G       # Foursquare有向图
        self.tw_G = tw_G         # Twitter有向图
        self.f_anchor_known_list = []  # 设定的事先知道的anchor link foursquare
        self.t_anchor_known_list = []  # 设定的事先知道的anchor link twitter
        self.f_all_anchor_list = []
        self.t_all_anchor_list = []
        self.random_num = 0   # 控制已知数量
        self.random_list = []  # 随机生成提前知道的anchor user数
        # self.set_file_network(four_G, tw_G, four_nodes_num, tw_nodes_num, random_num)  # 根据nodes的数量生成网络

    def set_random_network(self, random_num, degree):
        self.random_num = random_num  # 控制已知数量

        # # 删除边缘节点
        out_dict = self.four_G.out_degree()
        in_dict = self.four_G.in_degree()
        r_node = [v for v in self.four_G if (out_dict[v] + in_dict[v]) <degree]
        for v in r_node:
            if v in self.f_all_anchor_list:
                self.f_all_anchor_list.remove(v)
                self.t_all_anchor_list.remove(self.four_G.node[v]['twitterID'])
        self.four_G.remove_nodes_from(r_node)

        out_dict = self.tw_G.out_degree()
        in_dict = self.tw_G.in_degree()
        r_node = [v for v in self.tw_G if (out_dict[v] + in_dict[v]) <degree]
        for v in r_node:
            if v in self.t_all_anchor_list:
                self.t_all_anchor_list.remove(v)
                self.f_all_anchor_list.remove(self.tw_G.node[v]['fourID'])
        self.tw_G.remove_nodes_from(r_node)

        # # 根据规定数量随机生成网络
        # # l = 0
        # # if nodes1 > nodes2:
        # r_node = random.sample(list(self.four_G.nodes), len(self.four_G.nodes) - nodes1)
        # for v in r_node:
        #     if v in self.f_all_anchor_list:
        #         self.f_all_anchor_list.remove(v)
        #         self.t_all_anchor_list.remove(self.four_G.node[v]['twitterID'].lower())
        # self.four_G.remove_nodes_from(r_node)
        # r_node = random.sample(list(self.tw_G.nodes), len(self.tw_G.nodes) - nodes2)
        # for v in r_node:
        #     if v in self.t_all_anchor_list:
        #         self.t_all_anchor_list.remove(v)
        #         self.f_all_anchor_list.remove(self.tw_G.node[v]['fourID'])
        # self.tw_G.remove_nodes_from(r_node)

        # # 生成事先知道的锚用户
        self.random_list = random.sample(range(0, len(self.f_all_anchor_list)), random_num)  # 随机生成提前知道的anchor user数
        for i in self.random_list:
            self.f_anchor_known_list.append(self.f_all_anchor_list[i])
            self.four_G.node[self.f_all_anchor_list[i]]["in_test"] = 1
            self.t_anchor_known_list.append(self.t_all_anchor_list[i])

    def save_file_network(self, f_type, t_type, task_id):
        nx.write_gpickle(self.four_G, "%s/%s_%s.gpickle" % (DATAPATH, task_id, f_type))
        nx.write_gpickle(self.tw_G, "%s/%s_%s.gpickle" % (DATAPATH, task_id, t_type))
        message = {"f_anchor_known_list": self.f_all_anchor_list, "t_anchor_known_list": self.t_anchor_known_list,
                   "f_all_anchor_list": self.f_all_anchor_list}
        f = open("%s/%s_message" % (DATAPATH, task_id), 'w')
        f.write(str(message))
        f.close()

    # 存入所有的节点和节点属性
    def set_network(self):
        logger.debug("save node")
        f = open('E:/graduate/twitter_foursquare/foursquare/users/user', encoding='utf-8')
        twitter_file = open('E:/graduate/twitter_foursquare/twitter/user', encoding='utf-8')
        for line in twitter_file:
            tw_list = line.split('\t')
            user_name = tw_list[0].lower()
            if len(user_name) > 1 and len(tw_list) >= 5:
                self.tw_G.add_node(user_name, time='', location='', word='', fourID=None)

        # foursquare 目前只将对应的twitterid存了进去，其它的属性未存,
        # location=tw_list[4],  realname=tw_list[2], bio=tw_list[3], home=tw_list[4]
        num = 0
        for line in f:
            lis = line.split('\t')
            userFourID = lis[0].lower()
            if 'com' in lis[7]:
                userTwitterID = lis[7].split('twitter.com/')[1].lower()
                if self.tw_G.has_node(userTwitterID):
                    num = num + 1
                    self.four_G.add_node(userFourID, twitterID=userTwitterID, location='', time='', word='', in_test=0)
                    self.tw_G.node[userTwitterID]["fourID"] = userFourID  # 标明 tw对应的four ID
                    self.f_all_anchor_list.append(userFourID)
                    self.t_all_anchor_list.append(userTwitterID)
                else:
                    self.four_G.add_node(userFourID, twitterID=None, location='', time='', word='', in_test=0)
        f.close()
        twitter_file.close()

    # 存入用户的follow关系
    def set_follow(self, random_num, nodes1, nodes2):
        logger.debug("save follow")
        tw_f = open('E:/graduate/twitter_foursquare/twitter/following')
        for line in tw_f:
            user1 = line.split('\t')[0].lower()
            user2 = line.split('\t')[1].split('\n')[0].lower()
            if self.tw_G.has_node(user1) and self.tw_G.has_node(user2):
                if self.tw_G.has_edge(user2, user1):
                    self.tw_G.edges[user2, user1]["weight"] = 2
                    if user1 in self.t_anchor_known_list and user2 in self.f_anchor_known_list:
                        f_user1 = self.tw_G.node[user1]["fourID"]
                        f_user2 = self.tw_G.node[user2]["fourID"]
                        self.four_G.add_edge(f_user1, f_user2, weight=2)
                else:
                    self.tw_G.add_edge(user1, user2, weight=1)
                    if user1 in self.t_anchor_known_list and user2 in self.f_anchor_known_list:
                        f_user1 = self.tw_G.node[user1]["fourID"]
                        f_user2 = self.tw_G.node[user2]["fourID"]
                        self.four_G.add_edge(f_user1, f_user2, weight=1)
        tw_f.close()

        f = open('E:/graduate/twitter_foursquare/foursquare/users/user_following')
        for line in f:
            user1 = line.split('\t')[0].lower()
            user2 = line.split('\t')[1].split('\n')[0].lower()
            if self.four_G.has_node(user1) and self.four_G.has_node(user2):
                if self.four_G.has_edge(user2, user1):
                    self.four_G.edges[user2, user1]["weight"] = 2
                    if user1 in self.f_anchor_known_list and user2 in self.f_anchor_known_list:
                        t_user1 = self.four_G.node[user1]["twitterID"]
                        t_user2 = self.four_G.node[user2]["twitterID"]
                        if self.tw_G.has_edge(t_user1, t_user2):
                            self.tw_G.edges[t_user2, t_user1]["weight"] = 2
                else:
                    self.four_G.add_edge(user1, user2, weight=1)
                    if user1 in self.f_anchor_known_list and user2 in self.f_anchor_known_list:
                        t_user1 = self.four_G.node[user1]["twitterID"]
                        t_user2 = self.four_G.node[user2]["twitterID"]
                        self.tw_G.add_edge(t_user1, t_user2, weight=1)

        # # 删除twitter中的单向关系
        # self.tw_G.remove_edges_from([e for e in self.tw_G.edges() if self.tw_G.edges[e]["weight"] == 1])
        #
        # # 删除边缘节点
        vdict = self.four_G.degree()
        r_node = [v for v in self.four_G if vdict[v] < 3]
        for v in r_node:
            if v in self.f_all_anchor_list:
                self.f_all_anchor_list.remove(v)
                self.t_all_anchor_list.remove(self.four_G.node[v]['twitterID'])
        self.four_G.remove_nodes_from(r_node)

        vdict = self.tw_G.degree()
        r_node = [v for v in self.tw_G if vdict[v] < 3]
        for v in r_node:
            if v in self.t_all_anchor_list:
                self.t_all_anchor_list.remove(v)
                self.f_all_anchor_list.remove(self.tw_G.node[v]['fourID'])
        self.tw_G.remove_nodes_from(r_node)
        # 根据规定数量随机生成网络
        r_node = random.sample(list(self.four_G.nodes), len(self.four_G.nodes)-nodes1)
        for v in r_node:
            if v in self.f_all_anchor_list:
                self.f_all_anchor_list.remove(v)
                self.t_all_anchor_list.remove(self.four_G.node[v]['twitterID'])
        self.four_G.remove_nodes_from(r_node)
        r_node = random.sample(list(self.tw_G.nodes), len(self.tw_G.nodes)-nodes2)
        for v in r_node:
            if v in self.t_all_anchor_list:
                self.t_all_anchor_list.remove(v)
                self.f_all_anchor_list.remove(self.tw_G.node[v]['fourID'])
        self.tw_G.remove_nodes_from(r_node)

        #
        # # 生成事先知道的锚用户
        # self.random_list = [168, 350, 1286, 120, 803, 1093, 736, 130, 1187, 1210, 50, 579, 604, 1135, 1278, 1326, 330, 875, 1390, 95, 173, 698, 1067, 665, 1457, 458, 1281, 1197, 789, 147, 641, 1085, 1239, 13, 512, 343, 808, 539, 1402, 575, 829, 88, 1219, 346, 1221, 911, 1103, 1002, 426, 1414, 772, 373, 104, 162, 666, 809, 307, 1391, 887, 1463, 1060, 448, 1238, 1438, 1164, 419, 85, 949, 756, 7, 896, 954, 1481, 1399, 1468, 1251, 847, 398, 286, 1044, 595, 1176, 622, 1009, 1173, 530, 1094, 107, 1188, 1101, 1070, 793, 450, 1016, 746, 706, 1134, 719, 625, 909, 974, 1317, 890, 1019, 823, 962, 639, 587, 918, 1181, 294, 748, 425, 280, 1150, 1376, 226, 475, 661, 877, 599, 714, 917, 786, 124, 101, 160, 1350, 237, 205, 317, 920, 204, 1227, 105, 1448, 77, 649, 1245, 873, 15, 1088, 966, 672, 366, 1436, 1405, 1112, 175, 251, 108, 969, 1100, 674, 906, 1379, 1035, 891, 1108, 57, 1306, 263, 364, 1119, 1299, 463, 1032, 729, 281, 971, 610, 732, 731, 460, 1471, 945, 761, 525, 78, 150, 468, 1358, 38, 245, 1147, 1024, 788, 1124, 157, 831, 1470, 720, 2, 952, 1480, 279, 109, 1183, 424, 1268, 523, 276, 1036, 28, 930, 380, 540, 1454, 934, 1437, 912, 106, 1460, 697, 899, 801, 296, 686, 1171, 305, 895, 946, 103, 1000, 704, 807, 191, 755, 1250, 1406, 321, 987, 943, 1450, 1469, 1143, 1395, 1479, 135, 1021, 769, 1247, 1426, 614, 1374, 1318, 148, 1081, 678, 922, 423, 898, 629, 96, 230, 859, 222, 27, 312, 1010, 481, 269, 1079, 991, 1389, 832, 358, 90, 394, 257, 411, 667, 1475, 495, 500, 692, 711, 1242, 445, 754, 329, 1284, 180, 1220, 693, 618, 747, 1089, 1215, 1413, 229, 781, 1082, 368, 75, 267, 241, 370, 270, 824]
        self.random_list = random.sample(range(0, len(self.f_all_anchor_list)), random_num)  # 随机生成提前知道的anchor user数
        for i in self.random_list:
            self.f_anchor_known_list.append(self.f_all_anchor_list[i])
            self.four_G.node[self.f_all_anchor_list[i]]["in_test"] = 1
            self.t_anchor_known_list.append(self.t_all_anchor_list[i])

        f = open("E:/graduate/twitter_foursquare/location/four_infor.txt", 'r')
        for line in f:
            s = line.split(';')
            if self.four_G.has_node(s[0]):
                self.four_G.node[s[0]]['location'] = s[2]
                self.four_G.node[s[0]]['time'] = s[3].strip('\n')
        f.close()
        f = open("E:/graduate/twitter_foursquare/location/tw_infor.txt", 'r')
        for line in f:
            s = line.split(';')
            if self.tw_G.has_node(s[0]):
                self.tw_G.node[s[0]]['location'] = s[2]
                self.tw_G.node[s[0]]['time'] = s[3].strip('\n')
        f.close()
        # 将结果存入文件作为demo
        nx.write_gpickle(self.four_G, "E:/graduate/twitter_foursquare/data/%s_foursquare.gpickle" % (self.task_id))
        nx.write_gpickle(self.tw_G, "E:/graduate/twitter_foursquare/data/%s_twitter.gpickle" % (self.task_id))
        message = {"f_anchor_known_list": self.f_all_anchor_list, "t_anchor_known_list": self.t_anchor_known_list, "f_all_anchor_list":self.f_all_anchor_list}
        f = open("E:/graduate/twitter_foursquare/data/%s_message" % (self.task_id), 'a+')
        f.write(str(message))
        f.close()
        # logger.info(self.random_list)
        # logger.info(nx.info(self.tw_G))
        # logger.info(nx.info(self.four_G))
        # print("length of already known anchor list:", len(self.f_anchor_known_list), len(self.t_anchor_known_list))
        # print("length of all anchor list:", len(self.f_all_anchor_list), len(self.t_all_anchor_list))

    def fresh_anchor_known(self, engage):
        s = len(engage.keys())
        random_anchor_list = random.sample(engage.keys(), int(0.8 * s))
        for item in engage.keys():
            if item in random_anchor_list:
                self.four_G.node[item]['twitterID'] = engage[item]
                self.tw_G.node[engage[item]]['fourID'] = item
                self.f_anchor_known_list.append(item)
                self.t_anchor_known_list.append(engage[item])
        # 根据已知的将网络进行扩展
        for item in self.four_G.edges():
            if item[0] in self.f_anchor_known_list and item[1] in self.f_anchor_known_list:
                tw1 = self.four_G.node[item[0]]["twitterID"]
                tw2 = self.four_G.node[item[1]]["twitterID"]
                self.tw_G.add_edge(tw1, tw2)
        for item in self.tw_G.edges():
            if item[0] in self.t_anchor_known_list and item[1] in self.t_anchor_known_list:
                four1 = self.tw_G.node[item[0]]["fourID"]
                four2 = self.tw_G.node[item[1]]["fourID"]
                self.four_G.add_edge(four1, four2)


def del_dur(location):
    s = location.split(',')[0:-1]
    l = list(set(s))
    if 'None' in l:
        l.remove('None')
    return str(l)

@require_http_methods(["GET"])
def get_demo_by_task(request):
    task_id = request.GET.get("demo_name")
    f_nodes = []
    f_edges = []
    t_nodes = []
    t_edges = []
    four_G = nx.read_gpickle("%s/%s_foursquare.gpickle" % (DATAPATH, task_id))
    tw_G = nx.read_gpickle("%s/data/%s_twitter.gpickle" % (DATAPATH, task_id))
    f = open("%s/%s_message" % (DATAPATH, task_id), 'r')
    for item in f:
        message = eval(item)
    f.close()
    f = open("%s/%s_result" % (DATAPATH, task_id), 'r')
    for line in f:
        s = eval(line)
    f.close()
    f_predicted = s["f_predicted"]
    t_predicted = s["t_predicted"]
    # 只展示已知的anchor user之间的关系
    all_neighbors = []
    # logger.debug(len(message.get("t_anchor_known_list")))
    # for item in message.get("t_anchor_known_list"):
    #     if item in four_G.nodes():
    #         f_nei = list(four_G.neighbors(item))
    #         for i in f_nei:
    #             all_neighbors.extend(f_nei)
    for item in range(0, len(f_predicted)):
        f_nodes.append({'id': 'f'+f_predicted[item], 'title': '<p>type:foursquare</p><p>id:'+f_predicted[item]+'</p>'+str("location:" + del_dur(four_G.node[f_predicted[item]]['location'])), 'group': 0})
        f_nodes.append({'id': 't'+t_predicted[item], 'title': '<p>type:twitter</p><p>id:'+t_predicted[item]+'</p>'+str("location:" + del_dur(tw_G.node[t_predicted[item]]['location'])), 'group': 1})
        f_edges.append({'from': 'f'+f_predicted[item], 'to': 't'+t_predicted[item], 'value': 20})

    for item in four_G.edges():
        if item[0] in f_predicted and item[1] in f_predicted:
            f_edges.append({'from': 'f'+item[0], 'to': 'f'+item[1]})

    for item in tw_G.edges():
        if item[0] in t_predicted and item[1] in t_predicted:
            f_edges.append({'from': 't'+item[0], 'to': 't'+item[1]})

    # all_neighbors.extend(message.get("f_anchor_known_list"))
    # f_all_node = list(set(all_neighbors))
    # f_all_node.extend(f_predicted)
    # num = 0
    # for item in f_all_node:
    #     if item in message.get("f_anchor_known_list"):
    #         f_nodes.append({'id': item, 'title': str("id:"+item), 'group': 1})
    #     elif item in f_predicted:
    #         f_nodes.append({'id': item, 'title': str("id:"+item), 'group': 2})
    #     else:
    #         f_nodes.append({'id': item, 'title': str("id:" + item), 'group': 0})
    # for item in four_G.to_directed().edges():
    #     if item[0] in f_all_node and item[1] in f_all_node:
    #         f_edges.append({'from': item[0], 'to': item[1]})

    # t_all_node = list(set(message.get("t_anchor_known_list")))
    # t_all_node.extend(t_predicted)
    # num = 0
    # for item in t_all_node:
    #     if item in message.get("t_anchor_known_list"):
    #         t_nodes.append({'id': item, 'title': str("id:" + item), 'group': 1})
    #     elif item in t_predicted:
    #         t_nodes.append({'id': item, 'title': str("id:" + item), 'group': 2})
    #     else:
    #         t_nodes.append({'id': item, 'title': str("id:" + item), 'group': 0})
    # for item in tw_G.to_directed().edges():
    #     if item[0] in t_all_node and item[1] in t_all_node:
    #         t_edges.append({'from': item[0], 'to': item[1]})
    # for item in four_G.nodes():
    #     if item not in message.get("t_anchor_known_list"):
    #         f_nodes.append({'id': item, 'title': str("id:"+item), 'group': 0})
    #     else:
    #         f_nodes.append({'id': item, 'title': str("id:"+item), 'group': 1})
    # for item in four_G.edges():
    #     if item[0] in f_all_node and item[1] in f_all_node:
    #         f_edges.append({'from': item[0], 'to': item[1]})
    # for item in tw_G.nodes():
    #     if item not in message.get("t_anchor_known_list"):
    #         t_nodes.append({'id': item, 'title': str("id:"+item), 'group': 0})
    #     else:
    #         t_nodes.append({'id': item, 'title': str("id:"+item), 'group': 1})
    # for item in tw_G.edges():
    #     t_edges.append({'from': item[0], 'to': item[1]})
    # predict_anchor_nodes = message.get("predcited_anchor_nodes")
    logger.debug(len(t_edges))
    right = 0
    wrong = 0
    for i in range(0, len(f_predicted)):
        if f_predicted[i] == t_predicted[i]:
            right += 1
        elif f_predicted[i] not in message["f_all_anchor_list"] or t_predicted[i] not in message:
            wrong += 1
    logger.debug((right*2+5357-1772*2-wrong)/5357)
    response = {"twitter": {}, "foursquare": {}, "aligned": {}, "anchor_known_num": len(message["t_anchor_known_list"]), "real_anchor_num": len(message["f_all_anchor_list"])}
    response["foursquare"]["degree"] = nx.info(four_G).split('\n')[4].split(':')[1]
    response["twitter"]["degree"] = nx.info(tw_G).split('\n')[4].split(':')[1]
    response["foursquare"]["nodes"] = {"num": len(four_G.nodes()), "info": f_nodes}
    response["foursquare"]["edges"] = {"num": len(four_G.edges()), "info": f_edges}
    response["foursquare"]["anchor_known_list"] = message["t_anchor_known_list"]
    response["twitter"]["nodes"] = {"num": len(tw_G.nodes()), "info": t_nodes}
    response["twitter"]["edges"] = {"num": len(tw_G.edges()), "info": t_edges}
    response["twitter"]["anchor_known_list"] = message["t_anchor_known_list"]
    response["evaluation"] = s["evaluation"]
    logger.debug(response["evaluation"])
    return JsonResponse(response)


@require_http_methods(["GET"])
def get_network(request):
    four_G = nx.read_gpickle(DATAPATH + "/data/origin/foursquare.gpickle")
    tw_G = nx.read_gpickle(DATAPATH + "/origin/twitter.gpickle")
    f = open(DATAPATH + "/origin/message", 'r')
    for item in f:
        message = eval(item)
    f.close()
    f_nodes = []
    f_edges = []
    t_nodes = []
    t_edges = []
    # for item in four_G.nodes():
    #     if item not in []:
    #         f_nodes.append({'id': item, 'title': str("id:"+item), 'group': 0})
    #     else:
    #         f_nodes.append({'id': item, 'title': str("id:"+item), 'group': 1})
    # for item in four_G.edges():
    #     f_edges.append({'from': item[0], 'to': item[1]})
    # for item in tw_G.nodes():
    #     if item not in []:
    #         t_nodes.append({'id': item, 'title': str("id:"+item), 'group': 0})
    #     else:
    #         t_nodes.append({'id': item, 'title': str("id:"+item), 'group': 1})
    # for item in tw_G.edges():
    #     t_edges.append({'from': item[0], 'to': item[1]})
    response = {"twitter": {}, "foursquare": {}, "anchor_known_num": len([]), "real_anchor_num": len(message["f_all_anchor_list"])}
    response["foursquare"]["nodes"] = {"num": len(four_G.nodes()), "info": f_nodes}
    response["foursquare"]["edges"] = {"num": len(four_G.edges()), "info": f_edges}
    response["foursquare"]["anchor_known_list"] = []
    response["twitter"]["nodes"] = {"num": len(tw_G.nodes), "info": t_nodes}
    response["twitter"]["edges"] = {"num": len(tw_G.edges), "info": t_edges}
    response["twitter"]["anchor_known_list"] = []
    response["foursquare"]["degree"] = nx.info(four_G).split('\n')[4].split(':')[1]
    response["twitter"]["degree"] = nx.info(tw_G).split('\n')[4].split(':')[1]
    return JsonResponse(response)


@require_http_methods(["POST"])
def fresh_network(request):
    four_type = request.POST.get('four_type')
    tw_type = request.POST.get('tw_type')
    anchor_known_num = request.POST.get('anchor_known_number')
    user_name = request.POST.get('user_name')
    degree = request.POST.get('degree')
    logger.debug(request.POST)
    # 生成待启动的task
    user = message.objects.get(username=user_name)
    task_all = task.objects.all()
    for item in task_all:
        if item.already == 0:
            task.objects.get(task_id=item.task_id).delete()
    task_id = task.objects.count() + 1
    tasks = task(task_id=task_id, already=0, user=user)
    tasks.save()

    # 根据社交网络类型进行数据集读取
    four_url = dataset.objects.get(dataset_name=four_type).url
    tw_url = dataset.objects.get(dataset_name=tw_type).url
    four_G = nx.read_gpickle(four_url)
    tw_G = nx.read_gpickle(tw_url)
    # 读取f_all_anchor_known_list和t_all_anchor_knwon_list
    # 这个随机选最好是在选全部的anchor user,从f_all中选，然后删除非对齐的，再确定已知的
    f_message = open('E:/graduate/twitter_foursquare/data/origin/message', 'r')
    for line in f_message:
        message_line = eval(line)
    network = SocialNetwork(tw_G, four_G)
    network.f_all_anchor_list = message_line["f_all_anchor_list"]
    network.t_all_anchor_list = message_line["t_all_anchor_list"]
    network.set_random_network(int(anchor_known_num), int(degree))
    logger.debug(len(network.f_all_anchor_list))
    network.save_file_network(four_type, tw_type, int(task_id))
    # logger.debug(list(network.four_G.nodes()))
    f_nodes = []
    f_edges = []
    t_nodes = []
    t_edges = []
    num = 0
    for item in network.f_anchor_known_list:
        # if item not in network.f_anchor_known_list:
        f_nodes.append({'id': item, 'title': '<p>type:foursquare</p><p>id:'+item+'</p>'+str("location:" + del_dur(four_G.node[item]['location'])), 'group': num})
        num += 1
        # else:
        #     f_nodes.append({'id': item, 'title': str("id:"+item), 'group': 1})
    for item in network.four_G.to_undirected().edges():
        if item[0] in network.f_anchor_known_list and item[1] in network.f_anchor_known_list:
            f_edges.append({'from': item[0], 'to': item[1]})
    num = 0
    for item in network.t_anchor_known_list:
        # if item not in network.t_anchor_known_list:
        t_nodes.append({'id': item, 'title': '<p>type:twitter</p><p>id:'+item+'</p>'+str("location:" + del_dur(tw_G.node[item]['location'])), 'group': num})
        num += 1
        # else:
        #     t_nodes.append({'id': item, 'title': str("id:"+item), 'group': 1})
    for item in network.tw_G.to_undirected().edges():
        if item[0] in network.t_anchor_known_list and item[1] in network.t_anchor_known_list:
            t_edges.append({'from': item[0], 'to': item[1]})
    response = {"twitter": {}, "foursquare": {}, "anchor_known_num": len(network.f_anchor_known_list), "real_anchor_num": len(network.f_all_anchor_list), "task_id": task_id}
    response["foursquare"]["nodes"] = {"num": len(four_G.nodes()), "info": f_nodes}
    response["foursquare"]["edges"] = {"num": len(four_G.edges()), "info": f_edges}
    response["twitter"]["nodes"] = {"num": len(tw_G.nodes()), "info": t_nodes}
    response["twitter"]["edges"] = {"num": len(tw_G.edges()), "info": t_edges}
    return JsonResponse(response)


class myThread (threading.Thread):   # 继承父类threading.Thread
    def __init__(self, name, counter, task_id, choose, al):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = counter
        self.task_id = task_id
        self.choose = choose
        self.al = al

    def run(self):                   # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        four_G = nx.read_gpickle("E:/graduate/twitter_foursquare/data/%s_foursquare.gpickle" % (self.task_id))
        tw_G = nx.read_gpickle("E:/graduate/twitter_foursquare/data/%s_twitter.gpickle" % (self.task_id))
        f = open("E:/graduate/twitter_foursquare/data/%s_message" % (self.task_id), 'r')
        for item in f:
            message = eval(item)
        f.close()
        logger.debug(self.al)
        f_anchor_known_list = message.get("f_anchor_known_list")
        t_anchor_known_list = message.get("t_anchor_known_list")
        networksPair = SocialNetwork(tw_G, four_G)
        networksPair.f_anchor_known_list = f_anchor_known_list
        networksPair.t_anchor_known_list = t_anchor_known_list
        if self.choose == 2:   # 自己定义的算法
            feature = extractFeature.SimplifiedFeature(networksPair)
            classi = classifier.Classifier(networksPair, feature, self.al.get("classifier"))
            matching = strictMatching.StrictStableMatching(networksPair, classifier.result)
            matching.cut_k_list(self.al.get("matching_K"))
            matching.matching()
        else:
            for itera in range(0, self.al.get("ISS_k")):
                logger.debug("run feature")
                feature = extractFeature.SimplifiedFeature(networksPair)
                classi = classifier.Classifier(networksPair, feature, 3)
                matching = strictMatching.StrictStableMatching(networksPair, classi.result)
                networksPair.fresh_anchor_known(matching.engage)
        t = task.objects.get(task_id=self.task_id)
        t.already = 2                          # 已完成
        t.end_date = datetime.datetime.now()   # 完成时间
        t.save()
        aligned = dict()
        aligned["f_anchor_known_list"] = networksPair.f_anchor_known_list
        aligned["t_anchor_known_list"] = networksPair.t_anchor_known_list
        f = open("E:/graduate/twitter_foursquare/data/%s_aligned_result" % (self.task_id), 'a+')
        f.write(str(aligned))
        f.close()


@require_http_methods(["POST"])
def run_al(request):
    task_id = request.POST.get("task_id")
    algorithm = int(request.POST.get("algorithm"))
    matching = int(request.POST.get("matching"))
    al = dict()
    if algorithm == 2:
        if matching == 1:
            al["matching_K"] = None
        elif matching == 2:
            al["matching_K"] = int(request.POST.get("matching_k"))
        else:
            al["matching_K"] = 1
    elif algorithm == 1:
        al["ISS_k"] = int(request.POST.get("iss_k"))
    thread1 = myThread(task_id, 1, int(task_id), int(algorithm), al)
    thread1.start()
    al["Choose"] = algorithm
    t = task.objects.get(task_id = int(task_id))
    t.already = 1
    t.algorithm = al
    t.save()
    response = {"success": "yes"}
    return JsonResponse(response)


@require_http_methods(["GET"])
def get_task_list(request):
    user_name = request.GET.get("user_name")
    user = message.objects.get(username = user_name)
    res = []
    al = {1: 'ISS', 2: 'Customize'}
    ready = {0: 'Not start', 1: 'Running', 2: 'Finished'}
    for item in user.task_set.all():
        if item.algorithm is not None:
            s = eval(item.algorithm)
            s["Choose"] = al[s["Choose"]]
        red = ready[item.already]
        res.append({"start_time": item.start_date.strftime('%Y-%m-%d %H:%M:%S') , "end_time": item.end_date, "task_id": item.task_id, "already": red, "algorithm": s})
    response = {"sucess": "yes", "task": res}
    return JsonResponse(response)

@require_http_methods(["GET"])
def get_task_network(request):
    task_id = request.GET.get("task_name")
    f_nodes = []
    f_edges = []
    t_nodes = []
    t_edges = []
    four_G = nx.read_gpickle("E:/graduate/twitter_foursquare/data/%s_foursquare.gpickle" % (task_id))
    tw_G = nx.read_gpickle("E:/graduate/twitter_foursquare/data/%s_twitter.gpickle" % (task_id))
    f = open("E:/graduate/twitter_foursquare/data/%s_message" % (task_id), 'r')
    for item in f:
        message = eval(item)
    f.close()
    f = open("E:/graduate/twitter_foursquare/data/%s_result" % (task_id), 'r')
    for line in f:
        s = eval(line)
    f.close()
    f_predicted = s["f_predicted"]
    t_predicted = s["t_predicted"]
    # 只展示已知的anchor user之间的关系
    all_neighbors = []
    # logger.debug(len(message.get("t_anchor_known_list")))
    # for item in message.get("t_anchor_known_list"):
    #     if item in four_G.nodes():
    #         f_nei = list(four_G.neighbors(item))
    #         for i in f_nei:
    #             all_neighbors.extend(f_nei)
    for item in range(0, len(f_predicted)):
        f_nodes.append({'id': 'f' + f_predicted[item],
                        'title': '<p>type:foursquare</p><p>id:' + f_predicted[item] + '</p>' + str(
                            "location:" + del_dur(four_G.node[f_predicted[item]]['location'])), 'group': 0})
        f_nodes.append({'id': 't' + t_predicted[item],
                        'title': '<p>type:twitter</p><p>id:' + t_predicted[item] + '</p>' + str(
                            "location:" + del_dur(tw_G.node[t_predicted[item]]['location'])), 'group': 1})
        f_edges.append({'from': 'f' + f_predicted[item], 'to': 't' + t_predicted[item], 'value': 20})

    for item in four_G.edges():
        if item[0] in f_predicted and item[1] in f_predicted:
            f_edges.append({'from': 'f' + item[0], 'to': 'f' + item[1]})

    for item in tw_G.edges():
        if item[0] in t_predicted and item[1] in t_predicted:
            f_edges.append({'from': 't' + item[0], 'to': 't' + item[1]})
    logger.debug(len(t_edges))
    right = 0
    wrong = 0
    for i in range(0, len(f_predicted)):
        if f_predicted[i] == t_predicted[i]:
            right += 1
        elif f_predicted[i] not in message["f_all_anchor_list"] or t_predicted[i] not in message:
            wrong += 1
    logger.debug((right * 2 + 5357 - 1772 * 2 - wrong) / 5357)
    response = {"twitter": {}, "foursquare": {}, "aligned": {}, "anchor_known_num": len(message["t_anchor_known_list"]),
                "real_anchor_num": len(message["f_all_anchor_list"])}
    response["foursquare"]["degree"] = nx.info(four_G).split('\n')[4].split(':')[1]
    response["twitter"]["degree"] = nx.info(tw_G).split('\n')[4].split(':')[1]
    response["foursquare"]["nodes"] = {"num": len(four_G.nodes()), "info": f_nodes}
    response["foursquare"]["edges"] = {"num": len(four_G.edges()), "info": f_edges}
    response["foursquare"]["anchor_known_list"] = message["t_anchor_known_list"]
    response["twitter"]["nodes"] = {"num": len(tw_G.nodes()), "info": t_nodes}
    response["twitter"]["edges"] = {"num": len(tw_G.edges()), "info": t_edges}
    response["twitter"]["anchor_known_list"] = message["t_anchor_known_list"]
    response["evaluation"] = s["evaluation"]
    logger.debug(response["evaluation"])
    return JsonResponse(response)


@require_http_methods(["GET"])
def del_task(request):
    task_id = request.GET.get("task_name")
    try:
        task.objects.filter(task_id=task_id).delete()
        for item in ["message", "twitter.gpickle", "foursquare.gpickle"]:
            file_path = "/graduate/twitter_foursquare/data/%s_%s" % (task_id, item)
            if os.path.exists(file_path):
                os.remove(file_path)
        response = {"success": "yes"}
    except:
        response = {"success": "no"}
    return JsonResponse(response)

@require_http_methods(["GET"])
def get_dataset_list(request):
    data = dataset.objects.all()
    l = list()
    for item in data:
        l.append({"id": item.id, "name": item.dataset_name, "url": item.url})
    response = {"datasetlist": l}
    return JsonResponse(response)

@require_http_methods(["POST"])
def operate_dataset(request):
    data = request.POST.get("name")
    operate = int(request.POST.get("operation")) # 1是删除 2是增加
    url = request.POST.get("url")
    logger.debug(data)
    logger.debug(operate)
    try:
        if operate == 1:
            source = dataset.objects.get(id=data).delete()
        else:
            source = dataset(dataset_name=data, url=url)
            source.save()
        response = {"success": "yes"}
    except:
        response = {"success": "no"}
    return JsonResponse(response)

@require_http_methods(["POST"])
def upload_dataset(request):
    logger.debug(request)

@require_http_methods(["GET"])
def get_user_list(request):
    user_list = message.objects.all()
    s = []
    for item in user_list:
        s.append({"username": item.username, "authority": str(item.Authority)})
    response = {"user_list": s}
    logger.debug(s)
    return JsonResponse(response)

@require_http_methods(["POST"])
def login(request):
    name = request.POST.get('name')
    passwd = request.POST.get('passwd')
    logger.debug(name)
    user = message.objects.get(username=name)
    logger.debug(user)
    if passwd == user.password:
        response = {"success": "yes", "authority": user.Authority}
        logger.debug(response)
        return JsonResponse(response)
    else:
        response = {"success": "no"}
        return JsonResponse(response)