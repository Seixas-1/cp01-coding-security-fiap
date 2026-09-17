"""
Exercicio 10 (Desafio) - Mini-pipeline SIEM: log -> MongoDB -> ML

1. Le o auth.log e normaliza cada linha em um documento.
2. Insere todos no MongoDB.
3. Para cada IP, calcula via agregacao a contagem de FAILs.
4. Monta um dataset [qtd_fails] e rotula IP como suspeito (1) se >= 5 falhas, senao 0.
5. Treina um classificador e preve o rotulo de um IP novo com 8 falhas.
"""
import os
import re

from pymongo import MongoClient
from sklearn.tree import DecisionTreeClassifier

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "cp01_security")
LOG_PATH = os.path.join(os.path.dirname(__file__), "data", "auth.log")

LINHA_RE = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<tipo>\S+)\s+usuario=(?P<usuario>\S+)\s+ip=(?P<ip>\S+)$"
)

LIMIAR_SUSPEITO = 5


def ler_auth_log(caminho):
    eventos = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            match = LINHA_RE.match(linha)
            if not match:
                continue
            eventos.append(match.groupdict())
    return eventos


def main():
    eventos = ler_auth_log(LOG_PATH)

    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_DATABASE]
        col = db.auth_log

        col.delete_many({})
        col.insert_many(eventos)
        print(f"Eventos inseridos no MongoDB: {len(eventos)}")

        pipeline = [
            {"$match": {"tipo": "FAIL"}},
            {"$group": {"_id": "$ip", "fails": {"$sum": 1}}},
            {"$sort": {"fails": -1}},
        ]
        contagem_por_ip = list(col.aggregate(pipeline))

        X = [[doc["fails"]] for doc in contagem_por_ip]
        y = [1 if doc["fails"] >= LIMIAR_SUSPEITO else 0 for doc in contagem_por_ip]

        print(f"Dataset de treino: {X} rotulos {y}")

        modelo = DecisionTreeClassifier(random_state=42)
        modelo.fit(X, y)

        ip_novo_fails = 8
        predicao = modelo.predict([[ip_novo_fails]])[0]
        rotulo = "Suspeito (1)" if predicao == 1 else "Normal (0)"
        print(f"Previsao para IP com {ip_novo_fails} falhas -> {rotulo}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
