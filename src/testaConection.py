from neo4j import GraphDatabase

# Configuração do banco Neo4j
URI = "bolt://localhost:7687"  # Altere caso necessário
USER = "neo4j"
PASSWORD = "#neo4JJ4oen#"  # Substitua pela senha correta

def test_neo4j_connection(uri, user, password):
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run("RETURN 'Conexão bem-sucedida' AS mensagem")
            for record in result:
                print(record["mensagem"])
        driver.close()
        return True
    except Exception as e:
        print(f"Erro ao conectar ao Neo4j: {e}")
        return False

if __name__ == "__main__":
    if test_neo4j_connection(URI, USER, PASSWORD):
        print("✅ Conectado ao Neo4j com sucesso!")
    else:
        print("❌ Falha na conexão com o Neo4j.")
