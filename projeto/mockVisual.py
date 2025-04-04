from neo4j import GraphDatabase
import matplotlib.pyplot as plt
import networkx as nx

class VisualizadorNeo4j:
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "#neo4jcn*"))

    def fechar(self):
        self.driver.close()

    def obter_relacionamentos(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a)-[r]->(b)
                RETURN DISTINCT labels(a)[0] AS from_label, type(r) AS rel, labels(b)[0] AS to_label
            """)
            return [(record["from_label"], record["to_label"], record["rel"]) for record in result]

    def desenhar_grafo(self, relacoes):
        G = nx.DiGraph()
        for de, para, rel in relacoes:
            G.add_edge(de, para, label=rel)

        plt.figure(figsize=(12, 9))
        pos = nx.spring_layout(G, k=0.8)
        nx.draw(G, pos, with_labels=True, node_size=3500, node_color='lightgreen',
                font_size=10, font_weight='bold', arrows=True)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
        plt.title("🔍 Modelo Real do Grafo Patrimonial (Neo4j)", fontsize=14)
        plt.axis('off')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    viz = VisualizadorNeo4j()
    try:
        relacoes = viz.obter_relacionamentos()
        viz.desenhar_grafo(relacoes)
    finally:
        viz.fechar()
