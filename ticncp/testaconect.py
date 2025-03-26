from neo4j import GraphDatabase
import sys

def test_neo4j_connection(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*"):
    """
    Teste detalhado de conexão com o Neo4j
    """
    print(f"Tentando conectar ao Neo4j em {uri}")
    print(f"Usuário: {user}")
    
    try:
        # Configurações de conexão mais detalhadas
        driver = GraphDatabase.driver(
            uri, 
            auth=(user, password),
            connection_timeout=5,  # Timeout de 5 segundos
            max_connection_lifetime=3600,  # Máximo de 1 hora de conexão
            connection_acquisition_timeout=2  # Timeout de aquisição de conexão
        )
        
        # Verifica a conectividade
        with driver.session() as session:
            # Tenta executar um comando simples
            result = session.run("RETURN 1 as test")
            record = result.single()
            
            if record and record['test'] == 1:
                print("✅ Conexão estabelecida com sucesso!")
                print("Detalhes da conexão:")
                print(f"URI: {uri}")
                print(f"Driver: {driver}")
                
                # Informações adicionais sobre o servidor
                server_info = driver.get_server_info()
                print(f"Versão do Neo4j: {server_info.version}")
            else:
                print("❌ Falha ao executar comando de teste")
        
        driver.close()
    
    except Exception as e:
        print("❌ Erro na conexão:")
        print(f"Tipo de erro: {type(e).__name__}")
        print(f"Detalhes do erro: {str(e)}")
        
        # Diagnóstico adicional
        print("\nPossíveis causas:")
        print("1. Verifique se o Neo4j está rodando")
        print("2. Confirme as credenciais de conexão")
        print("3. Verifique se a porta está correta")
        print("4. Verifique se o firewall está bloqueando")
        
        # Algumas sugestões específicas
        if "authentication" in str(e).lower():
            print("\n⚠️ AVISO: Possível problema de autenticação!")
            print("- Verifique se a senha está correta")
            print("- Verifique se o usuário tem permissões")
        
        if "connection refused" in str(e).lower():
            print("\n⚠️ AVISO: Conexão recusada!")
            print("- Verifique se o Neo4j está realmente rodando")
            print("- Verifique a porta de conexão")

if __name__ == "__main__":
    # Permite passar parâmetros de conexão via linha de comando
    import sys
    
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "#neo4jcn*"
    
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    if len(sys.argv) > 2:
        user = sys.argv[2]
    if len(sys.argv) > 3:
        password = sys.argv[3]
    
    test_neo4j_connection(uri, user, password)