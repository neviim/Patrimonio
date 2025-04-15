# deleta_relacao_usuario.py

import sys
from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

def deleta_relacao_usuario(patrimonio_id: str, usuario_login: str):
    sucesso = crud.remover_relacao_usuario(patrimonio_id, usuario_login)
    if sucesso:
        print(f"✅ Relação entre usuário '{usuario_login}' e patrimônio '{patrimonio_id}' removida com sucesso.")
    else:
        print(f"❌ Falha ao remover a relação entre usuário '{usuario_login}' e patrimônio '{patrimonio_id}'.")

# Execução via terminal
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python deleta_relacao_usuario.py <patrimonio_id> <usuario_login>")
    else:
        deleta_relacao_usuario(sys.argv[1], sys.argv[2])

    crud.close()

    # python deleta_relacao_usuario.py PC001 jdoe

