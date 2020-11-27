# 応募数予測アプリ

### Webアプリへのリンク：https://evening-hamlet-30040.herokuapp.com/
test_x.csvをアップロードすると，予測データ(result.csv)ダウンロードすることができます．  
(読み込み・予測に少し時間がかかります)

アップロード画面  
![アップロード画面](https://user-images.githubusercontent.com/39262759/100361990-3037c900-303e-11eb-9c86-7efca2129155.png)


ダウンロード画面  
![ダウンロード画面](https://user-images.githubusercontent.com/39262759/100362042-4180d580-303e-11eb-9d0d-8e5285fdd7ed.png)

# 用いた回帰モデル

GBDTを使用しています．
詳しいコードはapp/predict/predict.pyにあります．  
試行錯誤した([回帰モデル作成のリポジトリ](https://github.com/NatsukiH/apply_prediction)内のsubmit_GBDT_NaN.ipynbをもとにしています)

# 所感
読み込みと予測に時間がかかりすぎる問題をどうにかしたかったと少し後悔しています．  
(課題締め切り直前で下手に変更して急に動かなくなってしまうのを恐れて，処理が速い学習モデルに変更することができませんでした)  
とはいえ，初めてflaskに触る良い機会になりました．機械学習をWEBアプリに組み込むのも初体験だったため悪戦苦闘しながら組み込みましたが，上手く形になって良かったです．  

# 雑なメモ
参考にしたページ・詰まったところなどを自分用に雑にまとめています．  
https://www.notion.so/WEB-6da2aae3ea3740f98e840ea1783d9b11

