"""
Exercicio 3 - Agregacao: Top IPs
Retorna os 3 IPs com mais eventos do tipo FAIL, ordenados de forma decrescente.
"""
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "cp01_security")

EVENTOS = [
    {"tipo": "FAIL", "ip": "185.220.101.1"}, {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK", "ip": "192.168.1.10"}, {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "185.220.101.1"}, {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "45.33.32.156"}, {"tipo": "FAIL", "ip": "185.220.101.1"},
]


def main():
    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_DATABASE]
        col = db.eventos

        col.delete_many({})
        col.insert_many(EVENTOS)

        pipeline = [
            {"$match": {"tipo": "FAIL"}},
            {"$group": {"_id": "$ip", "total": {"$sum": 1}}},
            {"$sort": {"total": -1}},
            {"$limit": 3},
        ]

        for doc in col.aggregate(pipeline):
            print(f"{doc['_id']} -> {doc['total']}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
