# gdrive-client -- Google Drive Client

List and download files


## 1. 設定

### 1.1 Google Drive APIの利用登録

[Google Drive Console](https://console.developers.google.com/) で、
認証情報(JSONファイル)を作成し、ダウンロードする。

1. プロジェクトを作成
2. 「Google Drive API」を`有効にする`
3. 認証情報(`OAuth クライアント ID`)を作成
4. 認証情報(JSONファイル)をダウンロード
   ファイル名: `client_secret.json`


### 1.2 認証情報の設定

* 下記の通りインストールして、最初は
  ブラウザが起動できる環境で`gdrive-client.sh`を実行する！
* sshでリモートログインしている場合は要注意！
* 2回目以降は、GUIやブラウザは不要。


## 2. Install

```bash
$ cd
$ python3 -m venv env1
$ cd env1
$ . ./bin/activate
(env1)$ git clone https://github.com/ytani01/gdrive-client.git
(env1)$ cd gdrive-client
(env1)$ pip install -r requirements.txt
(env1)$ cp {上記で保存した client_secret.json} .
```

## 3. usage

ヘルプ参照

```bash
$ gdrive-client.sh ~/env1 -h
```


## A. 参考

* https://note.nkmk.me/python-pydrive-download-upload-delete/
