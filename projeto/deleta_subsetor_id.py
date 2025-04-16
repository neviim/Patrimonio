# deleta_subsetor_id.py

import sys
from patrimonio_crud import PatrimonioCRUD

crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

def remover_subsetor_por_id(subsetor_id: str):
    sucesso = crud.remover_subsetor_por_id(subsetor_id)
    if sucesso:
        print(f"✅ SubSetor com ID '{subsetor_id}' removido com sucesso.")
    else:
        print(f"❌ Falha ao remover o SubSetor com ID '{subsetor_id}'.")

# Execução via terminal
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python deleta_subsetor_id.py <id_do_subsetor>")
    else:
        remover_subsetor_por_id(sys.argv[1])

    crud.close()

# python deleta_subsetor_id.py SS102

