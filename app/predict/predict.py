from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import sklearn

import xgboost as xgb
from sklearn.metrics import log_loss
from sklearn.externals import joblib

# ---------データの読み込み-------------------------
application = pd.read_csv("train_x.csv")
df_y = pd.read_csv("train_y.csv")


# ----------前処理---------------------------
# 全てnanのcolumnを削除
a_1 = application.dropna(how='all', axis=1)


# 各行においてユニークな値のリスト
nunipue_count_list = list(a_1.nunique(dropna=False))
# 列名のリスト
a_1_columns_list = a_1.columns.values
# ユニークな値が1つだけの行を除外する
a_2 = a_1.copy()

for index in range(len(nunipue_count_list)):
    #     ユニークな値が1つだけの時
    if nunipue_count_list[index] == 1:
        column_name = a_1_columns_list[index]
        a_2 = a_2.drop([column_name], axis=1)


# nanのカウント
null_count = list(a_2.isnull().sum())
# 列名のリスト
a_2_columns_list = a_2.columns.values
# NANが10000以上の指標を削除してみる
a_3 = a_2.copy()

for index in range(len(null_count)):
    #     NANが10000以上のとき
    if null_count[index] >= 10000:
        column_name = a_2_columns_list[index]
        a_3 = a_3.drop([column_name], axis=1)


# 長い文章のカラムを削除
a_4 = a_3.drop(["休日休暇　備考", "期間・時間　勤務時間", "お仕事名", "（派遣先）配属先部署", "仕事内容",  "応募資格",
                "派遣会社のうれしい特典", "お仕事のポイント（仕事PR）", "（派遣先）職場の雰囲気", "給与/交通費　備考"], axis=1)
a_4 = a_4.drop(["勤務地　最寄駅2（駅名）", "勤務地　最寄駅2（沿線名）"], axis=1)

a_5 = a_4.drop(["勤務地　備考", "期間・時間　勤務開始日", "勤務地　最寄駅1（沿線名）",
                "勤務地　最寄駅1（駅名）", "掲載期間　終了日"], axis=1)


# 掲載開始日を０，１にエンコード
day_mapping = {"2019/11/27": 0, "2019/9/25": 1}
a_5["掲載期間　開始日"] = a_5['掲載期間　開始日'].map(day_mapping)

# 拠点番号のエンコード


def func(x): return int(x[:3])


a_5["拠点番号"] = a_5["拠点番号"].map(func)

application_after = a_5


y = df_y["応募数 合計"]
X = application_after.drop(["お仕事No."], axis=1)

y_array = np.array(y)
X_array = np.array(X)

# train/testに分割する
X_train, X_test, y_train, y_test = train_test_split(
    X_array, y_array, test_size=0.4, random_state=0)


# -------GBDTで学習-------------------------

# 特徴量と目的変数をxboostのデータ構造に変換する
dtrain = xgb.DMatrix(X_train, label=y_train)
dvalid = xgb.DMatrix(X_test, label=y_test)
# dtest = xgb.DMatrix(submit_x_test)

# ハイパーパラメータの設定
param = {"object": "reg:squarederror", "silent": 1, "random_state": 71}
num_round = 53

# 学習の実行
# バリデーションデータもモデルに渡し、学習の進行とともにスコアがどう変わるかモニタリングする
# watchlistには学習データおよびバリデーションデータをセットする
watchlist = [(dtrain, "train"), (dvalid, "eval")]
model = xgb.train(param, dtrain, num_round, evals=watchlist)

# バリデーションデータでのスコアの確認
va_pred = model.predict(dvalid)

score = np.sqrt(mean_squared_error(va_pred, y_test))
print(score)


# 学習済みモデルの保存
joblib.dump(model, "gbdt.pkl", compress=True)
