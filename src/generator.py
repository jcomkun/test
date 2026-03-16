"""
投稿文生成モジュール
Claude APIを使ってX(Twitter)の投稿文を生成する
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


def load_prompt_template() -> str:
    prompt_file = PROMPTS_DIR / "tweet_prompt.md"
    if not prompt_file.exists():
        raise FileNotFoundError(f"プロンプトテンプレートが見つかりません: {prompt_file}")
    return prompt_file.read_text(encoding="utf-8")


def load_input(input_path: str) -> str:
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"入力ファイルが見つかりません: {input_path}")
    return path.read_text(encoding="utf-8")


def generate_tweet(input_text: str) -> str:
    """Claude APIを使って投稿文を生成する"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt_template = load_prompt_template()

    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=512,
        thinking={"type": "adaptive"},
        system=prompt_template,
        messages=[
            {"role": "user", "content": f"以下の内容をもとにツイートを生成してください:\n\n{input_text}"}
        ],
    ) as stream:
        tweet = ""
        for text in stream.text_stream:
            print(text, end="", flush=True)
            tweet += text

    print()  # 改行
    return tweet.strip()


def save_tweet(tweet: str) -> Path:
    """生成したツイートをoutputs/に保存する"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUTS_DIR / f"tweet_{timestamp}.txt"
    output_path.write_text(tweet, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Claude APIでX(Twitter)投稿文を生成する")
    parser.add_argument("input_file", help="素材ファイルのパス (例: inputs/article.txt)")
    parser.add_argument("--post", action="store_true", help="生成後にXへ投稿する")
    args = parser.parse_args()

    # 入力読み込み
    try:
        input_text = load_input(args.input_file)
    except FileNotFoundError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)

    # 投稿文生成
    print("--- 投稿文を生成中... ---")
    try:
        tweet = generate_tweet(input_text)
    except anthropic.AuthenticationError:
        print("エラー: ANTHROPIC_API_KEY が無効です。.env を確認してください。", file=sys.stderr)
        sys.exit(1)
    except anthropic.APIConnectionError:
        print("エラー: Anthropic APIに接続できませんでした。ネットワークを確認してください。", file=sys.stderr)
        sys.exit(1)

    # 文字数チェック（X は140文字制限）
    if len(tweet) > 140:
        print(f"\n⚠️  警告: 生成された投稿が {len(tweet)} 文字あります（X の上限は140文字）")
    else:
        print(f"\n✅ 文字数: {len(tweet)} / 140")

    # 保存
    output_path = save_tweet(tweet)
    print(f"💾 保存: {output_path}")

    # X へ投稿
    if args.post:
        from poster import post_tweet
        print("\n--- Xに投稿中... ---")
        post_tweet(tweet)


if __name__ == "__main__":
    main()
