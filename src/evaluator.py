#!/usr/bin/env python3
"""
rustshogi Evaluator Python使用例（PostgreSQL版）

このスクリプトは、rustshogiのEvaluatorクラスを使用して
PostgreSQLデータベースで評価関数の学習データ作成、モデル訓練、推論実行を行う例です。
"""

from rustshogi import Evaluator, Board


def main():
    print("rustshogi Evaluator Python使用例（PostgreSQL版）")
    print("=" * 60)

    # PostgreSQL接続設定
    # 実際の環境に合わせて接続文字列を変更してください
    connection_string = "postgresql://postgres:root@localhost:5433/postgres"

    # 1. PostgreSQL Evaluatorインスタンスを作成
    print("1. PostgreSQL Evaluatorインスタンスを作成中...")
    print(f"   接続文字列: {connection_string}")
    evaluator = Evaluator("postgres", connection_string)

    # 2. PostgreSQLデータベースを初期化
    print("2. PostgreSQLデータベースを初期化中...")
    try:
        evaluator.init_database()
        print("   PostgreSQLデータベースの初期化が完了しました")
    except Exception as e:
        print(f"   データベース初期化エラー: {e}")
        print("   PostgreSQLサーバーが起動していることを確認してください")
        return

    # 3. ランダム盤面を生成・保存（PostgreSQLに保存）
    print("3. ランダム盤面を生成・PostgreSQLに保存中...")
    try:
        saved_count = evaluator.generate_and_save_random_boards(
            100
        )  # PostgreSQLなので多めに
        print(f"   保存された盤面数: {saved_count}")
    except Exception as e:
        print(f"   盤面保存エラー: {e}")
        return

    # 4. ランダム対局を実行して勝利数を更新
    print("4. ランダム対局を実行中...")
    try:
        updated_count = evaluator.update_records_with_random_games(50, max_records=20)
        print(f"   更新されたレコード数: {updated_count}")
    except Exception as e:
        print(f"   対局実行エラー: {e}")
        return

    # 5. PostgreSQLデータベース統計を取得
    print("5. PostgreSQLデータベース統計を取得中...")
    try:
        stats = evaluator.get_database_stats()
        print(f"   総レコード数: {stats[0]}")
        print(f"   総ゲーム数: {stats[1]}")
        print(f"   平均ゲーム数: {stats[2]}")
    except Exception as e:
        print(f"   統計取得エラー: {e}")
        return

    # 6. モデルを訓練
    print("6. モデルを訓練中...")
    try:
        evaluator.train_model(
            min_games=10,  # PostgreSQLなのでより多くのデータを使用
            learning_rate=0.001,
            batch_size=16,
            num_epochs=5,  # PostgreSQLなので少し多めに
            model_save_path="test_model_postgres.bin",
        )
        print("   モデル訓練が完了しました")
    except Exception as e:
        print(f"   モデル訓練エラー: {e}")
        return

    # 7. 任意の盤面で評価関数を実行
    print("7. 評価関数を実行中...")
    try:
        board = Board()
        white_win_rate, black_win_rate, total_games = evaluator.evaluate_position(
            board, "test_model_postgres.bin"
        )
        print(f"   白の勝率予測: {white_win_rate:.3f}")
        print(f"   黒の勝率予測: {black_win_rate:.3f}")
        print(f"   総ゲーム数予測: {total_games:.1f}")
    except Exception as e:
        print(f"   評価関数実行エラー: {e}")
        return

    print("\nPostgreSQL使用例が完了しました！")
    print("PostgreSQLデータベースに学習データが保存されました。")


def sqlite_example():
    """SQLiteとの比較用の例"""
    print("\n=== SQLiteとの比較例 ===")

    # SQLite版
    print("SQLite版:")
    sqlite_evaluator = Evaluator("sqlite", "training_data_sqlite.db")
    sqlite_evaluator.init_database()
    sqlite_count = sqlite_evaluator.generate_and_save_random_boards(10)
    print(f"SQLite保存数: {sqlite_count}")

    # PostgreSQL版
    print("PostgreSQL版:")
    postgres_evaluator = Evaluator(
        "postgres", "postgresql://username:password@localhost:5432/rustshogi_db"
    )
    try:
        postgres_evaluator.init_database()
        postgres_count = postgres_evaluator.generate_and_save_random_boards(10)
        print(f"PostgreSQL保存数: {postgres_count}")
    except Exception as e:
        print(f"PostgreSQL接続エラー: {e}")


if __name__ == "__main__":
    main()
    # sqlite_example()  # 比較例を実行したい場合はコメントアウトを外す
