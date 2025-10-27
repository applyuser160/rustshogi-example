#!/usr/bin/env python3
"""
rustshogi Evaluator 試行処理

PostgreSQLデータベースのレコードに対してランダム対局を実行し、勝利数を更新する処理
"""

import sys
import os
import time
from datetime import datetime, timedelta

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
            games_per_record, max_records, 4
        )
        print(f"   ✅ 更新されたレコード数: {updated_count}")
        return True
    except Exception as e:
        print(f"   ❌ 対局実行エラー: {e}")
        return False


def run_trials_batch(
    evaluator,
    games_per_record=100,
    max_records=None,
    repeat_count=1,
    interval_minutes=2,
):
    """バッチを指定回数繰り返してランダム対局を実行"""
    print("rustshogi Evaluator バッチ試行処理")
    print("=" * 50)
    print(f"繰り返し回数: {repeat_count}")
    print(f"インターバル: {interval_minutes}分")
    print(f"レコードあたりのゲーム数: {games_per_record}")
    if max_records:
        print(f"最大更新レコード数: {max_records}")
    else:
        print("更新レコード数: 全レコード")
    print()

    total_updated_count = 0
    successful_batches = 0
    start_time = datetime.now()

    for batch_num in range(1, repeat_count + 1):
        print(f"\n🔄 バッチ {batch_num}/{repeat_count} 開始")
        print(f"開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 40)

        try:
            # 単一バッチを実行
            updated_count = evaluator.update_records_with_random_games(
                games_per_record, max_records, 8
            )
            total_updated_count += updated_count
            successful_batches += 1

            print(f"✅ バッチ {batch_num} 完了 - 更新レコード数: {updated_count}")

        except Exception as e:
            print(f"❌ バッチ {batch_num} エラー: {e}")
            print("次のバッチに進みます...")

        # 最後のバッチでない場合はインターバル
        if batch_num < repeat_count:
            print(f"\n⏰ {interval_minutes}分間のインターバル中...")
            print(
                f"次のバッチ開始予定時刻: {(datetime.now() + timedelta(minutes=interval_minutes)).strftime('%Y-%m-%d %H:%M:%S')}"
            )

            # インターバル中に進捗を表示
            for remaining_minutes in range(interval_minutes, 0, -1):
                print(f"残り時間: {remaining_minutes}分", end="\r")
                time.sleep(60)  # 1分待機
            print("インターバル終了" + " " * 20)  # 進捗表示をクリア

    # 最終結果を表示
    end_time = datetime.now()
    total_duration = end_time - start_time

    print("\n" + "=" * 50)
    print("📊 バッチ処理完了")
    print(f"成功したバッチ数: {successful_batches}/{repeat_count}")
    print(f"総更新レコード数: {total_updated_count}")
    print(f"総実行時間: {total_duration}")
    print(
        f"平均バッチ時間: {total_duration / repeat_count if repeat_count > 0 else timedelta(0)}"
    )

    return successful_batches == repeat_count


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
    parser.add_argument(
        "--repeat-count",
        type=int,
        default=1,
        help="バッチの繰り返し回数 (デフォルト: 1)",
    )
    parser.add_argument(
        "--interval-minutes",
        type=int,
        default=2,
        help="バッチ間のインターバル時間（分） (デフォルト: 2)",
    )

    args = parser.parse_args()

    # 環境チェックとevaluatorの初期化を一度だけ実行
    print("rustshogi Evaluator バッチ試行処理")
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
        sys.exit(1)

    # バッチ処理を実行
    success = run_trials_batch(
        evaluator,
        args.games_per_record,
        args.max_records,
        args.repeat_count,
        args.interval_minutes,
    )

    if success:
        print("\n🎉 バッチ試行処理が完了しました！")
        print("📁 PostgreSQLデータベースの勝利数が更新されました。")
    else:
        print("\n❌ バッチ試行処理が失敗しました。")
        sys.exit(1)


if __name__ == "__main__":
    main()
