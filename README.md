# synthesizer_ball
シンセサイザーボールのプロジェクト

◾ mozziの使用方法
①gitHubでmozziのライブラリをダウンロード
　　　http://sensorium.github.com/Mozzi/
②ArduinoIDEに登録
③ボードのdigital9Pin、GNDにスピーカーを接続
④シリアルモニター上から以下の数字を送信する
　(0:停止　1:A音源再生　2:B音源再生　3:BGM再生)

※1 A音源は現在コメントアウト中で無効にしているので0か2か3を送信
※2 基本はループ再生だがB音源は１回再生したら停止するようにしている

◾︎ medal.pyについて
　・必要モジュール
　　以下の記事を元にbluepyをインストール
　　http://tomosoft.jp/design/?p=8104

　　sudo python medal.py　で実行
    ※もしbtleが見つからないと言われたらbluepyの
    　ディレクトリにmedal.pyを入れて実行する