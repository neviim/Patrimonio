from neo4j import GraphDatabase
import sys

def check_neo4j_connectivity(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*"):
    """
    Verifica a conectividade ao banco de dados Neo4j.

    :param uri: URI do banco de dados Neo4j (default: bolt://10.0.14.23:7687)
    :param user: Nome de usuário para autenticação (default: ticncp)
    :param password: Senha para autenticação (default: #neo4jcn*)
    :return: True se a conectividade estiver ok, False caso contrário
    """
    try:
        # Criar o driver Neo4j
        driver = GraphDatabase.driver(uri, auth=(user, password))

        # Verificar conectividade
        with driver.session() as session:
            result = session.run("RETURN 1 AS number")  # Executa uma consulta simples
            record = result.single()  # Obtém o primeiro registro do resultado

            if record:
                print(f"Conectividade ao banco de dados Neo4j verificada com sucesso! Resultado: {record['number']}")
                return True
            else:
                print("Erro: Não foi possível obter um resultado da consulta.")
                return False

    except Exception as e:
        print(f"Erro ao conectar ao banco de dados Neo4j: {str(e)}")
        return False

# Exemplo de uso
if __name__ == "__main__":
    is_connected = check_neo4j_connectivity()
    if is_connected:
        print("O sistema está conectado ao banco de dados Neo4j.")
    else:
        print("Falha na conectividade ao banco de dados Neo4j.")