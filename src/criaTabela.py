import csv
from typing import List, Optional

class Gestor:
    def __init__(self, nome: str):
        self.nome = nome

    def __repr__(self):
        return f"Gestor(nome='{self.nome}')"


class Area:
    def __init__(self, nome: str, gestor: Optional[Gestor] = None):
        self.nome = nome
        self.gestor = gestor
        self.patrimonios = []

    def adicionar_patrimonio(self, patrimonio):
        self.patrimonios.append(patrimonio)

    def __repr__(self):
        return f"Area(nome='{self.nome}', gestor={self.gestor})"


class Patrimonio:
    def __init__(self, numero: str, status: str, usuario: Optional['Usuario'] = None):
        self.numero = numero
        self.status = status
        self.usuario = usuario

    def __repr__(self):
        return f"Patrimonio(numero='{self.numero}', status='{self.status}', usuario={self.usuario})"


class Usuario:
    def __init__(self, nome: str):
        self.nome = nome

    def __repr__(self):
        return f"Usuario(nome='{self.nome}')"


class SistemaPatrimonio:
    def __init__(self):
        self.areas = []
        self.gestores = []

    def adicionar_gestor(self, gestor: Gestor):
        self.gestores.append(gestor)

    def adicionar_area(self, area: Area):
        self.areas.append(area)

    def carregar_dados_csv(self, arquivo_csv: str):
        print("\n=== Carregando dados do CSV ===")
        with open(arquivo_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            current_area = None
            current_gestor = None

            # Pular as duas primeiras linhas (cabeçalho)
            next(reader)
            next(reader)

            for row in reader:
                # Ignorar linhas vazias
                if not any(row):
                    continue

                # Imprimir linha atual para debug
                print(f"Processando linha: {row}")

                # Identificar áreas e gestores
                if any(cell and 'Gestor' in str(cell) for cell in row):
                    for cell in row:
                        if cell and 'Gestor' in str(cell):
                            # Extrair nome da área e gestor
                            partes = str(cell).split('\n')
                            area_nome = partes[0].strip()
                            if len(partes) > 1 and 'Gestor' in partes[1]:
                                gestor_nome = partes[1].split(':')[1].strip()
                                current_gestor = Gestor(gestor_nome)
                                current_area = Area(area_nome, current_gestor)
                                self.adicionar_gestor(current_gestor)
                                self.adicionar_area(current_area)
                                print(f"Área encontrada: {area_nome} com gestor: {gestor_nome}")

                # Identificar patrimônios e usuários
                elif len(row) >= 5 and row[1]:  # Verifica se tem número de patrimônio
                    numero_patrimonio = row[1].strip()
                    usuario_nome = row[3].strip() if row[3] else "Sem Usuário"
                    status = row[5].strip() if len(row) > 5 and row[5] else "Desconhecido"

                    usuario = Usuario(usuario_nome)
                    patrimonio = Patrimonio(numero=numero_patrimonio, status=status, usuario=usuario)
                    print(f"Patrimônio encontrado: {patrimonio}")
                    
                    if current_area:
                        current_area.adicionar_patrimonio(patrimonio)
                        print(f"Patrimônio adicionado à área: {current_area.nome}")

    def exibir_tabela(self):
        print("\n=== Tabela de Patrimônios ===")
        print(f"Total de áreas carregadas: {len(self.areas)}")
        
        if not self.areas:
            print("Nenhuma área foi carregada!")
            return

        for area in self.areas:
            print(f"\nÁrea: {area.nome}")
            print(f"Gestor: {area.gestor.nome if area.gestor else 'N/A'}")
            print(f"Total de patrimônios: {len(area.patrimonios)}")
            for patrimonio in area.patrimonios:
                print(f"  - {patrimonio.numero} | {patrimonio.status} | {patrimonio.usuario.nome}")

        print("\n=== Tabela Formatada ===")
        print(f"{'Área':<30} {'Gestor':<20} {'Patrimônio':<15} {'Status':<15} {'Usuário':<30}")
        print("-" * 110)
        
        for area in self.areas:
            for patrimonio in area.patrimonios:
                print(f"{area.nome:<30} {area.gestor.nome if area.gestor else 'N/A':<20} {patrimonio.numero:<15} {patrimonio.status:<15} {patrimonio.usuario.nome:<30}")


# Execução do programa
if __name__ == "__main__":
    sistema = SistemaPatrimonio()
    sistema.carregar_dados_csv("./data/aipf-patrimonio_restructured.csv")
    sistema.exibir_tabela()