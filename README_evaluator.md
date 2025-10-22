# rustshogi Evaluator 使用方法

このディレクトリには、rustshogiのEvaluatorクラスを使用した評価関数の学習・推論システムが含まれています。

## ファイル構成

### 共通ユーティリティ
- `evaluator_utils.py` - 各処理で共通して使用する関数

### 個別処理スクリプト
- `generate_boards.py` - ランダム盤面生成・保存
- `run_trials.py` - ランダム対局実行・勝利数更新
- `train_model.py` - モデル訓練
- `evaluate_position.py` - 評価関数実行

### 統合スクリプト
- `evaluator_postgres_env.py` - 全処理を一括実行（環境変数対応）

## 使用方法

### 1. 環境変数の設定

PostgreSQL接続設定を環境変数で設定：

```bash
# 接続文字列を直接指定
export POSTGRES_CONNECTION_STRING="postgresql://postgres:root@localhost:5433/postgres"

# または個別に設定
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5433"
export POSTGRES_DB="postgres"
export POSTGRES_USER="postgres"
export POSTGRES_PASSWORD="root"
```

### 2. noxを使用した実行

#### 個別処理の実行

```bash
# ランダム盤面生成（デフォルト200個）
nox -s generate_boards

# カスタム盤面数で生成
nox -s generate_boards -- --count 500

# ランダム対局実行（デフォルト: レコードあたり100ゲーム、最大50レコード）
nox -s run_trials

# カスタム設定で対局実行
nox -s run_trials -- --games-per-record 200 --max-records 100

# バッチ繰り返し実行（5回繰り返し、各バッチ間に2分のインターバル）
nox -s run_trials -- --repeat-count 5 --interval-minutes 2

# モデル訓練（デフォルト設定）
nox -s train_model

# カスタム設定でモデル訓練
nox -s train_model -- --min-games 50 --num-epochs 20 --model-save-path "my_model.bin"

# 評価関数実行（デフォルト: model.bin、初期局面）
nox -s evaluate_position

# カスタム設定で評価関数実行
nox -s evaluate_position -- --model-path "my_model.bin" --board-sfen "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL -"
```

#### 全処理を一括実行

```bash
nox -s evaluator
```

### 3. 直接実行

```bash
# 個別スクリプトを直接実行
python src/generate_boards.py --count 300
python src/run_trials.py --games-per-record 150 --max-records 30
python src/run_trials.py --repeat-count 3 --interval-minutes 5 --games-per-record 100
python src/train_model.py --min-games 30 --num-epochs 15
python src/evaluate_position.py --model-path "my_model.bin"
```

## 処理フロー

1. **盤面生成** (`generate_boards.py`)
   - ランダムな盤面を生成
   - PostgreSQLデータベースに保存

2. **試行実行** (`run_trials.py`)
   - 保存された盤面に対してランダム対局を実行
   - 勝利数を更新
   - バッチ繰り返し機能：指定回数だけ処理を繰り返し実行
   - インターバル機能：各バッチ間に指定時間の待機

3. **モデル訓練** (`train_model.py`)
   - 学習データを取得
   - ニューラルネットワークモデルを訓練
   - モデルをファイルに保存

4. **推論実行** (`evaluate_position.py`)
   - 訓練されたモデルを読み込み
   - 任意の盤面で評価関数を実行

## パラメータ説明

### generate_boards.py
- `--count`: 生成する盤面数（デフォルト: 200）

### run_trials.py
- `--games-per-record`: レコードあたりのゲーム数（デフォルト: 100）
- `--max-records`: 最大更新レコード数（指定しない場合は全レコード）
- `--repeat-count`: バッチの繰り返し回数（デフォルト: 1）
- `--interval-minutes`: バッチ間のインターバル時間（分）（デフォルト: 2）

### train_model.py
- `--min-games`: 最小ゲーム数（デフォルト: 20）
- `--learning-rate`: 学習率（デフォルト: 0.001）
- `--batch-size`: バッチサイズ（デフォルト: 32）
- `--num-epochs`: エポック数（デフォルト: 10）
- `--model-save-path`: モデル保存パス（デフォルト: model.bin）

### evaluate_position.py
- `--model-path`: モデルファイルパス（デフォルト: model.bin）
- `--board-sfen`: 評価する盤面のSFEN（指定しない場合は初期局面）

## バッチ繰り返し機能の詳細

`run_trials.py`のバッチ繰り返し機能により、長時間の処理を自動化できます：

### 機能概要
- **繰り返し実行**: 指定した回数だけバッチ処理を繰り返し
- **インターバル**: 各バッチ間に指定時間の待機（システム負荷軽減）
- **進捗表示**: 各バッチの開始・完了時刻、残り時間を表示
- **エラー処理**: 個別バッチでエラーが発生しても次のバッチに進む
- **統計情報**: 成功バッチ数、総更新レコード数、実行時間を表示

### 使用例
```bash
# 10回繰り返し、各バッチ間に3分のインターバル
python src/run_trials.py --repeat-count 10 --interval-minutes 3

# 5回繰り返し、インターバルなし（連続実行）
python src/run_trials.py --repeat-count 5 --interval-minutes 0

# 3回繰り返し、レコードあたり50ゲーム、最大20レコード
python src/run_trials.py --repeat-count 3 --games-per-record 50 --max-records 20
```

## 注意事項

- PostgreSQLサーバーが起動していることを確認してください
- 環境変数で接続設定が正しく設定されていることを確認してください
- 各処理は依存関係があるため、順序を守って実行してください：
  1. 盤面生成 → 2. 試行実行 → 3. モデル訓練 → 4. 推論実行
- バッチ繰り返し実行時は、長時間の処理になる可能性があるため、適切なインターバルを設定してください
