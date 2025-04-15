# inserir_consultar_patrimonio.py

from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

# --- INSERÇÃO DE UM NOVO PATRIMÔNIO ---
novo_patrimonio = {
    "patrimonio_id": "PC003",
    "setor": "Administrativo",
    "local": "Sala 102",
    "gestor": "Maria Oliveira",
    "subsetor": "",
    "usuario_login": "ana.santos",
    "usuario_nome": "Ana S. Santos",
    "locadora": "Locadora XYZ"
}

inserido = crud.criar_patrimonio(**novo_patrimonio)
if inserido:
    print("✅ Patrimônio inserido com sucesso!")
else:
    print("❌ Falha ao inserir o patrimônio.")

    