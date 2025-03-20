from neo4j import GraphDatabase
import pandas as pd

# Configuração do banco Neo4j
URI = "bolt://localhost:7687"  # Verifique se está correto
USER = "neo4j"
PASSWORD = "#neo4JJ4oen#"

class PatrimonioImporter:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()  # Testa a conexão ao iniciar
            print("✅ Conectado ao Neo4j com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar ao Neo4j: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()
            print("🔌 Conexão com Neo4j fechada.")

    def import_data(self, file_path):
        if not self.driver:
            print("❌ Conexão com Neo4j não estabelecida. Abortando importação.")
            return
        
        try:
            df = pd.read_csv(file_path)
            print(f"📂 {len(df)} registros carregados do arquivo CSV.")

            with self.driver.session() as session:
                for _, row in df.iterrows():
                    if pd.notna(row.get('id')) and pd.notna(row.get('nome')):  # Evita entradas sem ID ou nome
                        session.write_transaction(self._create_or_update_patrimonio, row)
            print("✅ Importação concluída!")

        except Exception as e:
            print(f"❌ Erro ao importar dados: {e}")

    @staticmethod
    def _create_or_update_patrimonio(tx, row):
        query = """
        MERGE (p:Patrimonio {id: $id})
        ON CREATE SET p.nome = $nome, p.categoria = $categoria, p.localizacao = $localizacao, 
                      p.valor = $valor, p.data_aquisicao = $data_aquisicao
        ON MATCH SET p.valor = $valor, p.localizacao = $localizacao  // Atualiza dados caso já exista
        """
        try:
            tx.run(query, id=row['id'], nome=row['nome'], categoria=row.get('categoria', 'Desconhecida'), 
                   localizacao=row.get('localizacao', 'Não Informado'), valor=row.get('valor', 0), 
                   data_aquisicao=row.get('data_aquisicao', 'Desconhecida'))
        except Exception as e:
            print(f"⚠️ Erro ao inserir registro {row['id']}: {e}")

if __name__ == "__main__":
    file_path = "./data/aipf-patrimonio_restructured.csv"  # Verifique se este é o caminho correto
    importer = PatrimonioImporter(URI, USER, PASSWORD)
    importer.import_data(file_path)
    importer.close()

