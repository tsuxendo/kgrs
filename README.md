# kgrs 京都市体育館施設予約システム

東山体育館の自動抽選予約を行うプログラムです。

## セットアップ

このリポジトリをダウンロードして、ホームディレクトリにフォルダ名 `kgrs` で展開してください。

Chromeのバージョンを更新したのち、確認してください。

https://chromedriver.chromium.org/downloads

より近いバージョンのドライバを探し, そのバージョンをメモしてください

#### windows

最初に以下を1行1行コマンドプロンプトから実行してください。

```prompt
cd %userprofile%\kgrs
py -m venv venv
call venv\Scripts\activate.bat
pip install selenium pandas chrome-driver==（クロームドライバのバージョン番号）
deactivate
```

#### mac

最初に以下を1行1行ターミナルから実行してください。

```sh
cd ~/kgrs
python3 -m venv venv
. venv/bin/activate
pip install selenium pandas chrome-driver-binary==（クロームドライバのバージョン番号）
deactivate
```

## 実行

`datetime.csv` `user.csv` を用意してください.

### `datetime.csv`

予約日時の設定CSVファイルです。

> 例）
>
> ```csv
> year,month,day,time_code
> 年,月,日,時間帯コード
> 年,月,日,時間帯コード
> 年,月,日,時間帯コード
> 年,月,日,時間帯コード
> 年,月,日,時間帯コード
> ...
> ```

時間帯コードは以下の通りです。

|コード|時間帯|
|:-:|:-:|
|0|9〜11 時|
|1|11〜13 時|
|2|13〜15 時|
|3|15〜17 時|
|4|17〜19 時|
|5|19〜21 時|

### `user.csv` 

ユーザーの設定CSVファイルです。

> 例）
>
> ```csv
> user_id,password,fullname
> ユーザーID,パスワード,名前
> ユーザーID,パスワード,名前
> ユーザーID,パスワード,名前
> ユーザーID,パスワード,名前
> ...
> ```

### windows

以下を1行1行コマンドプロンプトから実行してください。

```prompt
cd %userprofile%\kgrs
call venv\Scripts\activate.bat
py reserve.py
deactivate
```

### mac

以下を1行1行ターミナルから実行してください。

```sh
cd ~/kgrs
. venv/bin/activate
python3 reserve.py
deactivate
```
