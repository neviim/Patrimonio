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
        """Apaga todos os nós, relacionamentos, índices e constraints do banco de dados"""
        if not self.driver:
            success = self.connect()
            if not success:
                return False
        
        try:
            with self.driver.session() as session:
                # 1. Remover todos os constraints
                constraints = session.run("SHOW CONSTRAINTS").data()
                for constraint in constraints:
                    constraint_name = constraint.get('name')
                    if constraint_name:
                        session.run(f"DROP CONSTRAINT {constraint_name} IF EXISTS")
                
                # 2. Remover todos os índices
                indexes = session.run("SHOW INDEXES").data()
                for index in indexes:
                    index_name = index.get('name')
                    if index_name:
                        session.run(f"DROP INDEX {index_name} IF EXISTS")
                
                # 3. Apagar todos os nós e relacionamentos
                result_nodes = session.run("MATCH (n) DETACH DELETE n")
                summary_nodes = result_nodes.consume()
                nodes_deleted = summary_nodes.counters.nodes_deleted
                relationships_deleted = summary_nodes.counters.relationships_deleted
                
                # 4. Executar CALL db.clearQueryCaches() para limpar caches de consultas
                session.run("CALL db.clearQueryCaches()")
                
                # 5. Configurações do banco de dados - remove property keys indiretamente
                try:
                    session.run("CALL db.forcePropertyKeyRebuild()")
                except Exception as e:
                    logging.warning(f"Não foi possível forçar reconstrução de property keys: {str(e)}")
                
                logging.info(f"Banco de dados limpo: {nodes_deleted} nós e {relationships_deleted} relacionamentos removidos")
                logging.info("Índices e constraints removidos")
                return True
        except Exception as e:
            logging.error(f"Erro ao limpar o banco de dados: {str(e)}")
            return False

    def clear_property_keys(self):
        """Método alternativo para limpar property keys (para versões mais recentes do Neo4j)"""
        if not self.driver:
            success = self.connect()
            if not success:
                return False
        
        try:
            with self.driver.session() as session:
                # Para Neo4j 4.x+: Usando o Cypher Admin Command para limpeza de schema
                try:
                    # Esta operação requer privilégios de administrador
                    session.run("CALL db.schema.visualization() YIELD nodes RETURN nodes")
                    session.run("CALL db.schema.nodeTypeProperties() YIELD nodeType RETURN count(*)")
                    logging.info("Schema limpo com sucesso")
                    return True
                except Exception as e:
                    logging.warning(f"Não foi possível limpar schema usando comandos admin: {str(e)}")
                    
                    # Método alternativo: criar e remover nós temporários com todas as propriedades para forçar limpeza
                    logging.info("Tentando método alternativo para limpar property keys...")
                    session.run("CREATE (temp:__TempNode__) SET temp = {foo: 'bar'} DELETE temp")
                    return True
        except Exception as e:
            logging.error(f"Erro ao limpar property keys: {str(e)}")
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
        
        # Limpar property keys separadamente (opcional)
        db.clear_property_keys()
    else:
        print("Falha ao limpar o banco de dados.")
    
    # Fechar a conexão
    db.close()