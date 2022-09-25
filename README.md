# kareobana

文字化け復元**支援**ツール「枯れ尾花」です。

UTF-8の文章をShift-JISで解釈して（糸編の漢字が多い）文字化けしたスクリーンショットを全手動で復元する機会が多かったので、少しでも自動化しました。

文字をCNN(with Neural Network Console)で学習し、Tesseract-OCRで文字の位置を認識し一文字ずつ切り取り推論をします。

現状精度はまちまちいまいちですが、全部を手動で検索・入力するよりはマシです。

# Usage

[Releases](https://github.com/OLIET2357/kareobana/releases)からTensorflowのsaved_modelをダウンロードしてルートディレクトリに置きます。

`python ocr.py [スクリーンショットのパス]` で認識した文字列が表示されます。

注意点としてOpenCVの制限で画像に日本語パスは使えません。

`-d`でデバッグ画像の出力、`-r`で文字のランキング表示を行います。

黒地に白字の画像のときには`-i`オプションを付けてください。
