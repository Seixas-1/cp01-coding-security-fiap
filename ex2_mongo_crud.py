"""
Exercicio 2 - CRUD com PyMongo
Colecao: vulnerabilidades
"""
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "cp01_security")

VULNS = [
    {"cve_id": "CVE-2024-001", "tipo": "SQL Injection", "severidade": "Alta", "corrigida": False},
    {"cve_id": "CVE-2024-002", "tipo": "XSS", "severidade": "Media", "corrigida": True},
    {"cve_id": "CVE-2024-003", "tipo": "Path Traversal", "severidade": "Critica", "corrigida": False},
]


def main():
    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_DATABASE]
        col = db.vulnerabilidades

        col.delete_many({})
        col.insert_many(VULNS)

        print("Buscar severidade='Alta':")
        for doc in col.find({"severidade": "Alta"}):
            print(f"{doc['cve_id']}: {doc['tipo']}")

        resultado = col.update_one(
            {"cve_id": "CVE-2024-001"}, {"$set": {"corrigida": True}}
        )
        print(f"\nupdate corrigida=True em 001 -> "
              f"\"{resultado.modified_count} documento modificado\"")

        abertas = col.count_documents({"corrigida": False})
        print(f"\ncount corrigida=False -> {abertas}")

        deletado = col.delete_one({"cve_id": "CVE-2024-002"})
        print(f"\ndelete por cve_id (CVE-2024-002) -> "
              f"{deletado.deleted_count} documento removido")
    finally:
        client.close()


if __name__ == "__main__":
    main()
