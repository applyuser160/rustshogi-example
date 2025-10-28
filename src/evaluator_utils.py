#!/usr/bin/env python3
"""
rustshogi Evaluator ユーティリティ関数

各処理（盤面生成、試行、学習、推論）で共通して使用する関数を定義
"""

import os
from rustshogi import NeuralEvaluator


def get_postgres_connection_string():
    """環境変数からPostgreSQL接続文字列を取得"""
    # 環境変数から接続文字列を取得
    connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

    if connection_string:
        return connection_string

    # 個別の環境変数から構築
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "postgres")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "root")

    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def create_evaluator():
    """PostgreSQL Evaluatorインスタンスを作成"""
    connection_string = get_postgres_connection_string()
    return NeuralEvaluator("postgres", connection_string)


def check_environment():
    """環境変数の設定状況をチェック"""
    print("🔍 環境変数の設定状況:")

    env_vars = [
        "POSTGRES_CONNECTION_STRING",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
    ]

    for var in env_vars:
        value = os.getenv(var)
        if value:
            if "PASSWORD" in var:
                print(f"   ✅ {var}: ***")
            else:
                print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: 未設定")


def print_connection_info():
    """接続情報を表示"""
    connection_string = get_postgres_connection_string()
    print("1. PostgreSQL接続設定:")
    print(f"   接続文字列: {connection_string}")

    # 接続文字列のマスク（パスワードを隠す）
    masked_connection = connection_string.split("@")[0].split(":")
    if len(masked_connection) >= 2:
        masked_connection[1] = "***"
        masked_string = (
            ":".join(masked_connection) + "@" + connection_string.split("@")[1]
        )
        print(f"   マスク済み: {masked_string}")
