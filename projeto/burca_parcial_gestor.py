# busca_parcial_gestor.py

import sys
from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

def listar_parcial_gestor(termo: str):
    try:
        dados = crud.buscar_patrimonios_parcial_por_gestor(termo)

        if dados:
            print(f"\n🔍 Patrimônios gerenciados por gestores contendo '{termo}':")
            for item in dados:
                print("   ---")
                for k, v in item.items():
                    print(f"   {k}: {v}")
        else:
            print(f"❌ Nenhum patrimônio encontrado para gestores contendo '{termo}'.")
    except Exception as e:
        print(f"Erro ao consultar por parte do nome do gestor: {e}")

# Execução via terminal
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python busca_parcial_gestor.py <parte_do_nome_do_gestor>")
    else:
        listar_parcial_gestor(sys.argv[1])

    crud.close()

# python burca_parcial_gestor.py silva

