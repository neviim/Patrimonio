// Criação da raiz
MERGE (:CNCP {nome: 'Centro Nacional de Controle Patrimonial'});

LOAD CSV WITH HEADERS FROM 'file:///aipf-patrimonio_restructured.csv' AS row
WITH row
WHERE row.Patrimonio IS NOT NULL

// Prepara dados com fallback
WITH
  trim(row.Setor) AS setor,
  trim(row.Gestor) AS gestor,
  trim(row.SubSetor) AS subsetor,
  trim(row.Patrimonio) AS patrimonio,
  trim(row.Usuario) AS usuario,
  trim(row.Nome) AS nomeUsuario,
  trim(row.Local) AS local,
  trim(row.Locacao) AS locadora

// Criação de nós obrigatórios
MERGE (s:Setor {nome: setor})
MERGE (g:Gestor {nome: gestor})
MERGE (p:Patrimonio {id: patrimonio})
MERGE (l:Local {nome: local})
MERGE (cncp:CNCP {nome: 'Centro Nacional de Controle Patrimonial'})

// Relacionamentos obrigatórios
MERGE (cncp)-[:ABRANGE]->(s)
MERGE (g)-[:GERENCIA]->(s)
MERGE (s)-[:ALOCA]->(p)
MERGE (p)-[:ESTA_EM]->(l)

// SubSetor (se existir)
FOREACH (_ IN CASE WHEN subsetor <> '' THEN [1] ELSE [] END |
  MERGE (ss:SubSetor {nome: subsetor})
  MERGE (s)-[:CONTEM]->(ss)
  MERGE (ss)-[:ALOCA]->(p)
)

// Usuario (se existir)
FOREACH (_ IN CASE WHEN usuario <> '' THEN [1] ELSE [] END |
  MERGE (u:Usuario {login: usuario})
  SET u.nome = nomeUsuario
  MERGE (u)-[:USA]->(p)
)

// Locadora (se existir)
FOREACH (_ IN CASE WHEN locadora <> '' THEN [1] ELSE [] END |
  MERGE (loc:Locadora {nome: locadora})
  MERGE (p)-[:LOCADO_POR]->(loc)
);
