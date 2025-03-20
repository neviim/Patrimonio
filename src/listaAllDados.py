from neo4j import GraphDatabase

# Configuração do banco Neo4j
URI = "bolt://localhost:7687"  # Verifique se está correto
USER = "neo4j"
PASSWORD = "#neo4JJ4oen#"

class PatrimonioLister:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
            print("✅ Conectado ao Neo4j com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar ao Neo4j: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()
            print("🔌 Conexão com Neo4j fechada.")

    def list_all_patrimonios(self):
        if not self.driver:
            print("❌ Conexão com Neo4j não estabelecida. Abortando listagem.")
            return []

        with self.driver.session() as session:
            result = session.read_transaction(self._get_all_patrimonios)
            return result

    @staticmethod
    def _get_all_patrimonios(tx):
        query = "MATCH (p:Patrimonio) RETURN p.id AS id, p.nome AS nome, p.categoria AS categoria, p.localizacao AS localizacao, p.valor AS valor, p.data_aquisicao AS data_aquisicao"
        result = tx.run(query)
        return [record for record in result]

if __name__ == "__main__":
    lister = PatrimonioLister(URI, USER, PASSWORD)
    patrimonios = lister.list_all_patrimonios()
    
    if patrimonios:
        print("📋 Listagem de Patrimônios:")
        for patrimonio in patrimonios:
            print(patrimonio)
    else:
        print("⚠️ Nenhum patrimônio encontrado.")

    lister.close()
