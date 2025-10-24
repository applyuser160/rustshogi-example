#!/usr/bin/env python3
"""
rustshogi Evaluator 学習処理

PostgreSQLデータベースの学習データを使用してモデルを訓練する処理
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evaluator_utils import create_evaluator, check_environment, print_connection_info


def train_model(
    min_games=20,
    learning_rate=0.001,
    batch_size=128,
    num_epochs=10,
    model_save_path="model.bin",
    max_samples=None,
):
    """モデルを訓練"""
    print("rustshogi Evaluator 学習処理")
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

    # データベース統計を取得
    print("4. PostgreSQLデータベース統計を取得中...")
    try:
        stats = evaluator.get_database_stats()
        print(f"   📊 総レコード数: {stats[0]}")
        print(f"   📊 総ゲーム数: {stats[1]}")
        print(f"   📊 平均ゲーム数: {stats[2]}")

        if stats[0] == 0:
            print(
                "   ❌ 学習データが存在しません。先に盤面生成処理を実行してください。"
            )
            return False

    except Exception as e:
        print(f"   ❌ 統計取得エラー: {e}")
        return False

    # モデルを訓練
    print("5. モデルを訓練中...")
    print(f"   最小ゲーム数: {min_games}")
    print(f"   学習率: {learning_rate}")
    print(f"   バッチサイズ: {batch_size}")
    print(f"   エポック数: {num_epochs}")
    print(f"   モデル保存パス: {model_save_path}")
    print(f"   最大サンプル数: {max_samples if max_samples else '全データ'}")

    try:
        if max_samples is not None:
            evaluator.train_model_with_sampling(
                min_games=min_games,
                learning_rate=learning_rate,
                batch_size=batch_size,
                num_epochs=num_epochs,
                model_save_path=model_save_path,
                max_samples=max_samples,
            )
        else:
            evaluator.train_model(
                min_games=min_games,
                learning_rate=learning_rate,
                batch_size=batch_size,
                num_epochs=num_epochs,
                model_save_path=model_save_path,
            )
        print("   ✅ モデル訓練が完了しました")
        return True
    except Exception as e:
        print(f"   ❌ モデル訓練エラー: {e}")
        return False


def main():
    """メイン処理"""
    import argparse

    parser = argparse.ArgumentParser(description="モデルを訓練")
    parser.add_argument(
        "--min-games", type=int, default=20, help="最小ゲーム数 (デフォルト: 20)"
    )
    parser.add_argument(
        "--learning-rate", type=float, default=0.001, help="学習率 (デフォルト: 0.001)"
    )
    parser.add_argument(
        "--batch-size", type=int, default=128, help="バッチサイズ (デフォルト: 128)"
    )
    parser.add_argument(
        "--num-epochs", type=int, default=10, help="エポック数 (デフォルト: 10)"
    )
    parser.add_argument(
        "--model-save-path",
        default="model.bin",
        help="モデル保存パス (デフォルト: model.bin)",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="最大サンプル数 (デフォルト: 全データ)",
    )

    args = parser.parse_args()

    success = train_model(
        min_games=args.min_games,
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
        num_epochs=args.num_epochs,
        model_save_path=args.model_save_path,
        max_samples=args.max_samples,
    )

    if success:
        print("\n🎉 学習処理が完了しました！")
        print(f"🤖 訓練されたモデル: {args.model_save_path}")
    else:
        print("\n❌ 学習処理が失敗しました。")
        sys.exit(1)


if __name__ == "__main__":
    main()
