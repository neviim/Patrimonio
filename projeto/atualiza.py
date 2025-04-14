# atualiza.py

import json
import sys
from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

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

# Execução via terminal
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python atualiza.py <caminho_para_arquivo_json>")
    else:
        atualizar_patrimonio_via_json(sys.argv[1])

    crud.close()

# Como utilizar: crie um arquivo: atualizacao_pc001.json
# {
#   "patrimonio_id": "PC001",
#   "local": "Sala de Reunião 3",
#   "setor": "TI",
#   "gestor": "João da Silva",
#   "subsetor": "Infraestrutura",
#   "usuario_login": "jsilva",
#   "usuario_nome": "João da Silva",
#   "locadora": "Locadora XYZ"
# }

# python atualiza.py ./data/atualizacao_pc001.json

