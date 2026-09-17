"""
Exercicio 6 - Indice e desempenho (MongoDB)

Comentario: sem indice a busca por IP seria O(n) (o MongoDB varre todos os
documentos da colecao, um "collection scan"). Com um indice em 'ip', a busca
passa a usar uma B-tree e o custo cai para ~O(log n), o que faz diferenca
real quando a colecao cresce de milhares para milhoes de eventos.
"""
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "cp01_security")

IPS = ["185.220.101.1", "10.0.0.5", "172.16.0.9", "8.8.8.8"]


def gerar_eventos(qtd=1000):
    eventos = []
    for i in range(qtd):
        eventos.append({"seq": i, "ip": IPS[i % len(IPS)], "tipo": "FAIL"})
    return eventos


def main():
    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_DATABASE]
        col = db.eventos_performance

        col.delete_many({})
        eventos = gerar_eventos(1000)
        col.insert_many(eventos)
        print(f"{len(eventos)} eventos inseridos.")

        col.create_index("ip")
        print("Indice criado em 'ip'.")

        alvo = "185.220.101.1"
        total = col.count_documents({"ip": alvo})
        print(f"Eventos do IP {alvo}: {total}")

        print("Comentario: sem indice a busca seria O(n) (varre tudo); "
              "com indice ~O(log n).")
    finally:
        client.close()


if __name__ == "__main__":
    main()
