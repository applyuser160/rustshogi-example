from datetime import timedelta
from datetime import datetime
from rustshogi import Game


class TestBenchmark:
    def test_random_games_benchmark(self, benchmark):
        """10回のランダム対局のベンチマークテスト"""

        def run_random_games():
            """10回のランダム対局を実行する関数"""
            games_completed = 0
            total_moves = 0

            for _ in range(100):
                game = Game()
                # ランダム対局を実行
                result_game = game.random_play()
                games_completed += 1
                total_moves += result_game.move_number

            return games_completed, total_moves

        # ベンチマーク実行
        benchmark.pedantic(run_random_games, rounds=10)

    def test_single_random_game_benchmark(self, benchmark):
        """単一のランダム対局のベンチマークテスト"""

        def run_single_game():
            """単一のランダム対局を実行する関数"""
            game = Game()
            result_game = game.random_play()
            return result_game.move_number

        # ベンチマーク実行
        benchmark.pedantic(run_single_game, rounds=10)

    def test_benchmark(self):
        # Arrange
        start = datetime.now()

        # Act
        for _ in range(100):
            game: Game = Game()
            game.random_play()
        end = datetime.now()

        # Assert
        assert end - start < timedelta(microseconds=33333)
