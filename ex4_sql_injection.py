"""
Exercicio 4 - Query parametrizada (defesa contra SQL Injection)

ATENCAO: 'busca_insegura' concatena a entrada diretamente na query de proposito,
apenas para demonstrar a vulnerabilidade. Rode SOMENTE no banco local de
laboratorio, nunca em producao.
"""
import os
import mysql.connector

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "cp01_security"),
}

USUARIOS = [
    ("admin", "admin@x.com"),
    ("ana", "ana@x.com"),
    ("bruno", "bruno@x.com"),
]


def conectar():
    return mysql.connector.connect(**DB_CONFIG)


def criar_tabela(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    cursor.execute(
        """
        CREATE TABLE usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
        """
    )
    cursor.executemany(
        "INSERT INTO usuarios (nome, email) VALUES (%s, %s)", USUARIOS
    )
    conn.commit()
    cursor.close()


def busca_insegura(conn, nome):
    """VULNERAVEL: concatena a entrada diretamente na query."""
    cursor = conn.cursor()
    query = f"SELECT id, nome, email FROM usuarios WHERE nome = '{nome}'"
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado


def busca_segura(conn, nome):
    """SEGURO: query parametrizada, a entrada nunca vira parte do SQL."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, email FROM usuarios WHERE nome = %s", (nome,)
    )
    resultado = cursor.fetchall()
    cursor.close()
    return resultado


def main():
    conn = conectar()
    try:
        criar_tabela(conn)

        entrada = "' OR '1'='1"

        inseguro = busca_insegura(conn, entrada)
        print(f"[INSEGURO] entrada={entrada}  -> {len(inseguro)} usuarios (VAZAMENTO)")

        seguro = busca_segura(conn, entrada)
        print(f"[SEGURO]   entrada={entrada}  -> {len(seguro)} usuarios (defesa OK)")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
