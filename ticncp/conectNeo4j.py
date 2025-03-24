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
            self.driver.verify_connectivity()
            print("Conexão estabelecida com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar ao Neo4j: {str(e)}")
            sys.exit(1)

    def import_and_relate_data(self, file_path):
        try:
            # Lê o arquivo CSV e preenche valores NaN
            df = pd.read_csv(file_path)
            # Preenche valores NaN com "Não Especificado"
            df = df.fillna("Não Especificado")
            print(f"Arquivo CSV carregado. Total de linhas: {len(df)}")

            with self.driver.session() as session:
                # Limpa o banco de dados
                session.run("MATCH (n) DETACH DELETE n")

                # 1. Primeiro, cria nós únicos para cada entidade
                print("Criando nós de entidades...")
                
                # Cria Setores
                query_setor = """
                WITH $setores AS setores
                UNWIND setores AS setor
                MERGE (s:Setor {nome: setor})
                """
                setores = df['Setor'].unique().tolist()
                session.run(query_setor, setores=setores)

                # Cria SubSetores (agora com tratamento de valores nulos)
                query_subsetor = """
                WITH $subsetores AS subsetores
                UNWIND subsetores AS subsetor
                MERGE (ss:SubSetor {nome: subsetor})
                """
                subsetores = df['SubSetor'].unique().tolist()
                session.run(query_subsetor, subsetores=subsetores)

                # Cria Gestores
                query_gestor = """
                WITH $gestores AS gestores
                UNWIND gestores AS gestor
                MERGE (g:Gestor {nome: gestor})
                """
                gestores = df['Gestor'].unique().tolist()
                session.run(query_gestor, gestores=gestores)

                # Cria Locais
                query_local = """
                WITH $locais AS locais
                UNWIND locais AS local
                MERGE (l:Local {nome: local})
                """
                locais = df['Local'].unique().tolist()
                session.run(query_local, locais=locais)

                # Cria Locações
                query_locacao = """
                WITH $locacoes AS locacoes
                UNWIND locacoes AS locacao
                MERGE (loc:Locacao {nome: locacao})
                """
                locacoes = df['Locacao'].unique().tolist()
                session.run(query_locacao, locacoes=locacoes)

                # 2. Cria os itens de Patrimônio e seus relacionamentos
                print("Criando itens de patrimônio e relacionamentos...")
                
                query_patrimonio = """
                CREATE (p:Patrimonio)
                SET p = $properties
                WITH p
                MATCH (s:Setor {nome: $setor})
                MATCH (ss:SubSetor {nome: $subsetor})
                MATCH (g:Gestor {nome: $gestor})
                MATCH (l:Local {nome: $local})
                MATCH (loc:Locacao {nome: $locacao})
                CREATE (p)-[:PERTENCE_AO_SETOR]->(s)
                CREATE (p)-[:PERTENCE_AO_SUBSETOR]->(ss)
                CREATE (p)-[:GERIDO_POR]->(g)
                CREATE (p)-[:LOCALIZADO_EM]->(l)
                CREATE (p)-[:ALOCADO_EM]->(loc)
                """

                # Processa cada item do patrimônio
                for index, row in df.iterrows():
                    properties = row.to_dict()
                    # Remove as colunas que viraram relacionamentos
                    relacionamentos = ['Setor', 'SubSetor', 'Gestor', 'Local', 'Locacao']
                    for rel in relacionamentos:
                        if rel in properties:
                            del properties[rel]

                    session.run(query_patrimonio, 
                              properties=properties,
                              setor=row['Setor'],
                              subsetor=row['SubSetor'],
                              gestor=row['Gestor'],
                              local=row['Local'],
                              locacao=row['Locacao'])

                    if (index + 1) % 100 == 0:
                        print(f"Processados {index + 1} registros...")

                # 3. Cria relacionamentos hierárquicos
                print("Criando relacionamentos hierárquicos...")
                
                # Relaciona SubSetor com Setor
                query_hierarquia = """
                MATCH (ss:SubSetor)
                MATCH (s:Setor)
                WHERE ss.setor = s.nome
                CREATE (ss)-[:PERTENCE_AO_SETOR]->(s)
                """
                session.run(query_hierarquia)

                print("Importação e relacionamentos concluídos!")
                
                # Estatísticas finais
                self._print_statistics(session)

        except Exception as e:
            print(f"Erro durante a importação: {str(e)}")

    def _print_statistics(self, session):
        """Imprime estatísticas do banco de dados"""
        stats = [
            ("Patrimônios", "MATCH (p:Patrimonio) RETURN count(p) as count"),
            ("Setores", "MATCH (s:Setor) RETURN count(s) as count"),
            ("SubSetores", "MATCH (ss:SubSetor) RETURN count(ss) as count"),
            ("Gestores", "MATCH (g:Gestor) RETURN count(g) as count"),
            ("Locais", "MATCH (l:Local) RETURN count(l) as count"),
            ("Locações", "MATCH (loc:Locacao) RETURN count(loc) as count"),
            ("Relacionamentos", "MATCH ()-[r]->() RETURN count(r) as count")
        ]

        print("\nEstatísticas do banco de dados:")
        for label, query in stats:
            result = session.run(query)
            count = result.single()["count"]
            print(f"Total de {label}: {count}")

    def close(self):
        if self.driver:
            self.driver.close()
            print("Conexão fechada.")

if __name__ == "__main__":
    neo4j_conn = Neo4jConnection()
    neo4j_conn.connect()
    neo4j_conn.import_and_relate_data('aipf-patrimonio_Igienizada.csv')
    neo4j_conn.close()
