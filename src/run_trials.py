#!/usr/bin/env python3
"""
rustshogi Evaluator 試行処理

PostgreSQLデータベースのレコードに対してランダム対局を実行し、勝利数を更新する処理
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evaluator_utils import create_evaluator, check_environment, print_connection_info


def run_trials(games_per_record=100, max_records=None):
    """ランダム対局を実行して勝利数を更新"""
    print("rustshogi Evaluator 試行処理")
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

    # ランダム対局を実行して勝利数を更新
    print("4. ランダム対局を実行中...")
    print(f"   レコードあたりのゲーム数: {games_per_record}")
    if max_records:
        print(f"   最大更新レコード数: {max_records}")
    else:
        print("   更新レコード数: 全レコード")

    try:
        updated_count = evaluator.update_records_with_random_games(
            games_per_record, max_records, 8
        )
        print(f"   ✅ 更新されたレコード数: {updated_count}")
        return True
    except Exception as e:
        print(f"   ❌ 対局実行エラー: {e}")
        return False


def main():
    """メイン処理"""
    import argparse

    parser = argparse.ArgumentParser(description="ランダム対局を実行して勝利数を更新")
    parser.add_argument(
        "--games-per-record",
        type=int,
        default=100,
        help="レコードあたりのゲーム数 (デフォルト: 100)",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        help="最大更新レコード数 (指定しない場合は全レコード)",
    )

    args = parser.parse_args()

    success = run_trials(args.games_per_record, args.max_records)

    if success:
        print("\n🎉 試行処理が完了しました！")
        print("📁 PostgreSQLデータベースの勝利数が更新されました。")
    else:
        print("\n❌ 試行処理が失敗しました。")
        sys.exit(1)


if __name__ == "__main__":
    main()
