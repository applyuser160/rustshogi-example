#!/usr/bin/env python3
"""
rustshogi Evaluator Python使用例（PostgreSQL版 + 環境変数対応）

このスクリプトは、rustshogiのEvaluatorクラスを使用して
PostgreSQLデータベースで評価関数の学習データ作成、モデル訓練、推論実行を行う例です。
環境変数から接続設定を読み取ります。
"""

import os
from rustshogi import Evaluator, Board


def get_postgres_connection_string():
    """環境変数からPostgreSQL接続文字列を取得"""
    # 環境変数から接続文字列を取得
    connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

    if connection_string:
        return connection_string

    # 個別の環境変数から構築
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "postgres")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "root")

    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def main():
    print("rustshogi Evaluator Python使用例（PostgreSQL版 + 環境変数対応）")
    print("=" * 70)

    # 環境変数からPostgreSQL接続設定を取得
    connection_string = get_postgres_connection_string()

    print("1. PostgreSQL接続設定:")
    print(f"   接続文字列: {connection_string}")

    # 接続文字列のマスク（パスワードを隠す）
    masked_connection = connection_string.split("@")[0].split(":")
    if len(masked_connection) >= 2:
        masked_connection[1] = "***"
        masked_string = (
            ":".join(masked_connection) + "@" + connection_string.split("@")[1]
        )
        print(f"   マスク済み: {masked_string}")

    # 1. PostgreSQL Evaluatorインスタンスを作成
    print("\n2. PostgreSQL Evaluatorインスタンスを作成中...")
    evaluator = Evaluator("postgres", connection_string)

    # 2. PostgreSQLデータベースを初期化
    print("3. PostgreSQLデータベースを初期化中...")
    try:
        evaluator.init_database()
        print("   ✅ PostgreSQLデータベースの初期化が完了しました")
    except Exception as e:
        print(f"   ❌ データベース初期化エラー: {e}")
        print("   💡 PostgreSQLサーバーが起動していることを確認してください")
        print("   💡 接続文字列が正しいことを確認してください")
        return

    # 3. ランダム盤面を生成・保存（PostgreSQLに保存）
    print("4. ランダム盤面を生成・PostgreSQLに保存中...")
    try:
        saved_count = evaluator.generate_and_save_random_boards(200)  # より多くのデータ
        print(f"   ✅ 保存された盤面数: {saved_count}")
    except Exception as e:
        print(f"   ❌ 盤面保存エラー: {e}")
        return

    # 4. ランダム対局を実行して勝利数を更新
    print("5. ランダム対局を実行中...")
    try:
        updated_count = evaluator.update_records_with_random_games(100, 50, 8)
        print(f"   ✅ 更新されたレコード数: {updated_count}")
    except Exception as e:
        print(f"   ❌ 対局実行エラー: {e}")
        return

    # 5. PostgreSQLデータベース統計を取得
    print("6. PostgreSQLデータベース統計を取得中...")
    try:
        stats = evaluator.get_database_stats()
        print(f"   📊 総レコード数: {stats[0]}")
        print(f"   📊 総ゲーム数: {stats[1]}")
        print(f"   📊 平均ゲーム数: {stats[2]}")
    except Exception as e:
        print(f"   ❌ 統計取得エラー: {e}")
        return

    # 6. モデルを訓練
    print("7. モデルを訓練中...")
    try:
        evaluator.train_model(
            min_games=20,  # より多くのデータを使用
            learning_rate=0.001,
            batch_size=32,
            num_epochs=10,  # より多くのエポック
            model_save_path="test_model_postgres_env.bin",
        )
        print("   ✅ モデル訓練が完了しました")
    except Exception as e:
        print(f"   ❌ モデル訓練エラー: {e}")
        return

    # 7. 任意の盤面で評価関数を実行
    print("8. 評価関数を実行中...")
    try:
        board = Board()
        white_win_rate, black_win_rate, total_games = evaluator.evaluate_position(
            board, "test_model_postgres_env.bin"
        )
        print(f"   🎯 白の勝率予測: {white_win_rate:.3f}")
        print(f"   🎯 黒の勝率予測: {black_win_rate:.3f}")
        print(f"   🎯 総ゲーム数予測: {total_games:.1f}")
    except Exception as e:
        print(f"   ❌ 評価関数実行エラー: {e}")
        return

    print("\n🎉 PostgreSQL使用例が完了しました！")
    print("📁 PostgreSQLデータベースに学習データが保存されました。")
    print("🤖 訓練されたモデル: test_model_postgres_env.bin")


def check_environment():
    """環境変数の設定状況をチェック"""
    print("🔍 環境変数の設定状況:")

    env_vars = [
        "POSTGRES_CONNECTION_STRING",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    ]

    for var in env_vars:
        value = os.getenv(var)
        if value:
            if "PASSWORD" in var:
                print(f"   ✅ {var}: ***")
            else:
                print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: 未設定")


if __name__ == "__main__":
    check_environment()
    print()
    main()
