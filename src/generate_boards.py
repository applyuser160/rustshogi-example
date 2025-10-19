#!/usr/bin/env python3
"""
rustshogi Evaluator 盤面生成処理

PostgreSQLデータベースにランダム盤面を生成・保存する処理
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evaluator_utils import create_evaluator, check_environment, print_connection_info


def generate_boards(count=200):
    """ランダム盤面を生成・PostgreSQLに保存"""
    print("rustshogi Evaluator 盤面生成処理")
    print("=" * 50)

    check_environment()
    print()
    print_connection_info()

    # PostgreSQL Evaluatorインスタンスを作成
    print("\n2. PostgreSQL Evaluatorインスタンスを作成中...")
    evaluator = create_evaluator()

    # PostgreSQLデータベースを初期化
    print("3. PostgreSQLデータベースを初期化中...")
    try:
        evaluator.init_database()
        print("   ✅ PostgreSQLデータベースの初期化が完了しました")
    except Exception as e:
        print(f"   ❌ データベース初期化エラー: {e}")
        print("   💡 PostgreSQLサーバーが起動していることを確認してください")
        print("   💡 接続文字列が正しいことを確認してください")
        return False

    # ランダム盤面を生成・保存
    print(f"4. {count}個のランダム盤面を生成・PostgreSQLに保存中...")
    try:
        saved_count = evaluator.generate_and_save_random_boards(count)
        print(f"   ✅ 保存された盤面数: {saved_count}")
        return True
    except Exception as e:
        print(f"   ❌ 盤面保存エラー: {e}")
        return False


def main():
    """メイン処理"""
    import argparse

    parser = argparse.ArgumentParser(description="ランダム盤面を生成・保存")
    parser.add_argument(
        "--count", type=int, default=200, help="生成する盤面数 (デフォルト: 200)"
    )

    args = parser.parse_args()

    success = generate_boards(args.count)

    if success:
        print("\n🎉 盤面生成処理が完了しました！")
        print("📁 PostgreSQLデータベースにランダム盤面が保存されました。")
    else:
        print("\n❌ 盤面生成処理が失敗しました。")
        sys.exit(1)


if __name__ == "__main__":
    main()
