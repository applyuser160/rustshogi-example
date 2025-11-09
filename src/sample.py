from rustshogi import (
    EvaluationResult,
    SearchEngine,
    NeuralEvaluator,
    Board,
    ColorType,
)

evaluator = NeuralEvaluator(
    db_type_str="postgresql",
    connection_string="postgresql://postgres:postgres@localhost:5433/rustshogi",
    model_path="v4_model.mpk",
)

search_engine = SearchEngine(
    algorithm="alphabeta",
    max_nodes=1000000,
    evaluator=evaluator,
)

results: list[EvaluationResult] = search_engine.search(
    board=Board(
        "ln2k2nl/1r2g1g2/1ppsp1spp/p2p1pp2/9/2P1P4/PP1PS1PPP/3GG1R2/LNS1K2NL 2bp"
    ),
    color=ColorType.Black,
    depth=6,
    limit=3,
)

for result in results:
    print(result.score)
    print(result.best_move)
    print(result.nodes_searched)
