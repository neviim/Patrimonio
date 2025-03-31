from neo4j import GraphDatabase
import logging

class Neo4jDatabase:
    def __init__(self):
        self.uri = "bolt://localhost:7687"
        self.user = "neo4j"
        self.password = "#neo4jcn*"
        self.driver = None
        
    def connect(self):
        """Estabelece conexão com o banco de dados Neo4j"""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            logging.info("Conexão com o Neo4j estabelecida com sucesso")
            return True
        except Exception as e:
            logging.error(f"Erro ao conectar ao Neo4j: {str(e)}")
            return False
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.driver:
            self.driver.close()
            logging.info("Conexão com o Neo4j fechada")
    
    def clear_database(self):
        """Apaga todos os nós e relacionamentos do banco de dados"""
        if not self.driver:
            success = self.connect()
            if not success:
                return False
        
        try:
            with self.driver.session() as session:
                # Executa a query para apagar todos os nós e relacionamentos
                result = session.run("MATCH (n) DETACH DELETE n")
                # Obtem estatísticas do resultado
                summary = result.consume()
                nodes_deleted = summary.counters.nodes_deleted
                relationships_deleted = summary.counters.relationships_deleted
                
                logging.info(f"Banco de dados limpo: {nodes_deleted} nós e {relationships_deleted} relacionamentos removidos")
                return True
        except Exception as e:
            logging.error(f"Erro ao limpar o banco de dados: {str(e)}")
            return False


# Exemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Criar instância da classe e limpar o banco de dados
    db = Neo4jDatabase()
    success = db.clear_database()
    
    if success:
        print("Banco de dados limpo com sucesso!")
    else:
        print("Falha ao limpar o banco de dados.")
    
    # Fechar a conexão
    db.close()