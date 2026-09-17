"""
Exercicio 9 - Metricas honestas em conjunto desbalanceado

Comentario: a acuracia sozinha e enganosa aqui porque a classe majoritaria
(normal) domina o calculo. Mesmo perdendo METADE dos ataques reais (recall
0.50), a acuracia ainda aparece alta (0.90) so por acertar quase todos os
casos normais -- por isso em seguranca sempre olhamos recall/precisao/F1
junto da matriz de confusao, nunca so a acuracia.
"""
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
)

y_true = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]  # 8 normais, 2 ataques
y_pred = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]  # perdeu 1 ataque


def main():
    matriz = confusion_matrix(y_true, y_pred)
    acuracia = accuracy_score(y_true, y_pred)
    precisao = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f"Matriz: {matriz.tolist()}")
    print(f"Acuracia: {acuracia:.2f} | Precisao: {precisao:.2f} | "
          f"Recall: {recall:.2f} | F1: {f1:.2f}")
    print("Comentario: acuracia 0.90 mascara que METADE dos ataques "
          "passou (recall 0.50).")


if __name__ == "__main__":
    main()
