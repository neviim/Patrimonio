# inserir_consultar_patrimonio.py

from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")


# --- CONSULTA DO PATRIMÔNIO INSERIDO ---
# resultado = crud.buscar_patrimonio_por_id("P123456")

# if resultado:
#     print("\n🔎 Patrimônio encontrado:")
#     for chave, valor in resultado.items():
#         print(f"{chave}: {valor}")
# else:
#     print("⚠️ Patrimônio não encontrado.")

# --- CONSULTA POR ID DE PATRIMÔNIO OU USUÁRIO ---
def consultar_patrimonio_ou_usuario(tipo: str, valor: str):
    if tipo == "patrimonio":
        dados = crud.buscar_patrimonio_por_id(valor)
        if dados:
            print(f"\n📘 Resultado da busca por patrimônio '{valor}':")
            for k, v in dados.items():
                print(f"{k}: {v}")
        else:
            print(f"❌ Patrimônio '{valor}' não encontrado.")

    elif tipo == "usuario":
        dados = crud.buscar_patrimonios_por_usuario(valor)
        if dados:
            print(f"\n👤 Patrimônios associados ao usuário '{valor}':")
            for item in dados:
                print("---")
                for k, v in item.items():
                    print(f"{k}: {v}")
        else:
            print(f"❌ Nenhum patrimônio encontrado para o usuário '{valor}'.")
    else:
        print("⚠️ Tipo inválido. Use 'patrimonio' ou 'usuario'.")

# Exemplo de uso das consultas
consultar_patrimonio_ou_usuario("patrimonio", "P123456")
consultar_patrimonio_ou_usuario("usuario", "jdoe")

# Fecha conexão ao final
crud.close()
