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
