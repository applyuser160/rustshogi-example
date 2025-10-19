#!/usr/bin/env python3
"""
rustshogi Evaluator Python使用例

このスクリプトは、rustshogiのEvaluatorクラスを使用して
評価関数の学習データ作成、モデル訓練、推論実行を行う例です。
"""

from rustshogi import Evaluator, Board


def main():
    print("rustshogi Evaluator Python使用例")
    print("=" * 50)

    # 1. Evaluatorインスタンスを作成
    print("1. Evaluatorインスタンスを作成中...")
    evaluator = Evaluator("training_data.db")

    # 2. データベースを初期化
    print("2. データベースを初期化中...")
    evaluator.init_database()

    # 3. ランダム盤面を生成・保存（少数でテスト）
    print("3. ランダム盤面を生成・保存中...")
    saved_count = evaluator.generate_and_save_random_boards(10)
    print(f"   保存された盤面数: {saved_count}")

    # 4. ランダム対局を実行して勝利数を更新
    print("4. ランダム対局を実行中...")
    updated_count = evaluator.update_records_with_random_games(5, max_records=5)
    print(f"   更新されたレコード数: {updated_count}")

    # 5. データベース統計を取得
    print("5. データベース統計を取得中...")
    stats = evaluator.get_database_stats()
    print(f"   総レコード数: {stats[0]}")
    print(f"   総ゲーム数: {stats[1]}")
    print(f"   平均ゲーム数: {stats[2]}")

    # 6. モデルを訓練
    print("6. モデルを訓練中...")
    try:
        evaluator.train_model(
            min_games=1,
            learning_rate=0.001,
            batch_size=2,
            num_epochs=1,  # テスト用に少なめ
            model_save_path="test_model.bin",
        )
        print("   モデル訓練が完了しました")
    except Exception as e:
        print(f"   モデル訓練エラー: {e}")

    # 7. 任意の盤面で評価関数を実行
    print("7. 評価関数を実行中...")
    try:
        board = Board()
        white_win_rate, black_win_rate, total_games = evaluator.evaluate_position(
            board, "test_model.bin"
        )
        print(f"   白の勝率予測: {white_win_rate:.3f}")
        print(f"   黒の勝率予測: {black_win_rate:.3f}")
        print(f"   総ゲーム数予測: {total_games:.1f}")
    except Exception as e:
        print(f"   評価関数実行エラー: {e}")

    print("\n使用例が完了しました！")


if __name__ == "__main__":
    main()
