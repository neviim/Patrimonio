from neo4j import GraphDatabase
import pandas as pd

class PatrimonioGraph:

    def __init__(self):
        self.uri = "bolt://localhost:7687"
        self.user = "neo4j"
        self.password = "#neo4jcn*"
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        if self.driver:
            self.driver.close()

    def importar_csv_para_neo4j(self, caminho_csv):
        df = pd.read_csv(caminho_csv).fillna('')

        with self.driver.session() as session:
            session.run("MERGE (:CNCP {nome: 'Centro Nacional de Controle Patrimonial'})")

            for _, row in df.iterrows():
                setor = row['Setor'].strip()
                gestor = row['Gestor'].strip()
                subsetor = row['SubSetor'].strip()
                patrimonio = str(row['Patrimonio']).strip()
                login = row['Usuario'].strip()
                nome = row['Nome'].strip()
                local = row['Local'].strip()
                locadora = row['Locacao'].strip()

                session.write_transaction(self._criar_estrutura, setor, gestor, subsetor,
                                          patrimonio, login, nome, local, locadora)

    @staticmethod
    def _criar_estrutura(tx, setor, gestor, subsetor, patrimonio, login, nome, local, locadora):
        tx.run("""
            MERGE (cncp:CNCP {nome: 'Centro Nacional de Controle Patrimonial'})
            MERGE (s:Setor {nome: $setor})
            MERGE (g:Gestor {nome: $gestor})
            MERGE (p:Patrimonio {id: $patrimonio})
            MERGE (l:Local {nome: $local})
            MERGE (g)-[:GERENCIA]->(s)
            MERGE (cncp)-[:ABRANGE]->(s)
            MERGE (s)-[:ALOCA]->(p)
            MERGE (p)-[:ESTA_EM]->(l)
            """, setor=setor, gestor=gestor, patrimonio=patrimonio, local=local)

        if subsetor:
            tx.run("""
                MERGE (ss:SubSetor {nome: $subsetor})
                MERGE (s:Setor {nome: $setor})
                MERGE (p:Patrimonio {id: $patrimonio})
                MERGE (s)-[:CONTEM]->(ss)
                MERGE (ss)-[:ALOCA]->(p)
                """, subsetor=subsetor, setor=setor, patrimonio=patrimonio)

        if login and nome:
            tx.run("""
                MERGE (u:Usuario {login: $login})
                SET u.nome = $nome
                MERGE (p:Patrimonio {id: $patrimonio})
                MERGE (u)-[:USA]->(p)
                """, login=login, nome=nome, patrimonio=patrimonio)

        if locadora:
            tx.run("""
                MERGE (loc:Locadora {nome: $locadora})
                MERGE (p:Patrimonio {id: $patrimonio})
                MERGE (p)-[:LOCADO_POR]->(loc)
                """, locadora=locadora, patrimonio=patrimonio)

    def testar_estrutura(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (cncp:CNCP)-[:ABRANGE]->(s:Setor)
                OPTIONAL MATCH (s)<-[:GERENCIA]-(g:Gestor)
                OPTIONAL MATCH (s)-[:ALOCA]->(p:Patrimonio)
                OPTIONAL MATCH (p)-[:ESTA_EM]->(l:Local)
                OPTIONAL MATCH (p)<-[:USA]-(u:Usuario)
                OPTIONAL MATCH (p)-[:LOCADO_POR]->(loc:Locadora)
                RETURN cncp.nome AS CNCP, s.nome AS Setor, g.nome AS Gestor,
                       p.id AS Patrimonio, l.nome AS Local, u.nome AS Usuario,
                       loc.nome AS Locadora
                LIMIT 10
            """)
            print("📊 Verificação de estrutura:")
            for row in result:
                print(dict(row))


if __name__ == "__main__":
    grafo = PatrimonioGraph()
    try:
        grafo.importar_csv_para_neo4j("./data/aipf-patrimonio_restructured.csv")
        grafo.testar_estrutura()
    finally:
        grafo.close()
