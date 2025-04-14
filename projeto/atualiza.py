# inserir_consultar_patrimonio.py

import sys
import json
from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

# --- FUNÇÃO PARA ATUALIZAR UM PATRIMÔNIO A PARTIR DE UM JSON ---
def atualizar_patrimonio_via_json(caminho_json: str):
    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        patrimonio_id = dados.get("patrimonio_id")
        if not patrimonio_id:
            print("❌ O campo 'patrimonio_id' é obrigatório no JSON.")
            return

        atualizado = crud.atualizar_patrimonio(patrimonio_id.upper(), **{k: v for k, v in dados.items() if k != "patrimonio_id"})
        if atualizado:
            print(f"✅ Patrimônio '{patrimonio_id.upper()}' atualizado com sucesso.")
        else:
            print(f"❌ Falha ao atualizar o patrimônio '{patrimonio_id.upper()}'.")

    except Exception as e:
        print(f"Erro ao ler ou atualizar a partir do JSON: {e}")