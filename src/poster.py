"""
X(Twitter) 投稿モジュール
Tweepy を使って X(Twitter) に投稿する
"""

import argparse
import os
import sys
from pathlib import Path

import tweepy
from dotenv import load_dotenv

load_dotenv()


def get_twitter_client() -> tweepy.Client:
    """X(Twitter) API クライアントを初期化する"""
    required_vars = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"]
    missing = [v for v in required_vars if not os.environ.get(v)]
    if missing:
        raise EnvironmentError(
            f"以下の環境変数が設定されていません: {', '.join(missing)}\n"
            ".env を確認してください。"
        )

    return tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )


def post_tweet(text: str) -> str:
    """X(Twitter) にツイートを投稿する。投稿IDを返す。"""
    if len(text) > 140:
        raise ValueError(f"投稿文が長すぎます ({len(text)} 文字)。140文字以内にしてください。")

    client = get_twitter_client()
    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    print(f"✅ 投稿完了! Tweet ID: {tweet_id}")
    print(f"   URL: https://x.com/i/web/status/{tweet_id}")
    return tweet_id


def main():
    parser = argparse.ArgumentParser(description="X(Twitter) に投稿する")
    parser.add_argument("tweet_file", help="投稿するテキストファイルのパス (例: outputs/tweet_xxx.txt)")
    args = parser.parse_args()

    tweet_path = Path(args.tweet_file)
    if not tweet_path.exists():
        print(f"エラー: ファイルが見つかりません: {tweet_path}", file=sys.stderr)
        sys.exit(1)

    tweet_text = tweet_path.read_text(encoding="utf-8").strip()
    print(f"--- 投稿内容 ({len(tweet_text)} 文字) ---")
    print(tweet_text)
    print("---")

    try:
        post_tweet(tweet_text)
    except ValueError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except EnvironmentError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except tweepy.TweepyException as e:
        print(f"X API エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
