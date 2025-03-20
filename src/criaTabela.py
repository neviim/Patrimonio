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
        with open(arquivo_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            current_area = None
            current_gestor = None

            for row in reader:
                # Ignorar linhas vazias ou cabeçalhos
                if not any(row):
                    continue

                # Identificar áreas e gestores
                if "Gestor (a)" in row[0]:
                    area_nome = row[0].split("-")[0].strip()
                    gestor_nome = row[0].split(":")[1].strip()
                    current_gestor = Gestor(gestor_nome)
                    current_area = Area(area_nome, current_gestor)
                    self.adicionar_gestor(current_gestor)
                    self.adicionar_area(current_area)

                # Identificar patrimônios e usuários
                elif row[0].isdigit() or row[0].startswith("Patr.") or row[0].startswith("L0") or row[0].startswith("Ark"):
                    numero_patrimonio = row[0].strip()
                    usuario_nome = row[2].strip() if len(row) > 2 else "Sem Usuário"
                    status = row[4].strip() if len(row) > 4 else "Desconhecido"

                    usuario = Usuario(usuario_nome)
                    patrimonio = Patrimonio(numero=numero_patrimonio, status=status, usuario=usuario)
                    if current_area:
                        current_area.adicionar_patrimonio(patrimonio)

    def exibir_tabela(self):
        print(f"{'Área':<30} {'Gestor':<20} {'Patrimônio':<15} {'Status':<15} {'Usuário':<30}")
        print("-" * 110)
        for area in self.areas:
            for patrimonio in area.patrimonios:
                print(f"{area.nome:<30} {area.gestor.nome:<20} {patrimonio.numero:<15} {patrimonio.status:<15} {patrimonio.usuario.nome:<30}")


# Execução do programa
if __name__ == "__main__":
    sistema = SistemaPatrimonio()
    sistema.carregar_dados_csv("./data/aipf-patrimonio_restructured.csv")
    sistema.exibir_tabela()