from neo4j import GraphDatabase
import sys

def test_neo4j_connection(uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*"):
    """
    Teste detalhado de conexão com o Neo4j.
    """
    print(f"Tentando conectar ao Neo4j em {uri}")
    print(f"Usuário: {user}")

    try:
        # Configurações de conexão mais detalhadas
        driver = GraphDatabase.driver(
            uri,
            auth=(user, password),
            connection_timeout=30,  # Timeout de 30 segundos para estabelecer a conexão
            max_connection_lifetime=3600,  # Máximo de 1 hora de vida útil da conexão
            connection_acquisition_timeout=5  # Timeout de aquisição de conexão
        )

        # Verifica a conectividade
        with driver.session() as session:
            # Tenta executar um comando simples
            result = session.run("RETURN 1 AS test")
            record = result.single()

            if record and record['test'] == 1:
                print("✅ Conexão estabelecida com sucesso!")
                print("Detalhes da conexão:")
                print(f"URI: {uri}")
                print(f"Driver: {driver}")

                # Tentativa de obter informações do servidor
                try:
                    server_info = driver.get_server_info()
                    print(f"Versão do Neo4j: {server_info.agent.split('/')[-1]}")  # Extrai a versão do agente
                except Exception as e:
                    print("❌ Não foi possível obter a versão do Neo4j.")
                    print(f"Detalhes: {str(e)}")

            else:
                print("❌ Falha ao executar comando de teste")

        driver.close()

    except Exception as e:
        print("❌ Erro na conexão:")
        print(f"Tipo de erro: {type(e).__name__}")
        print(f"Detalhes do erro: {str(e)}")

        # Diagnóstico adicional
        print("\nPossíveis causas:")
        print("1. Verifique se o Neo4j está rodando.")
        print("2. Confirme as credenciais de conexão.")
        print("3. Verifique se a porta está correta.")
        print("4. Verifique se o firewall está bloqueando.")

        # Sugestões específicas com base no erro
        if "authentication" in str(e).lower():
            print("\n⚠️ AVISO: Possível problema de autenticação!")
            print("- Verifique se a senha está correta.")
            print("- Certifique-se de que o usuário tem permissões adequadas.")
            print("- Se necessário, redefina a senha do usuário no Neo4j Browser.")

        if "connection refused" in str(e).lower():
            print("\n⚠️ AVISO: Conexão recusada!")
            print("- Verifique se o serviço Neo4j está realmente rodando.")
            print("- Confirme se a porta configurada (7687) está correta.")
            print("- Certifique-se de que o Neo4j está ouvindo em 'localhost'.")

if __name__ == "__main__":
    # Permite passar parâmetros de conexão via linha de comando
    import sys

    # Valores padrão
    uri = "bolt://localhost:7687"
    user = "neo4j"  # Alterado para o usuário correto
    password = "#neo4jcn*"  # Senha fornecida

    # Sobrescreve os valores padrão se forem fornecidos via linha de comando
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    if len(sys.argv) > 2:
        user = sys.argv[2]
    if len(sys.argv) > 3:
        password = sys.argv[3]

    # Executa o teste de conexão
    test_neo4j_connection(uri, user, password)