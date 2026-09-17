"""
Exercicio 1 - Modelagem e CRUD SQL
Tabela: ativos(id PK AUTO_INCREMENT, nome, ip UNIQUE, tipo,
                criticidade ENUM('baixa','media','alta'), status)
"""
import os
import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "cp01_security"),
}

ATIVOS_INICIAIS = [
    ("SRV-WEB01", "192.168.1.10", "servidor", "alta", "ativo"),
    ("PC-RH03", "192.168.1.45", "estacao", "baixa", "ativo"),
    ("SW-CORE01", "192.168.1.1", "switch", "media", "inativo"),
]


def conectar():
    return mysql.connector.connect(**DB_CONFIG)


def criar_tabela(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS ativos")
    cursor.execute(
        """
        CREATE TABLE ativos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            ip VARCHAR(45) NOT NULL UNIQUE,
            tipo VARCHAR(50) NOT NULL,
            criticidade ENUM('baixa', 'media', 'alta') NOT NULL,
            status VARCHAR(20) NOT NULL
        )
        """
    )
    conn.commit()
    cursor.close()


def inserir_ativo(conn, nome, ip, tipo, criticidade, status):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO ativos (nome, ip, tipo, criticidade, status) "
            "VALUES (%s, %s, %s, %s, %s)",
            (nome, ip, tipo, criticidade, status),
        )
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.IntegrityError as err:
        conn.rollback()
        if err.errno == errorcode.ER_DUP_ENTRY:
            print(f"Erro de UNIQUE tratado: IP '{ip}' ja cadastrado ({err})")
        else:
            raise
        return None
    finally:
        cursor.close()


def listar_por_tipo(conn, tipo):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nome, ip, criticidade, status FROM ativos WHERE tipo = %s",
        (tipo,),
    )
    resultado = cursor.fetchall()
    cursor.close()
    return resultado


def atualizar_status(conn, nome, novo_status):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE ativos SET status = %s WHERE nome = %s",
        (novo_status, nome),
    )
    conn.commit()
    linhas = cursor.rowcount
    cursor.close()
    return linhas


def remover_ativo(conn, nome):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ativos WHERE nome = %s", (nome,))
    conn.commit()
    linhas = cursor.rowcount
    cursor.close()
    return linhas


def main():
    conn = conectar()
    try:
        criar_tabela(conn)

        for ativo in ATIVOS_INICIAIS:
            inserir_ativo(conn, *ativo)

        print("Listar tipo='servidor':")
        for nome, ip, criticidade, status in listar_por_tipo(conn, "servidor"):
            print(f"{nome} | {ip} | {criticidade} | {status}")

        linhas = atualizar_status(conn, "SW-CORE01", "ativo")
        print(f"\nApos UPDATE status de SW-CORE01 para 'ativo' -> "
              f"\"{linhas} registro atualizado\"")

        print("\nInserir IP duplicado (192.168.1.10):")
        inserir_ativo(conn, "SRV-WEB02", "192.168.1.10", "servidor", "media", "ativo")

        removidos = remover_ativo(conn, "PC-RH03")
        print(f"\nRemovido PC-RH03 -> {removidos} registro(s) deletado(s)")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
