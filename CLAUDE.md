# SNS投稿自動生成プロジェクト

## 概要
X(Twitter)への投稿文をClaude APIで自動生成・投稿するツール。
素材ファイル（テキスト、URLなど）を `inputs/` に置いてコマンドを実行すると、
Claude APIが投稿文を生成し、X(Twitter)に投稿する。

## ディレクトリ構成

```
.
├── CLAUDE.md              # このファイル（Claude Codeへの指示書）
├── .env                   # APIキー（Gitにコミットしない）
├── .gitignore
├── requirements.txt
├── src/
│   ├── generator.py       # Claude APIで投稿文を生成
│   └── poster.py          # X(Twitter) APIへ投稿
├── prompts/
│   └── tweet_prompt.md    # 投稿生成用プロンプトテンプレート
├── inputs/                # 素材ファイル置き場
└── outputs/               # 生成した投稿の確認・保存用
```

## セットアップ

```bash
pip install -r requirements.txt
cp .env.example .env  # .env を編集してAPIキーを設定
```

## よく使うコマンド

```bash
# 投稿文の生成（素材ファイルを指定）
python src/generator.py inputs/article.txt

# 生成した投稿をXに投稿
python src/poster.py outputs/latest_tweet.txt

# 生成から投稿まで一括実行
python src/generator.py inputs/article.txt --post
```

## 環境変数（.env）

| 変数名 | 説明 |
|--------|------|
| `ANTHROPIC_API_KEY` | Anthropic Claude APIキー |
| `X_API_KEY` | X(Twitter) API Key |
| `X_API_SECRET` | X(Twitter) API Secret |
| `X_ACCESS_TOKEN` | X(Twitter) Access Token |
| `X_ACCESS_TOKEN_SECRET` | X(Twitter) Access Token Secret |

## コーディングルール

- APIキーは必ず `.env` で管理し、コードにハードコードしない
- 生成した投稿は `outputs/` に保存してから投稿する（確認のため）
- エラー時は分かりやすいメッセージを出力する
- 投稿前に文字数チェックを行う（X は140文字制限）

## 依存ライブラリ

- `anthropic` - Claude API クライアント
- `tweepy` - X(Twitter) API クライアント
- `python-dotenv` - 環境変数管理
