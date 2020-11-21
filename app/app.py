# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from werkzeug.utils import secure_filename
from flask import Flask, render_template

# requestをインポート
from flask import request
from flask import render_template

# Flaskオブジェクトの生成
app = Flask(__name__)


# 「/」へアクセスがあった場合に、"Hello World"の文字列を返す
@app.route("/")
def hello():
    return "Hello World"


# 「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/index")
def index():
    return render_template("index.html")


# クライアントの命名したファイル名を利用するためのsecure_filename()

# 「/uploads」へアクセスがあった場合に、「uploads.html」を返す
@app.route('/uploads', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files["the_file"]

        # 任意の階層をフルパスで指定(macの場合。任意のユーザー名は変更してください。)
        # f.save('/Users/任意のユーザー名/Python/myproject/uploads/' + secure_filename(f.filename))

        # アップロードしてサーバーにファイルが保存されたらfinishedを表示
        return render_template('finished.html')
    else:
        # GETでアクセスされた時、uploadsを表示
        return render_template('uploads.html')


# おまじない
if __name__ == "__main__":
    app.run(debug=True)
