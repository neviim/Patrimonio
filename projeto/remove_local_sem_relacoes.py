# remove_local_sem_relacoes.py

import sys
from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

def remover_local(nome: str):
    sucesso = crud.remover_local_se_sem_relacoes(nome)
    if sucesso:
        print(f"✅ Local '{nome}' removido com sucesso.")
    else:
        print(f"❌ O local '{nome}' não foi removido. Pode ainda conter relações.")

# Execução via terminal
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python remove_local_sem_relacoes.py <nome_do_local>")
    else:
        remover_local(sys.argv[1])

    crud.close()


# python remove_local_sem_relacoes.py "Sala de Reunião 3"

