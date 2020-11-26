# 応募数予測アプリ

test_x.csvをアップロードすると，予測データ(result.csv)ダウンロードすることができます．  
(予測するのに少し時間がかかります)

アップロード画面  
![アップロード画面](https://user-images.githubusercontent.com/39262759/100361990-3037c900-303e-11eb-9c86-7efca2129155.png)


ダウンロード画面  
![ダウンロード画面](https://user-images.githubusercontent.com/39262759/100362042-4180d580-303e-11eb-9d0d-8e5285fdd7ed.png)

# 用いた回帰モデル

GBDTを使用しています．
詳しいコードはapp/predict/predict.pyにあります．  
([試行錯誤したGithubのリポジトリ](https://github.com/NatsukiH/apply_prediction)内のsubmit_GBDT_NaN.ipynbをもとにしています)
