# PostgreSQL設定例
# このファイルを参考にPostgreSQLデータベースを設定してください

# 1. PostgreSQLのインストール
# Windows: https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql postgresql-contrib

# 2. PostgreSQLサーバーの起動
# Windows: サービスからPostgreSQLを起動
# macOS: brew services start postgresql
# Ubuntu: sudo systemctl start postgresql

# 3. データベースとユーザーの作成
# psql -U postgres
# CREATE DATABASE rustshogi_db;
# CREATE USER rustshogi_user WITH PASSWORD 'your_password';
# GRANT ALL PRIVILEGES ON DATABASE rustshogi_db TO rustshogi_user;
# \q

# 4. 接続文字列の例
# postgresql://username:password@localhost:5432/database_name
# postgresql://rustshogi_user:your_password@localhost:5432/rustshogi_db

# 5. 環境変数での設定（推奨）
# export POSTGRES_CONNECTION_STRING="postgresql://rustshogi_user:your_password@localhost:5432/rustshogi_db"

# 6. Pythonでの使用例
# import os
# connection_string = os.getenv('POSTGRES_CONNECTION_STRING', 'postgresql://rustshogi_user:your_password@localhost:5432/rustshogi_db')
# evaluator = Evaluator("postgres", connection_string)
