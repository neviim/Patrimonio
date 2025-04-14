# inserir_consultar_patrimonio.py

import sys
from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

# --- CONSULTA POR ID DE PATRIMÔNIO OU USUÁRIO ---
def consultar_patrimonio_ou_usuario(tipo: str, valor: str):
    if tipo == "patrimonio":
        dados = crud.buscar_patrimonio_por_id(valor.upper())
        if dados:
            print(f"\n📘 Resultado da busca por patrimônio '{valor.upper()}':")
            print("")

            for k, v in dados.items():
                print(f"   {k}: {v}")
        else:
            print(f"❌ Patrimônio '{valor.upper()}' não encontrado.")

    elif tipo == "usuario":
        dados = crud.buscar_patrimonios_por_usuario(valor)
        if dados:
            print(f"\n👤 Patrimônios associados ao usuário '{valor}':")
            print("")
            
            for item in dados:
                print("   ---")
                for k, v in item.items():
                    print(f"   {k}: {v}")
        else:
            print(f"❌ Nenhum patrimônio encontrado para o usuário '{valor}'.")
    else:
        print("⚠️ Tipo inválido. Use 'patrimonio' ou 'usuario'.")

# --- LEITURA DE PARÂMETRO VIA TERMINAL ---
if len(sys.argv) != 3:
    print("Uso: python inserir_consultar_patrimonio.py [patrimonio|usuario] <valor>")
else:
    tipo_param = sys.argv[1].lower()
    valor_param = sys.argv[2]
    consultar_patrimonio_ou_usuario(tipo_param, valor_param)

# Fecha conexão ao final
crud.close()


# Como utilizar:
# 
# python consultar_user_patri.py patrimonio P123456
# python consultar_user_patri.py usuario jdoe
# 

