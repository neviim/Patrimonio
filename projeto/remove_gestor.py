# remove_gestor.py

import sys
from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

def remover_gestor(nome: str):
    sucesso = crud.remover_gestor(nome)
    if sucesso:
        print(f"✅ Gestor '{nome}' removido com sucesso.")
    else:
        print(f"❌ Falha ao remover o gestor '{nome}'.")

# Execução via terminal
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python remove_gestor.py <nome_do_gestor>")
    else:
        remover_gestor(sys.argv[1])

    crud.close()

# python remove_gestor.py "Marina Oliveira"

