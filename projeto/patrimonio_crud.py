from neo4j import GraphDatabase
import pandas as pd
from typing import Dict, List, Optional, Union, Any


class PatrimonioCRUD:
    """
    Classe CRUD para gerenciamento de patrimônio no Neo4j.
    Implementa operações de Criação, Leitura, Atualização e Exclusão para o grafo de patrimônio.
    """
    
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "#neo4jcn*"):
        """
        Inicializa a conexão com o banco de dados Neo4j.
        
        Args:
            uri: URI do servidor Neo4j
            user: Nome de usuário para autenticação
            password: Senha para autenticação
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        
    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.driver:
            self.driver.close()
    
    def __enter__(self):
        """Permite usar a classe com o gerenciador de contexto 'with'."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fecha a conexão automaticamente ao sair do contexto 'with'."""
        self.close()

    # CREATE OPERATIONS
    
    def criar_patrimonio(self, patrimonio_id: str, setor: str, local: str, 
                        gestor: Optional[str] = None, subsetor: Optional[str] = None,
                        usuario_login: Optional[str] = None, usuario_nome: Optional[str] = None,
                        locadora: Optional[str] = None) -> bool:
        """
        Cria um novo registro de patrimônio com todos os relacionamentos.
        
        Args:
            patrimonio_id: ID único do patrimônio
            setor: Nome do setor
            local: Nome do local
            gestor: Nome do gestor (opcional)
            subsetor: Nome do subsetor (opcional)
            usuario_login: Login do usuário (opcional)
            usuario_nome: Nome do usuário (opcional)
            locadora: Nome da locadora (opcional)
            
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        with self.driver.session() as session:
            try:
                session.execute_write(
                    self._criar_estrutura,
                    setor=setor,
                    gestor=gestor if gestor else "",
                    subsetor=subsetor if subsetor else "",
                    patrimonio=patrimonio_id,
                    login=usuario_login if usuario_login else "",
                    nome=usuario_nome if usuario_nome else "",
                    local=local,
                    locadora=locadora if locadora else ""
                )
                return True
            except Exception as e:
                print(f"Erro ao criar patrimônio: {e}")
                return False
    
    def importar_csv(self, caminho_csv: str) -> int:
        """
        Importa dados de um arquivo CSV para o Neo4j.
        
        Args:
            caminho_csv: Caminho para o arquivo CSV
            
        Returns:
            int: Número de registros importados
        """
        try:
            df = pd.read_csv(caminho_csv).fillna('')
            count = 0
            
            with self.driver.session() as session:
                session.run("MERGE (:CNCP {nome: 'Canção Nova Cachoeira Paulista - Patrimonial'})")
                
                for _, row in df.iterrows():
                    setor = row['Setor'].strip()
                    gestor = row['Gestor'].strip()
                    subsetor = row['SubSetor'].strip()
                    patrimonio = str(row['Patrimonio']).strip()
                    login = row['Usuario'].strip()
                    nome = row['Nome'].strip()
                    local = row['Local'].strip()
                    locadora = row['Locacao'].strip()
                    
                    session.execute_write(
                        self._criar_estrutura,
                        setor, gestor, subsetor, patrimonio, login, nome, local, locadora
                    )
                    count += 1
            
            return count
        except Exception as e:
            print(f"Erro ao importar CSV: {e}")
            return 0
    
    @staticmethod
    def _criar_estrutura(tx, setor, gestor, subsetor, patrimonio, login, nome, local, locadora):
        """
        Método estático para criar a estrutura do grafo.
        
        Args:
            tx: Transação Neo4j
            setor: Nome do setor
            gestor: Nome do gestor
            subsetor: Nome do subsetor
            patrimonio: ID do patrimônio
            login: Login do usuário
            nome: Nome do usuário
            local: Nome do local
            locadora: Nome da locadora
        """
        # Criando o patrimônio e suas conexões principais
        tx.run("""
            MERGE (cncp:CNCP {nome: 'Centro Nacional de Controle Patrimonial'})
            MERGE (s:Setor {nome: $setor})
            MERGE (p:Patrimonio {id: $patrimonio})
            MERGE (l:Local {nome: $local})
            MERGE (cncp)-[:ABRANGE]->(s)
            MERGE (s)-[:ALOCA]->(p)
            MERGE (p)-[:ESTA_EM]->(l)
            """, setor=setor, patrimonio=patrimonio, local=local)
        
        # Criando o gestor se existir
        if gestor:
            tx.run("""
                MERGE (g:Gestor {nome: $gestor})
                MERGE (s:Setor {nome: $setor})
                MERGE (g)-[:GERENCIA]->(s)
                """, gestor=gestor, setor=setor)
        
        # Criando o subsetor se existir
        if subsetor:
            tx.run("""
                MERGE (ss:SubSetor {nome: $subsetor})
                MERGE (s:Setor {nome: $setor})
                MERGE (p:Patrimonio {id: $patrimonio})
                MERGE (s)-[:CONTEM]->(ss)
                MERGE (ss)-[:ALOCA]->(p)
                """, subsetor=subsetor, setor=setor, patrimonio=patrimonio)
        
        # Criando o usuário se existir
        if login and nome:
            tx.run("""
                MERGE (u:Usuario {login: $login})
                SET u.nome = $nome
                MERGE (p:Patrimonio {id: $patrimonio})
                MERGE (u)-[:USA]->(p)
                """, login=login, nome=nome, patrimonio=patrimonio)
        
        # Criando a locadora se existir
        if locadora:
            tx.run("""
                MERGE (loc:Locadora {nome: $locadora})
                MERGE (p:Patrimonio {id: $patrimonio})
                MERGE (p)-[:LOCADO_POR]->(loc)
                """, locadora=locadora, patrimonio=patrimonio)

    # READ OPERATIONS
    
    def buscar_patrimonio_por_id(self, patrimonio_id: str) -> Optional[Dict]:
        """
        Busca um patrimônio pelo ID.
        
        Args:
            patrimonio_id: ID do patrimônio
            
        Returns:
            Dict: Dados do patrimônio ou None se não encontrado
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Patrimonio {id: $patrimonio})
                OPTIONAL MATCH (s:Setor)-[:ALOCA]->(p)
                OPTIONAL MATCH (ss:SubSetor)-[:ALOCA]->(p)
                OPTIONAL MATCH (g:Gestor)-[:GERENCIA]->(s)
                OPTIONAL MATCH (p)-[:ESTA_EM]->(l:Local)
                OPTIONAL MATCH (u:Usuario)-[:USA]->(p)
                OPTIONAL MATCH (p)-[:LOCADO_POR]->(loc:Locadora)
                RETURN p.id AS patrimonio_id, 
                       s.nome AS setor,
                       ss.nome AS subsetor,
                       g.nome AS gestor,
                       l.nome AS local,
                       u.login AS usuario_login,
                       u.nome AS usuario_nome,
                       loc.nome AS locadora
            """, patrimonio=patrimonio_id)
            
            record = result.single()
            return dict(record) if record else None
    
    def listar_patrimonios(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Lista todos os patrimônios com paginação.
        
        Args:
            limit: Número máximo de registros
            offset: Posição inicial
            
        Returns:
            List[Dict]: Lista de patrimônios
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Patrimonio)
                OPTIONAL MATCH (s:Setor)-[:ALOCA]->(p)
                OPTIONAL MATCH (p)-[:ESTA_EM]->(l:Local)
                RETURN p.id AS patrimonio_id, s.nome AS setor, l.nome AS local
                ORDER BY p.id
                SKIP $offset
                LIMIT $limit
            """, offset=offset, limit=limit)
            
            return [dict(record) for record in result]

    def listar_patrimonios_por_local(self, local: str) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Patrimonio)-[:ESTA_EM]->(l:Local {nome: $local})
                OPTIONAL MATCH (s:Setor)-[:ALOCA]->(p)
                OPTIONAL MATCH (u:Usuario)-[:USA]->(p)
                RETURN p.id AS patrimonio_id, s.nome AS setor, l.nome AS local, u.login AS usuario_login, u.nome AS usuario_nome
            """, local=local)
            return [dict(record) for record in result]

    def buscar_patrimonios_por_setor(self, setor: str) -> List[Dict]:
        """
        Busca patrimônios por setor.
        
        Args:
            setor: Nome do setor
            
        Returns:
            List[Dict]: Lista de patrimônios no setor
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (s:Setor {nome: $setor})-[:ALOCA]->(p:Patrimonio)
                OPTIONAL MATCH (p)-[:ESTA_EM]->(l:Local)
                OPTIONAL MATCH (u:Usuario)-[:USA]->(p)
                RETURN p.id AS patrimonio_id, s.nome AS setor, l.nome AS local, u.login AS usuario_login, u.nome AS usuario_nome
            """, setor=setor)
            
            return [dict(record) for record in result]
    
    def buscar_patrimonios_por_usuario(self, login: str) -> List[Dict]:
        """
        Busca patrimônios associados a um usuário.
        
        Args:
            login: Login do usuário
            
        Returns:
            List[Dict]: Lista de patrimônios do usuário
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:Usuario {login: $login})-[:USA]->(p:Patrimonio)
                OPTIONAL MATCH (s:Setor)-[:ALOCA]->(p)
                OPTIONAL MATCH (p)-[:ESTA_EM]->(l:Local)
                RETURN p.id AS patrimonio_id, s.nome AS setor, l.nome AS local, u.nome AS usuario_nome
            """, login=login)
            
            return [dict(record) for record in result]
    
    # UPDATE OPERATIONS
    
    def atualizar_patrimonio(self, patrimonio_id: str, **kwargs) -> bool:
        """
        Atualiza informações de um patrimônio.
        
        Args:
            patrimonio_id: ID do patrimônio
            **kwargs: Atributos a serem atualizados (local, setor, gestor, etc.)
            
        Returns:
            bool: True se a atualização foi bem-sucedida
        """
        try:
            with self.driver.session() as session:
                # Atualizar local se fornecido
                if 'local' in kwargs:
                    session.run("""
                        MATCH (p:Patrimonio {id: $patrimonio})
                        OPTIONAL MATCH (p)-[r:ESTA_EM]->(:Local)
                        DELETE r
                        WITH p
                        MERGE (l:Local {nome: $local})
                        MERGE (p)-[:ESTA_EM]->(l)
                    """, patrimonio=patrimonio_id, local=kwargs['local'])
                
                # Atualizar setor se fornecido
                if 'setor' in kwargs:
                    session.run("""
                        MATCH (p:Patrimonio {id: $patrimonio})
                        OPTIONAL MATCH (old:Setor)-[r:ALOCA]->(p)
                        DELETE r
                        WITH p
                        MERGE (s:Setor {nome: $setor})
                        MERGE (s)-[:ALOCA]->(p)
                    """, patrimonio=patrimonio_id, setor=kwargs['setor'])
                
                # Atualizar gestor de setor se fornecido
                if 'setor' in kwargs and 'gestor' in kwargs:
                    session.run("""
                        MATCH (s:Setor {nome: $setor})
                        OPTIONAL MATCH (old:Gestor)-[r:GERENCIA]->(s)
                        DELETE r
                        WITH s
                        MERGE (g:Gestor {nome: $gestor})
                        MERGE (g)-[:GERENCIA]->(s)
                    """, setor=kwargs['setor'], gestor=kwargs['gestor'])
                
                # Atualizar subsetor se fornecido
                if 'subsetor' in kwargs:
                    session.run("""
                        MATCH (p:Patrimonio {id: $patrimonio})
                        OPTIONAL MATCH (:SubSetor)-[r:ALOCA]->(p)
                        DELETE r
                        WITH p
                        MATCH (s:Setor)-[:ALOCA]->(p)
                        MERGE (ss:SubSetor {nome: $subsetor})
                        MERGE (s)-[:CONTEM]->(ss)
                        MERGE (ss)-[:ALOCA]->(p)
                    """, patrimonio=patrimonio_id, subsetor=kwargs['subsetor'])
                
                # Atualizar usuário se fornecido
                if 'usuario_login' in kwargs:
                    session.run("""
                        MATCH (p:Patrimonio {id: $patrimonio})
                        OPTIONAL MATCH (:Usuario)-[r:USA]->(p)
                        DELETE r
                        WITH p
                        MERGE (u:Usuario {login: $login})
                        SET u.nome = $nome
                        MERGE (u)-[:USA]->(p)
                    """, patrimonio=patrimonio_id, 
                         login=kwargs['usuario_login'], 
                         nome=kwargs.get('usuario_nome', kwargs['usuario_login']))
                
                # Atualizar locadora se fornecida
                if 'locadora' in kwargs:
                    session.run("""
                        MATCH (p:Patrimonio {id: $patrimonio})
                        OPTIONAL MATCH (p)-[r:LOCADO_POR]->(:Locadora)
                        DELETE r
                        WITH p
                        MERGE (loc:Locadora {nome: $locadora})
                        MERGE (p)-[:LOCADO_POR]->(loc)
                    """, patrimonio=patrimonio_id, locadora=kwargs['locadora'])
                
                return True
        except Exception as e:
            print(f"Erro ao atualizar patrimônio: {e}")
            return False
    
    # DELETE OPERATIONS
    
    def remover_patrimonio(self, patrimonio_id: str) -> bool:
        """
        Remove um patrimônio e todas as suas relações.
        
        Args:
            patrimonio_id: ID do patrimônio
            
        Returns:
            bool: True se a remoção foi bem-sucedida
        """
        try:
            with self.driver.session() as session:
                session.run("""
                    MATCH (p:Patrimonio {id: $patrimonio})
                    OPTIONAL MATCH (p)-[r]-()
                    DELETE r, p
                """, patrimonio=patrimonio_id)
                return True
        except Exception as e:
            print(f"Erro ao remover patrimônio: {e}")
            return False
    
    def remover_relacao_usuario(self, patrimonio_id: str, usuario_login: str) -> bool:
        """
        Remove a relação entre um usuário e um patrimônio.
        
        Args:
            patrimonio_id: ID do patrimônio
            usuario_login: Login do usuário
            
        Returns:
            bool: True se a remoção foi bem-sucedida
        """
        try:
            with self.driver.session() as session:
                session.run("""
                    MATCH (u:Usuario {login: $login})-[r:USA]->(p:Patrimonio {id: $patrimonio})
                    DELETE r
                """, login=usuario_login, patrimonio=patrimonio_id)
                return True
        except Exception as e:
            print(f"Erro ao remover relação usuário-patrimônio: {e}")
            return False
    
    # UTILITIES
    
    def estatisticas(self) -> Dict[str, int]:
        """
        Retorna estatísticas do grafo.
        
        Returns:
            Dict[str, int]: Estatísticas do grafo
        """
        with self.driver.session() as session:
            stats = {}
            
            # Contagem de nós por tipo
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as tipo, count(n) as quantidade
            """)
            for record in result:
                stats[f"total_{record['tipo'].lower()}"] = record['quantidade']
            
            # Contagem de relacionamentos
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as tipo, count(r) as quantidade
            """)
            for record in result:
                stats[f"relacoes_{record['tipo'].lower()}"] = record['quantidade']
                
            return stats
    
    def limpar_banco(self) -> bool:
        """
        Remove todos os nós e relacionamentos do banco.
        CUIDADO: Isso apagará todos os dados!
        
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        try:
            with self.driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
                return True
        except Exception as e:
            print(f"Erro ao limpar banco: {e}")
            return False