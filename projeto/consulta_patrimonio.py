# inserir_consultar_patrimonio.py

from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")


# --- CONSULTA DO PATRIMÔNIO INSERIDO ---
resultado = crud.buscar_patrimonio_por_id("P123456")

if resultado:
    print("\n🔎 Patrimônio encontrado:")
    print("   ----------------------")

    for chave, valor in resultado.items():
        print(f"   {chave}: {valor}")
else:
    print("⚠️ Patrimônio não encontrado.")


# Fecha conexão ao final
crud.close()