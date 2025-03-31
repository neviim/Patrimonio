from neo4j import GraphDatabase
import logging
from tabulate import tabulate
import time

class Neo4jStatusChecker:
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
    
    def get_database_status(self):
        """Retorna um dicionário com o status do banco de dados Neo4j"""
        if not self.driver:
            success = self.connect()
            if not success:
                return {"error": "Falha ao conectar ao banco de dados"}
        
        status = {}
        
        try:
            with self.driver.session() as session:
                # Obter nome e status da database atual
                db_info = session.run("CALL db.info()").data()[0]
                status["database_name"] = db_info.get("name", "unknown")
                status["database_status"] = "online"  # Se conseguimos executar a query, está online
                
                # Total de nós
                result = session.run("MATCH (n) RETURN count(n) as count")
                status["nodes"] = result.single()["count"]
                
                # Total de relacionamentos
                result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
                status["relationships"] = result.single()["count"]
                
                # Labels
                result = session.run("CALL db.labels()")
                labels = [record["label"] for record in result]
                status["labels"] = labels
                status["labels_count"] = len(labels)
                
                # Relationship Types
                result = session.run("CALL db.relationshipTypes()")
                rel_types = [record["relationshipType"] for record in result]
                status["relationship_types"] = rel_types
                status["relationship_types_count"] = len(rel_types)
                
                # Property Keys
                result = session.run("CALL db.propertyKeys()")
                prop_keys = [record["propertyKey"] for record in result]
                status["property_keys"] = prop_keys
                status["property_keys_count"] = len(prop_keys)
                
                # Constraints
                try:
                    result = session.run("SHOW CONSTRAINTS")
                    constraints = [dict(record) for record in result]
                    status["constraints"] = constraints
                    status["constraints_count"] = len(constraints)
                except:
                    # Fallback para versões anteriores do Neo4j
                    result = session.run("CALL db.constraints()")
                    constraints = [dict(record) for record in result]
                    status["constraints"] = constraints
                    status["constraints_count"] = len(constraints)
                
                # Indexes
                try:
                    result = session.run("SHOW INDEXES")
                    indexes = [dict(record) for record in result]
                    status["indexes"] = indexes
                    status["indexes_count"] = len(indexes)
                except:
                    # Fallback para versões anteriores do Neo4j
                    result = session.run("CALL db.indexes()")
                    indexes = [dict(record) for record in result]
                    status["indexes"] = indexes
                    status["indexes_count"] = len(indexes)
                
                # Informações de memória e armazenamento
                try:
                    result = session.run("CALL dbms.listTransactions()")
                    transactions = [dict(record) for record in result]
                    status["active_transactions"] = len(transactions)
                except:
                    status["active_transactions"] = "N/A"
                
                # Versão do Neo4j
                try:
                    result = session.run("CALL dbms.components() YIELD name, versions WHERE name = 'Neo4j Kernel' RETURN versions[0] AS version")
                    version = result.single()["version"]
                    status["neo4j_version"] = version
                except:
                    status["neo4j_version"] = "N/A"
                
                # Adicionar timestamp
                status["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
                
                return status
        except Exception as e:
            logging.error(f"Erro ao obter status do banco de dados: {str(e)}")
            return {"error": str(e)}
    
    def print_status(self):
        """Imprime o status do banco de dados em formato tabular"""
        status = self.get_database_status()
        
        if "error" in status:
            print(f"Erro: {status['error']}")
            return
        
        # Tabela principal com estatísticas gerais
        main_data = [
            ["Database", status["database_name"]],
            ["Status", status["database_status"]],
            ["Neo4j Version", status.get("neo4j_version", "N/A")],
            ["Nodes", status["nodes"]],
            ["Relationships", status["relationships"]],
            ["Labels", status["labels_count"]],
            ["Relationship Types", status["relationship_types_count"]],
            ["Property Keys", status["property_keys_count"]],
            ["Constraints", status["constraints_count"]],
            ["Indexes", status["indexes_count"]],
            ["Active Transactions", status.get("active_transactions", "N/A")],
            ["Timestamp", status["timestamp"]]
        ]
        
        print("\n=== NEO4J DATABASE STATUS ===")
        print(tabulate(main_data, tablefmt="pretty"))
        
        # Imprimir detalhes de labels, relationship types e property keys
        if status["labels"]:
            print("\n=== LABELS ===")
            print(", ".join(status["labels"]))
        
        if status["relationship_types"]:
            print("\n=== RELATIONSHIP TYPES ===")
            print(", ".join(status["relationship_types"]))
        
        if status["property_keys"]:
            print("\n=== PROPERTY KEYS ===")
            print(", ".join(status["property_keys"]))
        
        # Imprimir constraints e indexes se existirem
        if status["constraints_count"] > 0:
            print("\n=== CONSTRAINTS ===")
            for constraint in status["constraints"]:
                print(f"- {constraint}")
        
        if status["indexes_count"] > 0:
            print("\n=== INDEXES ===")
            for index in status["indexes"]:
                print(f"- {index}")
    
    def export_status_json(self, filename="neo4j_status.json"):
        """Exporta o status do banco de dados para um arquivo JSON"""
        import json
        status = self.get_database_status()
        
        try:
            with open(filename, 'w') as f:
                json.dump(status, f, indent=2, default=str)
            print(f"Status exportado para {filename}")
            return True
        except Exception as e:
            logging.error(f"Erro ao exportar status: {str(e)}")
            return False


# Exemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Criar instância e verificar status
    checker = Neo4jStatusChecker()
    checker.print_status()
    
    # Opcional: exportar para JSON
    # checker.export_status_json()
    
    # Fechar a conexão
    checker.close()