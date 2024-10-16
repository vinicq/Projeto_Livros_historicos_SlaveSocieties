# Este arquivo pode ser usado para implementar e treinar modelos de aprendizado de máquina
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def treinar_modelo(dados):
    # Supondo que 'dados' seja um DataFrame do pandas
    X = dados.drop('target', axis=1)  # Substitua 'target' pelo nome da coluna alvo
    y = dados['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier()
    modelo.fit(X_train, y_train)

    acuracia = modelo.score(X_test, y_test)
    print(f"Acurácia do modelo: {acuracia:.2f}")
