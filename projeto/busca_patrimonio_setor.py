# lista_patrimonio_setor.py

import sys
from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

def listar_patrimonios_por_setor(setor: str):
    try:
        dados = crud.buscar_patrimonios_por_setor(setor)

        if dados:
            print(f"\n🏢 Patrimônios no setor '{setor}':")
            for item in dados:
                print("   ---")
                for k, v in item.items():
                    print(f"   {k}: {v}")
        else:
            print(f"❌ Nenhum patrimônio encontrado no setor '{setor}'.")
    except Exception as e:
        print(f"Erro ao consultar por setor: {e}")

# Execução via terminal
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python lista_patrimonio_setor.py <nome_do_setor>")
    else:
        listar_patrimonios_por_setor(sys.argv[1])

    crud.close()

# python busca_patrimonio_setor.py "TI"
