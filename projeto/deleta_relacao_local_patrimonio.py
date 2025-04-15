# deleta_relacao_local_patrimonio.py

import sys
from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

def remover_relacao_local(patrimonio_id: str):
    sucesso = crud.remover_relacao_local_patrimonio(patrimonio_id)
    if sucesso:
        print(f"✅ Relação entre o patrimônio '{patrimonio_id}' e o local foi removida com sucesso.")
    else:
        print(f"❌ Falha ao remover a relação com o local para o patrimônio '{patrimonio_id}'.")

# Execução via terminal
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python deleta_relacao_local_patrimonio.py <patrimonio_id>")
    else:
        remover_relacao_local(sys.argv[1])

    crud.close()

# python deleta_relacao_local_patrimonio.py PC003

