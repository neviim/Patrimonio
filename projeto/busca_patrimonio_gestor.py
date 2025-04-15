# lista_patrimonio_gestor.py

import sys
from patrimonio_crud import PatrimonioCRUD

# Instancia a classe de acesso ao banco de dados
crud = PatrimonioCRUD(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*")

def busca_patrimonios_por_gestor(gestor: str):
    try:
        dados = crud.listar_patrimonios_por_gestor(gestor)

        if dados:
            print(f"\n👤 Patrimônios sob responsabilidade do gestor '{gestor}':")
            for item in dados:
                print("---")
                for k, v in item.items():
                    print(f"{k}: {v}")
        else:
            print(f"❌ Nenhum patrimônio encontrado para o gestor '{gestor}'.")
    except Exception as e:
        print(f"Erro ao consultar por gestor: {e}")

# Execução via terminal
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python busca_patrimonio_gestor.py <nome_do_gestor>")
    else:
        busca_patrimonios_por_gestor(sys.argv[1])

    crud.close()

# python busca_patrimonio_gestor.py "João da Silva"

