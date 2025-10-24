import nox
import os
import glob


@nox.session(
    venv_backend="uv",
    python=["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"],
    tags=["all-tests"],
)
def tests(session):
    session.run("uv", "sync", "--dev")
    session.run("uv", "pip", "install", "pytest", "pytest-benchmark")

    rustshogi_dir = os.path.abspath("../rustshogi")
    with session.chdir(rustshogi_dir):
        python_executable = os.path.join(session.bin, "python.exe")
        session.run(
            "uvx", "maturin", "build", "--release", "--locked", "-i", python_executable
        )

    python_version = session.python.replace(".", "")
    wheel_pattern = f"../rustshogi/target/wheels/rustshogi-*-cp{python_version}-cp{python_version}-*.whl"
    wheel_files = glob.glob(wheel_pattern)
    if wheel_files:
        latest_wheel = max(wheel_files, key=lambda x: os.path.getctime(x))
        session.run("uv", "pip", "install", latest_wheel)
    else:
        session.error(f"No wheel files found for Python {session.python}")

    session.env["PYTHONPATH"] = "."
    args = session.posargs or ["tests"]
    session.run("python", "-m", "pytest", *args)


@nox.session(
    venv_backend="uv",
    python=["3.12"],
    tags=["evaluator"],
)
def evaluator(session):
    session.run("uv", "sync", "--dev")
    rustshogi_dir = os.path.abspath("../rustshogi")
    with session.chdir(rustshogi_dir):
        python_executable = os.path.join(session.bin, "python.exe")
        session.run(
            "uvx", "maturin", "build", "--release", "--locked", "-i", python_executable
        )

    python_version = session.python.replace(".", "")
    wheel_pattern = f"../rustshogi/target/wheels/rustshogi-*-cp{python_version}-cp{python_version}-*.whl"
    wheel_files = glob.glob(wheel_pattern)
    if wheel_files:
        latest_wheel = max(wheel_files, key=lambda x: os.path.getctime(x))
        session.run("uv", "pip", "install", latest_wheel)
    else:
        session.error(f"No wheel files found for Python {session.python}")

    session.env["PYTHONPATH"] = "."
    # session.run("python", "src/evaluator.py")
    session.run("python", "src/evaluator_postgres_env.py")


@nox.session(
    venv_backend="uv",
    python=["3.12"],
    tags=["generate_boards"],
)
def generate_boards(session):
    """ランダム盤面を生成・PostgreSQLに保存"""
    session.run("uv", "sync", "--dev")
    rustshogi_dir = os.path.abspath("../rustshogi")
    with session.chdir(rustshogi_dir):
        python_executable = os.path.join(session.bin, "python.exe")
        session.run(
            "uvx", "maturin", "build", "--release", "--locked", "-i", python_executable
        )

    python_version = session.python.replace(".", "")
    wheel_pattern = f"../rustshogi/target/wheels/rustshogi-*-cp{python_version}-cp{python_version}-*.whl"
    wheel_files = glob.glob(wheel_pattern)
    if wheel_files:
        latest_wheel = max(wheel_files, key=lambda x: os.path.getctime(x))
        session.run("uv", "pip", "install", latest_wheel)
    else:
        session.error(f"No wheel files found for Python {session.python}")

    session.env["PYTHONPATH"] = "."
    args = session.posargs or ["--count", "200"]
    session.run("python", "src/generate_boards.py", *args)


@nox.session(
    venv_backend="uv",
    python=["3.13"],
    tags=["run_trials"],
)
def run_trials(session):
    """ランダム対局を実行して勝利数を更新"""
    session.run("uv", "sync", "--dev")
    rustshogi_dir = os.path.abspath("../rustshogi")
    with session.chdir(rustshogi_dir):
        python_executable = os.path.join(session.bin, "python.exe")
        session.run(
            "uvx", "maturin", "build", "--release", "--locked", "-i", python_executable
        )

    python_version = session.python.replace(".", "")
    wheel_pattern = f"../rustshogi/target/wheels/rustshogi-*-cp{python_version}-cp{python_version}-*.whl"
    wheel_files = glob.glob(wheel_pattern)
    if wheel_files:
        latest_wheel = max(wheel_files, key=lambda x: os.path.getctime(x))
        session.run("uv", "pip", "install", latest_wheel)
    else:
        session.error(f"No wheel files found for Python {session.python}")

    session.env["PYTHONPATH"] = "."
    args = session.posargs or ["--games-per-record", "100", "--max-records", "50"]
    session.run("python", "src/run_trials.py", *args)


@nox.session(
    venv_backend="uv",
    python=["3.12"],
    tags=["train_model"],
)
def train_model(session):
    """モデルを訓練"""
    session.run("uv", "sync", "--dev")
    rustshogi_dir = os.path.abspath("../rustshogi")
    with session.chdir(rustshogi_dir):
        python_executable = os.path.join(session.bin, "python.exe")
        session.run(
            "uvx", "maturin", "build", "--release", "--locked", "-i", python_executable
        )

    python_version = session.python.replace(".", "")
    wheel_pattern = f"../rustshogi/target/wheels/rustshogi-*-cp{python_version}-cp{python_version}-*.whl"
    wheel_files = glob.glob(wheel_pattern)
    if wheel_files:
        latest_wheel = max(wheel_files, key=lambda x: os.path.getctime(x))
        session.run("uv", "pip", "install", latest_wheel)
    else:
        session.error(f"No wheel files found for Python {session.python}")

    session.env["PYTHONPATH"] = "."
    args = session.posargs or [
        "--min-games",
        "20",
        "--num-epochs",
        "10",
        "--model-save-path",
        "model.bin",
        "--max-samples",
        "5000",
    ]
    session.run("python", "src/train_model.py", *args)


@nox.session(
    venv_backend="uv",
    python=["3.12"],
    tags=["evaluate_position"],
)
def evaluate_position(session):
    """評価関数を実行"""
    session.run("uv", "sync", "--dev")
    rustshogi_dir = os.path.abspath("../rustshogi")
    with session.chdir(rustshogi_dir):
        python_executable = os.path.join(session.bin, "python.exe")
        session.run(
            "uvx", "maturin", "build", "--release", "--locked", "-i", python_executable
        )

    python_version = session.python.replace(".", "")
    wheel_pattern = f"../rustshogi/target/wheels/rustshogi-*-cp{python_version}-cp{python_version}-*.whl"
    wheel_files = glob.glob(wheel_pattern)
    if wheel_files:
        latest_wheel = max(wheel_files, key=lambda x: os.path.getctime(x))
        session.run("uv", "pip", "install", latest_wheel)
    else:
        session.error(f"No wheel files found for Python {session.python}")

    session.env["PYTHONPATH"] = "."
    args = session.posargs or ["--model-path", "model.bin"]
    session.run("python", "src/evaluate_position.py", *args)
