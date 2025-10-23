#!/usr/bin/env python3
"""
rustshogi Evaluator 推論処理

訓練されたモデルを使用して任意の盤面で評価関数を実行する処理
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evaluator_utils import create_evaluator, check_environment, print_connection_info
from rustshogi import Board


def evaluate_position(model_path="model.bin", board_sfen=None):
    """任意の盤面で評価関数を実行"""
    print("rustshogi Evaluator 推論処理")
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

    # 盤面を準備
    print("4. 評価対象の盤面を準備中...")
    if board_sfen:
        try:
            board = Board.from_sfen(board_sfen)
            print(f"   📋 指定されたSFEN: {board_sfen}")
        except Exception as e:
            print(f"   ❌ SFEN解析エラー: {e}")
            return False
    else:
        board = Board()
        print("   📋 初期局面を使用")

    print(f"   📋 盤面SFEN: {board}")

    # モデルファイルの存在確認
    if not os.path.exists(model_path):
        print(f"   ❌ モデルファイルが見つかりません: {model_path}")
        print("   💡 先に学習処理を実行してください。")
        return False

    # 評価関数を実行
    print("5. 評価関数を実行中...")
    print(f"   モデルパス: {model_path}")

    try:
        white_win_rate, black_win_rate, total_games = evaluator.evaluate_position(
            board, model_path
        )
        print(f"   🎯 白の勝率予測: {white_win_rate:.3f}")
        print(f"   🎯 黒の勝率予測: {black_win_rate:.3f}")
        print(f"   🎯 総ゲーム数予測: {total_games:.1f}")
        return True
    except Exception as e:
        print(f"   ❌ 評価関数実行エラー: {e}")
        return False


def main():
    """メイン処理"""
    import argparse

    parser = argparse.ArgumentParser(description="評価関数を実行")
    parser.add_argument(
        "--model-path",
        default="model.bin",
        help="モデルファイルパス (デフォルト: model.bin)",
    )
    parser.add_argument(
        "--board-sfen", help="評価する盤面のSFEN (指定しない場合は初期局面)"
    )

    args = parser.parse_args()

    success = evaluate_position(args.model_path, args.board_sfen)

    if success:
        print("\n🎉 推論処理が完了しました！")
        print("🎯 盤面の評価が完了しました。")
    else:
        print("\n❌ 推論処理が失敗しました。")
        sys.exit(1)


if __name__ == "__main__":
    main()
