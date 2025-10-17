from rustshogi import Game


class TestGame:
    def test_game_random_move(self):
        # Act
        game = Game()
        game.input_board("startpos")
        num = 10
        threads = 2
        results = game.random_move(num, threads)

        # 結果が空でないことを確認
        assert len(results) > 0

        # 各結果の総ゲーム数がnumと一致することを確認
        for result in results:
            assert result.total_games == num
            # 白と黒の勝利数の合計が総ゲーム数以下であることを確認
            assert result.white_wins + result.black_wins <= result.total_games

        # 結果の数が可能な手の数と一致することを確認
        possible_moves = game.board.search_moves(game.turn)
        assert len(results) == len(possible_moves)
