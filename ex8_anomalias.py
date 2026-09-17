"""
Exercicio 8 - Deteccao de anomalias (IsolationForest)
[requisicoes_min, conexoes_simultaneas] -> -1 = anomalia, 1 = normal
"""
import numpy as np
from sklearn.ensemble import IsolationForest

TRAFEGO = np.array([
    [100, 5], [120, 6], [110, 5], [105, 4], [50000, 500], [109, 5], [111, 6], [45000, 450],
])


def main():
    modelo = IsolationForest(contamination=0.25, random_state=42)
    predicoes = modelo.fit_predict(TRAFEGO)

    for i, (amostra, rotulo) in enumerate(zip(TRAFEGO, predicoes)):
        status = "ANOMALIA" if rotulo == -1 else "Normal"
        valores = [int(v) for v in amostra]
        print(f"Amostra {i}: {valores} -> {status}")


if __name__ == "__main__":
    main()
