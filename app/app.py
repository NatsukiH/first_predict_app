# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from werkzeug.utils import secure_filename
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory

import os

import numpy as np
import pandas as pd
import xgboost as xgb
import sklearn
from sklearn.metrics import log_loss
from sklearn.externals import joblib

import pickle

# Flaskオブジェクトの生成
app = Flask(__name__)


# 前処理を行う
def preprocesse(test_matrix):
    # 学習の際に用いたカラムのみを抽出
    column_list = ['職場の様子', '休日休暇(月曜日)', '（派遣先）配属先部署　男女比　男', '大手企業', '交通費別途支給',
                   '（派遣先）配属先部署　人数', '残業月20時間以上', '職種コード', '1日7時間以下勤務OK', '短時間勤務OK(1日4h以内)',
                   '駅から徒歩5分以内', '学校・公的機関（官公庁）', '土日祝のみ勤務', '掲載期間　開始日', 'Wordのスキルを活かす',
                   '勤務地　最寄駅1（分）', 'お仕事No.', '派遣スタッフ活躍中', '大量募集', 'Accessのスキルを活かす',
                   '休日休暇(火曜日)', '平日休みあり', '勤務地　最寄駅2（駅からの交通手段）', 'フラグオプション選択', '期間・時間　勤務期間',
                   '派遣形態', '週2・3日OK', '勤務先公開', 'Excelのスキルを活かす', '16時前退社OK', '正社員登用あり',
                   '残業月20時間未満', '英語力不要', '拠点番号', '休日休暇(日曜日)', '社員食堂あり', '10時以降出社OK',
                   '英語以外の語学力を活かす', '休日休暇(祝日)', '外資系企業', '服装自由', 'PowerPointのスキルを活かす',
                   '（派遣先）配属先部署　男女比　女', '休日休暇(土曜日)', '休日休暇(木曜日)', '（派遣先）配属先部署　平均年齢',
                   '英語力を活かす', '会社概要　業界コード', '勤務地　都道府県コード', 'PCスキル不要', '車通勤OK', '制服あり',
                   '休日休暇(水曜日)', '仕事の仕方', '勤務地　最寄駅1（駅からの交通手段）', '紹介予定派遣', 'シフト勤務', '経験者優遇',
                   '週4日勤務', '未経験OK', '土日祝休み', '給与/交通費　交通費', '休日休暇(金曜日)', '扶養控除内',
                   '給与/交通費　給与下限', 'オフィスが禁煙・分煙', '勤務地　市区町村コード', '勤務地　最寄駅2（分）', '残業なし']
    t_x_1 = test_matrix[column_list]

    t_x_2 = t_x_1.replace('2019/10/24', 3)

    def func(x): return int(x[:3])
    t_x_2["拠点番号"] = t_x_2["拠点番号"].map(func)

    return t_x_2


# クライアントの命名したファイル名を利用するためのsecure_filename()

# 「/uploads」へアクセスがあった場合に、「uploads.html」を返す
@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files["the_file"]

        # 任意の階層をフルパスで指定(macの場合。任意のユーザー名は変更してください。)
        f.save('C:/Users/natsu/Documents/workspace/workschool/first_predict_app/uploads/' +
               secure_filename(f.filename))

        # ------予測する-------
        # ニューラルネットワークのモデルを読み込み
        # 現在のディレクトリを取得
        path = os.path.abspath(__file__)[:-11]
        model_name = path + '/app/predict/gbdt.pkl'
        model = joblib.load(model_name)

        # with open('/predict/model.pickle', mode='rb') as f:  # with構文でファイルパスとバイナリ読み来みモードを設定
        #     model = pickle.load(f)                  # オブジェクトをデシリアライズ

        # テストデータの読み込み
        t_x = pd.read_csv(path + '/uploads/' + f.filename)
        submit_x = preprocesse(t_x)
        work_number = submit_x["お仕事No."]
        submit_x_test = np.array(submit_x.drop(["お仕事No."], axis=1))
        dtest = xgb.DMatrix(submit_x_test)

        pred = model.predict(dtest)

        # -------結果ファイルの作成----------
        pred_df = pd.DataFrame(pred, columns=['応募数 合計'])
        submit = pd.concat([work_number, pred_df], axis=1)
        submit.to_csv(path + "/results/result.csv",
                      index=False, encoding="utf-8_sig")

        # アップロードしてサーバーにファイルが保存されたらdownloadsを表示
        return render_template('downloads.html')
    else:
        # GETでアクセスされた時、uploadsを表示
        return render_template('uploads.html')


@app.route("/downloads")
def downloads_file():
    # 現在のディレクトリを取得
    path = os.path.abspath(__file__)[:-11]
    return send_from_directory(
        directory=path + '/results',
        filename='result.csv',
        as_attachment=True,
        attachment_filename='result.csv',
    )


# おまじない
if __name__ == "__main__":
    app.run(debug=True)
