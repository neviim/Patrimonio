"""
Exemplos de uso da classe PatrimonioCRUD
"""
from patrimonio_crud import PatrimonioCRUD
import json


def exibir_resultado(titulo, dados):
    """Função auxiliar para exibir resultados de forma formatada"""
    print(f"\n{'='*50}")
    print(f"📌 {titulo}")
    print(f"{'='*50}")
    if isinstance(dados, list):
        for item in dados:
            print(json.dumps(item, indent=2, ensure_ascii=False))
    elif isinstance(dados, dict):
        print(json.dumps(dados, indent=2, ensure_ascii=False))
    else:
        print(dados)


def demonstrar_crud():
    """Demonstra as operações CRUD da classe PatrimonioCRUD"""
    
    # Usando a classe com gerenciador de contexto (with)
    with PatrimonioCRUD() as crud:
        # Limpar banco para demonstração (remover em ambiente de produção!)
        crud.limpar_banco()
        
        print("🚀 Iniciando demonstração do CRUD de Patrimônio")
        
        # CREATE - Criando patrimônios individuais
        exibir_resultado("Criando patrimônio", 
            crud.criar_patrimonio(
                patrimonio_id="PC001",
                setor="TI",
                gestor="Carlos Silva",
                subsetor="Infraestrutura",
                local="Sala 101",
                usuario_login="ana.santos",
                usuario_nome="Ana Santos",
                locadora="TechRent"
            )
        )
        
        # Criando mais alguns patrimônios para demonstração
        crud.criar_patrimonio(
            patrimonio_id="PC002", 
            setor="TI", 
            local="Sala 101", 
            usuario_login="joao.lima", 
            usuario_nome="João Lima"
        )
        
        crud.criar_patrimonio(
            patrimonio_id="IMP001", 
            setor="Administrativo", 
            gestor="Marina Oliveira", 
            local="Sala 205"
        )
        
        # READ - Buscando um patrimônio específico
        exibir_resultado("Buscando patrimônio por ID", 
            crud.buscar_patrimonio_por_id("PC001")
        )
        
        # READ - Listando todos os patrimônios
        exibir_resultado("Listando todos os patrimônios", 
            crud.listar_patrimonios()
        )
        
        # READ - Buscando por setor
        exibir_resultado("Buscando patrimônios por setor", 
            crud.buscar_patrimonios_por_setor("TI")
        )
        
        # READ - Buscando por usuário
        exibir_resultado("Buscando patrimônios por usuário", 
            crud.buscar_patrimonios_por_usuario("ana.santos")
        )
        
        # UPDATE - Atualizando informações de um patrimônio
        exibir_resultado("Atualizando local do patrimônio", 
            crud.atualizar_patrimonio("PC001", local="Sala 102")
        )
        
        # Verificando a atualização
        exibir_resultado("Verificando atualização", 
            crud.buscar_patrimonio_por_id("PC001")
        )
        
        # UPDATE - Atualizando múltiplas informações
        exibir_resultado("Atualizando múltiplas informações", 
            crud.atualizar_patrimonio(
                "PC001",
                setor="Desenvolvimento",
                gestor="Pedro Mendes",
                usuario_login="ana.santos",
                usuario_nome="Ana S. Santos"
            )
        )
        
        # Verificando as múltiplas atualizações
        exibir_resultado("Verificando múltiplas atualizações", 
            crud.buscar_patrimonio_por_id("PC001")
        )
        
        # DELETE - Removendo relação com usuário
        exibir_resultado("Removendo relação usuário-patrimônio", 
            crud.remover_relacao_usuario("PC001", "ana.santos")
        )
        
        # Verificando remoção da relação
        exibir_resultado("Verificando remoção da relação", 
            crud.buscar_patrimonio_por_id("PC001")
        )
        
        # DELETE - Removendo um patrimônio
        exibir_resultado("Removendo patrimônio", 
            crud.remover_patrimonio("IMP001")
        )
        
        # Verificando remoção de patrimônio
        exibir_resultado("Verificando remoção do patrimônio", 
            crud.buscar_patrimonio_por_id("IMP001")
        )
        
        # Estatísticas finais
        exibir_resultado("Estatísticas do grafo", 
            crud.estatisticas()
        )
        
        # Importando CSV (exemplo)
        print("\n📊 Importando CSV (simulado para o exemplo)...")
        print("Para importar um CSV real, use:")
        print("crud.importar_csv('./caminho/para/seu/arquivo.csv')")


def exemplo_importacao_csv():
    """Demonstra como importar um CSV"""
    with PatrimonioCRUD() as crud:
        # Exemplo de importação de CSV
        print("\n📄 Para importar um CSV, execute:")
        print("registros_importados = crud.importar_csv('./data/aipf-patrimonio_restructured.csv')")
        print("print(f'Foram importados {registros_importados} registros')")


if __name__ == "__main__":
    demonstrar_crud()
    exemplo_importacao_csv()