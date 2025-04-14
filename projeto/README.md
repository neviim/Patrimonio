# Atualiza

## Exemplo de JSON para atualizar o patrimônio PC001:

{
  "patrimonio_id": "PC001",
  "local": "Sala de Reunião 3",
  "setor": "TI",
  "gestor": "João da Silva",
  "subsetor": "Infraestrutura",
  "usuario_login": "jsilva",
  "usuario_nome": "João da Silva",
  "locadora": "Locadora XYZ"
}

Esse JSON:
    - Move o patrimônio PC001 para uma nova sala
    - Atualiza o setor e subsetor
    - Define um novo gestor
    - Atualiza o usuário vinculado
    - Define ou altera a locadora

Pode salvar esse conteúdo como [atualizacao_pc001.json] e executar:


# Como utilizar:
python atualiza.py ./data/atualizacao_pc001.json


### LIsta patrimonio por Locais

# python inserir_consultar_patrimonio.py local "Sala 101"
