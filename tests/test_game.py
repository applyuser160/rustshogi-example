from rustshogi import Game


class TestGame:
    def test_game_random_move(self):
        # Act
        game = Game()
        game.input_board("startpos")
        num = 10
        threads = 2
        result = game.random_move(num, threads)
        assert result.count == num
