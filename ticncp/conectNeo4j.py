from neo4j import GraphDatabase
import sys
import pandas as pd

class Neo4jConnection:
    def __init__(self):
        self.uri = "bolt://localhost:7687"
        self.user = "neo4j"
        self.password = "#neo4jcn*"
        self.driver = None

    def connect(self):
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            print("Conectando ao Neo4j...")
            
            # Testa a conexão
            self.driver.verify_connectivity()
            print("Conexão estabelecida com sucesso!")
            
            # Executa uma query simples para validar
            with self.driver.session() as session:
                result = session.run("MATCH (n) RETURN count(n) as count")
                count = result.single()["count"]
                print(f"Total de nós no banco de dados: {count}")
                
        except Exception as e:
            print(f"Erro ao conectar ao Neo4j: {str(e)}")
            sys.exit(1)

    def import_csv(self, file_path):
        try:
            # Lê o arquivo CSV usando pandas
            df = pd.read_csv(file_path)
            print(f"Arquivo CSV carregado. Total de linhas: {len(df)}")

            # Cria nós para cada linha do CSV
            with self.driver.session() as session:
                # Primeiro, limpa os dados existentes
                session.run("MATCH (n:Patrimonio) DETACH DELETE n")
                
                # Importa os novos dados
                for index, row in df.iterrows():
                    # Converte a linha para dicionário e remove valores NaN
                    properties = row.to_dict()
                    properties = {k: str(v) for k, v in properties.items() if pd.notna(v)}
                    
                    # Query Cypher para criar o nó
                    query = """
                    CREATE (p:Patrimonio)
                    SET p = $properties
                    """
                    session.run(query, properties=properties)
                    
                    if (index + 1) % 100 == 0:
                        print(f"Importados {index + 1} registros...")

                print("Importação concluída!")
                
                # Conta o total de registros
                result = session.run("MATCH (n:Patrimonio) RETURN count(n) as count")
                count = result.single()["count"]
                print(f"Total de registros no banco: {count}")

        except Exception as e:
            print(f"Erro durante a importação: {str(e)}")

    def close(self):
        if self.driver:
            self.driver.close()
            print("Conexão fechada.")

if __name__ == "__main__":
    # Cria uma instância da conexão
    neo4j_conn = Neo4jConnection()
    
    # Tenta conectar
    neo4j_conn.connect()
    
    # Importa o arquivo CSV
    neo4j_conn.import_csv('aipf-patrimonio_Igienizada.csv')
    
    # Fecha a conexão
    neo4j_conn.close()
