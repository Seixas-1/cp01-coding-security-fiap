"""
Exercicio 5 - Transacao com rollback
Tabela: contas(id, titular, saldo)
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

CONTAS_INICIAIS = [
    (1, "Alice", 1000),
    (2, "Bob", 500),
]


def conectar():
    return mysql.connector.connect(**DB_CONFIG)


def criar_tabela(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS contas")
    cursor.execute(
        """
        CREATE TABLE contas (
            id INT PRIMARY KEY,
            titular VARCHAR(100) NOT NULL,
            saldo DECIMAL(10, 2) NOT NULL
        )
        """
    )
    cursor.executemany(
        "INSERT INTO contas (id, titular, saldo) VALUES (%s, %s, %s)",
        CONTAS_INICIAIS,
    )
    conn.commit()
    cursor.close()


def saldo_de(conn, conta_id):
    cursor = conn.cursor()
    cursor.execute("SELECT saldo FROM contas WHERE id = %s", (conta_id,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def transferir(conn, origem_id, destino_id, valor):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE contas SET saldo = saldo - %s WHERE id = %s",
            (valor, origem_id),
        )
        cursor.execute(
            "UPDATE contas SET saldo = saldo + %s WHERE id = %s",
            (valor, destino_id),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"conta destino {destino_id} inexistente")

        conn.commit()
        return True
    except (mysql.connector.Error, ValueError):
        conn.rollback()
        return False
    finally:
        cursor.close()


def main():
    conn = conectar()
    try:
        criar_tabela(conn)

        if transferir(conn, 1, 2, 200):
            print(f"Transferencia 1 OK. Alice={saldo_de(conn, 1)}, Bob={saldo_de(conn, 2)}")

        if not transferir(conn, 1, 99, 100):
            print(f"Transferencia 2 FALHOU (conta destino inexistente). "
                  f"Rollback. Alice={saldo_de(conn, 1)}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
