from rustshogi import (
    Board,
    ColorType,
    EvaluationResult,
    SearchEngine,
    SimpleEvaluator,
)


class TestSearch:
    def test_search_engine_default(self):
        """SearchEngineのデフォルト設定での動作テスト"""
        # Arrange
        engine = SearchEngine()
        board = Board("startpos")

        # Act
        result = engine.search(board, ColorType.Black, depth=1)

        # Assert
        assert isinstance(result, EvaluationResult)
        assert hasattr(result, "score")
        assert hasattr(result, "best_move")
        assert hasattr(result, "nodes_searched")
        assert result.nodes_searched > 0

    def test_search_engine_minmax(self):
        """MinMax探索アルゴリズムのテスト"""
        # Arrange
        engine = SearchEngine(algorithm="minmax", max_nodes=10000)
        board = Board("startpos")

        # Act
        result = engine.search(board, ColorType.Black, depth=1)

        # Assert
        assert isinstance(result, EvaluationResult)
        assert result.nodes_searched <= 10000

    def test_search_engine_alphabeta(self):
        """AlphaBeta探索アルゴリズムのテスト"""
        # Arrange
        engine = SearchEngine(algorithm="alphabeta", max_nodes=10000)
        board = Board("startpos")

        # Act
        result = engine.search(board, ColorType.Black, depth=1)

        # Assert
        assert isinstance(result, EvaluationResult)
        assert result.nodes_searched <= 10000

    def test_search_engine_with_simple_evaluator(self):
        """SimpleEvaluatorを使ったテスト"""
        # Arrange
        evaluator = SimpleEvaluator()
        engine = SearchEngine(algorithm="minmax", max_nodes=10000, evaluator=evaluator)
        board = Board("startpos")

        # Act
        result = engine.search(board, ColorType.Black, depth=1)

        # Assert
        assert isinstance(result, EvaluationResult)
        assert isinstance(result.score, float)

    def test_search_engine_different_depths(self):
        """異なる深度での探索テスト"""
        # Arrange
        engine = SearchEngine(algorithm="alphabeta", max_nodes=50000)

        # Act
        result_depth_1 = engine.search(Board("startpos"), ColorType.Black, depth=1)
        result_depth_2 = engine.search(Board("startpos"), ColorType.Black, depth=2)
        result_depth_3 = engine.search(Board("startpos"), ColorType.Black, depth=3)

        # Assert
        assert isinstance(result_depth_1, EvaluationResult)
        assert isinstance(result_depth_2, EvaluationResult)
        assert isinstance(result_depth_3, EvaluationResult)
        assert result_depth_3.nodes_searched >= result_depth_2.nodes_searched
        assert result_depth_2.nodes_searched >= result_depth_1.nodes_searched

    def test_search_engine_different_colors(self):
        """異なる色での探索テスト"""
        # Arrange
        engine = SearchEngine(algorithm="minmax", max_nodes=10000)
        board = Board("startpos")

        # Act
        result_black = engine.search(board, ColorType.Black, depth=1)
        result_white = engine.search(board, ColorType.White, depth=1)

        # Assert
        assert isinstance(result_black, EvaluationResult)
        assert isinstance(result_white, EvaluationResult)
        assert hasattr(result_black, "score")
        assert hasattr(result_white, "score")

    def test_search_engine_custom_board(self):
        """カスタム盤面での探索テスト"""
        # Arrange
        engine = SearchEngine(algorithm="alphabeta", max_nodes=50000)
        board = Board("lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL -")

        # Act
        result = engine.search(board, ColorType.Black, depth=2)

        # Assert
        assert isinstance(result, EvaluationResult)
        assert result.nodes_searched > 0

    def test_search_engine_best_move(self):
        """最善手が取得できるかテスト"""
        # Arrange
        engine = SearchEngine(algorithm="minmax", max_nodes=100000)
        board = Board("startpos")

        # Act
        result = engine.search(board, ColorType.Black, depth=2)

        # Assert
        assert isinstance(result, EvaluationResult)
        # 最善手はNoneの場合もあるが、探索が成功することを確認
        if result.best_move is not None:
            # Moveオブジェクトにはget_from()とget_to()メソッドがあることを確認
            from_addr = result.best_move.get_from()
            to_addr = result.best_move.get_to()
            assert from_addr is not None
            assert to_addr is not None

    def test_search_engine_max_nodes_limit(self):
        """max_nodes制限のテスト"""
        # Arrange
        engine = SearchEngine(algorithm="alphabeta", max_nodes=1000)
        board = Board("startpos")

        # Act
        result = engine.search(board, ColorType.Black, depth=2)

        # Assert
        assert isinstance(result, EvaluationResult)
        assert result.nodes_searched <= 1000

    def test_search_engine_complex_position(self):
        """複雑な局面での探索テスト"""
        # Arrange - より戦術的に興味深い局面
        sfen = "lnsgkgsnl/1r7/ppppppppp/9/9/9/PPPPPPPPP/B8/LNSGKGSNL w - 1"
        board = Board(sfen)
        engine = SearchEngine(algorithm="minmax", max_nodes=50000)

        # Act
        result = engine.search(board, ColorType.Black, depth=2)

        # Assert
        assert isinstance(result, EvaluationResult)
        assert result.nodes_searched > 0
        assert isinstance(result.score, float)
