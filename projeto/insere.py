# inserir_consultar_patrimonio.py

from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

# --- INSERÇÃO DE UM NOVO PATRIMÔNIO ---
novo_patrimonio = {
    "patrimonio_id": "P123456",
    "setor": "TI",
    "local": "Sala 101",
    "gestor": "Carlos Silva",
    "subsetor": "Infraestrutura",
    "usuario_login": "jdoe",
    "usuario_nome": "John Doe",
    "locadora": "Locadora XYZ"
}

inserido = crud.criar_patrimonio(**novo_patrimonio)
if inserido:
    print("✅ Patrimônio inserido com sucesso!")
else:
    print("❌ Falha ao inserir o patrimônio.")

    