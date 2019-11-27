import pandas as pd
from sklearn import cross_validation, metrics
from sklearn.ensemble import RandomForestClassifier

# データの読み込み
mr = pd.read_csv("mushroom.csv", header=None)

# データ中の分類変数を展開する
label = []
data = []
attr_list = []
for row_index, row in mr.iterrows():
    label.append(row.ix[0])
    exdata = []
    for col, v in enumerate(row.ix[1:]):
        if row_index == 0:
            attr = {"dic": {}, "cnt":0}
            attr_list.append(attr)
        else:
            attr = attr_list[col]
        # キノコの特徴を表す記号を12列で表す
        d = [0,0,0,0,0,0,0,0,0,0,0,0]
        if v in attr["dic"]:
            idx = attr["dic"][v]
        else:
            idx = attr["cnt"]
            attr["dic"][v] = idx
            attr["cnt"] += 1
        d[idx] = 1
        exdata += d
    data.append(exdata)


# 学習用とテスト用データに分ける
data_train, data_test, label_train, label_test = \
    cross_validation.train_test_split(data, label)
#データの学習
clf = RandomForestClassifier()
clf.fit(data_train, label_train)
# データを予測
predict = clf.predict(data_test)
# 合っているか結果を確認
ac_score = metrics.accuracy_score(label_test, predict)
print("正解率=", ac_score)


