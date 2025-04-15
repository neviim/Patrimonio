# listar_por_local.py

import sys
from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

def listar_patrimonios_por_local(local: str):
    try:
        dados = crud.listar_patrimonios_por_local(local)

        if dados:
            print(f"\n📍 Patrimônios no local '{local}':")
            for item in dados:
                print("   ---")
                for k, v in item.items():
                    print(f"   {k}: {v}")
        else:
            print(f"❌ Nenhum patrimônio encontrado no local '{local}'.")
    except Exception as e:
        print(f"Erro ao consultar por local: {e}")

# Execução via terminal
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python listar_por_local.py <nome_do_local>")
    else:
        listar_patrimonios_por_local(sys.argv[1])

    crud.close()



# python listar_por_local.py "Sala 101"
