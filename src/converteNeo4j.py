import pandas as pd
import csv

def structure_data_for_neo4j():
    # Ler o arquivo CSV com parâmetros ajustados
    df = pd.read_csv(
        r".\data\aipf-patrimonio_restructured.csv",
        header=None,
        delimiter=',',
        quoting=csv.QUOTE_ALL,
        on_bad_lines='skip'
    )
    
    # Listas para armazenar os diferentes tipos de nós e relacionamentos
    current_department = ""
    current_manager = ""
    
    # Abrir arquivos para escrita
    with open(r".\data\aipf-patrimonio_neo4j_nodes.csv", 'w', newline='', encoding='utf-8') as nodes_file, \
         open(r".\data\aipf-patrimonio_neo4j_relationships.csv", 'w', newline='', encoding='utf-8') as rels_file:
        
        # Definir writers
        nodes_writer = csv.writer(nodes_file)
        rels_writer = csv.writer(rels_file)
        
        # Escrever cabeçalhos
        nodes_writer.writerow(['id', 'label', 'properties'])
        rels_writer.writerow(['start', 'end', 'type', 'properties'])
        
        # Processar cada linha do DataFrame
        for _, row in df.iterrows():
            # Verificar se é uma linha de departamento
            if pd.notna(row[0]) and isinstance(row[0], str) and 'Gestor' in str(row[0]):
                current_department = row[0].split('\n')[0].strip()
                # Extrair gestor se existir
                if '-Gestor' in row[0]:
                    current_manager = row[0].split(':')[1].strip()
                    # Adicionar gestor como usuário
                    nodes_writer.writerow([
                        f"user_{current_manager.replace(' ', '_')}",
                        'User',
                        f"{{name: '{current_manager}', role: 'Manager'}}"
                    ])
                    # Adicionar relacionamento gestor-departamento
                    rels_writer.writerow([
                        f"user_{current_manager.replace(' ', '_')}",
                        f"dept_{current_department.replace(' ', '_')}",
                        'MANAGES',
                        "{}"
                    ])
                
                # Adicionar departamento
                nodes_writer.writerow([
                    f"dept_{current_department.replace(' ', '_')}",
                    'Department',
                    f"{{name: '{current_department}'}}"
                ])
            
            # Processar ativos e usuários
            if pd.notna(row[1]) and pd.notna(row[3]):
                asset_id = str(row[1]).strip()
                user_name = str(row[3]).strip()
                asset_type = 'Alugado' if pd.notna(row[5]) and 'Alugado' in str(row[5]) else 'AIPF'
                
                # Adicionar ativo
                nodes_writer.writerow([
                    f"asset_{asset_id.replace(' ', '_')}",
                    'Asset',
                    f"{{id: '{asset_id}', type: '{asset_type}'}}"
                ])
                
                # Adicionar usuário
                nodes_writer.writerow([
                    f"user_{user_name.replace(' ', '_')}",
                    'User',
                    f"{{name: '{user_name}'}}"
                ])
                
                # Relacionamentos
                # Usuário -> Ativo
                rels_writer.writerow([
                    f"user_{user_name.replace(' ', '_')}",
                    f"asset_{asset_id.replace(' ', '_')}",
                    'USES',
                    "{}"
                ])
                
                # Departamento -> Ativo
                if current_department:
                    rels_writer.writerow([
                        f"dept_{current_department.replace(' ', '_')}",
                        f"asset_{asset_id.replace(' ', '_')}",
                        'OWNS',
                        "{}"
                    ])

def main():
    structure_data_for_neo4j()
    print("Arquivos gerados com sucesso: aipf-patrimonio_neo4j_nodes.csv e aipf-patrimonio_neo4j_relationships.csv")

if __name__ == "__main__":
    main()