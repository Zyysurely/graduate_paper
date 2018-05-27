from sklearn.ensemble import RandomForestClassifier
from ..logconfig import logger
# # from svm import *
# from svmutil import *
from sklearn.ensemble import AdaBoostClassifier  # 多个弱分类器的集成判定
from sklearn.tree import DecisionTreeClassifier  # 定义弱分类器
from sklearn import svm

class Classifier(object):
    def __init__(self, socialnetwork, feature, choose):
        self.socialnetwork = socialnetwork
        self.feature = feature
        self.choose = choose
        self.result = self.run_classifier()

    def run_classifier(self):
        logger.debug("run classifier")
        # 随机森林训练
        if self.choose == 1:      #RF
            clf = RandomForestClassifier(n_estimators=100, max_depth=None, min_samples_split=2)
            # clf = clf.fit(self.feature.x, self.feature.y)
            # print(clf.feature_importances_)  # 每个特征的重要性
            # s = clf.predict_proba(self.feature.xt)
        elif self.choose == 2:    # SVM
            clf = svm.SVC()
        else:    # adaBoosting
            weakClassifier = DecisionTreeClassifier(max_depth=1)
            clf = AdaBoostClassifier(base_estimator=weakClassifier, algorithm='SAMME', n_estimators=300,
                                     learning_rate=0.8)
        clf = clf.fit(self.feature.x, self.feature.y)
        s = clf.predict_proba(self.feature.xt)
        print(len(self.feature.xt))
        classify_result = []
        for i in range(0, len(s)):
            classify_result.append(self.feature.name[i] + ';' + str([s[i][0], s[i][1]]))
        return classify_result

        # # svm模型
        # prob = svm_problem(y, x)
        # # -t为选择核函数类型，0为线性，其它全设置为默认参数不调整
        # param = svm_parameter('-t 0')
        # model = svm_train(prob, param, '-h 0')
        # p_label, p_acc, p_val = svm_predict(yt, xt, model, '-b 0')
        # classify_result = []
        # for i in range(0, len(p_label)):
        #     classify_result.append(self.feature.name[i] + ';' + str([p_val[i], 0]))
