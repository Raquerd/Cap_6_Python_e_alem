import json
import random
from datetime import datetime, timedelta

# Listas reais de exemplos de insumos, categorias, fabricantes e unidades de medida
insumos = [
    "Glifosato", "Atrazina", "Metolacloro", "Clorpirifós", "Mancozebe",
    "Fungicida Triazol", "Inseticida Lambda-Cialotrina", "Herbicida 2,4-D",
    "Adubo NPK 20-05-20", "Calcário Dolomítico", "Sulfato de Amônio",
    "Uréia", "Fertilizante MAP", "Superfosfato Simples", "Sementes de Soja",
    "Sementes de Milho Híbrido", "Sementes de Trigo", "Inoculante Bradyrhizobium"
]

categorias = [
    "Herbicida", "Inseticida", "Fungicida", "Fertilizante", "Corretivo de Solo", "Semente", "Inoculante"
]

fabricantes = [
    "Bayer", "Syngenta", "Basf", "Corteva", "FMC", "Yara", "Adama", "Nutrien"
]

unidades = ["Litro", "Quilograma", "Saco", "Unidade"]

# Função para gerar datas aleatórias
def random_date(start, end):
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

# Gerar a base de dados
dados = []
for _ in range(6500):
    insumo = random.choice(insumos)
    categoria = next((cat for cat in categorias if cat.lower() in insumo.lower()), random.choice(categorias))
    fabricante = random.choice(fabricantes)
    validade = random_date(datetime(2025, 1, 1), datetime(2030, 12, 31))
    quantidade = round(random.uniform(10, 1000), 2)
    unidade = random.choice(unidades)
    aquisicao = random_date(datetime(2020, 1, 1), datetime(2024, 12, 31))
    valor = round(random.uniform(50, 5000), 2)

    dados.append({
        "Insumo": insumo,
        "Categoria": categoria,
        "Fabricante": fabricante,
        "Data de validade": validade,
        "Quantidade em estoque": quantidade,
        "Unidade de medida": unidade,
        "Data de aquisição": aquisicao,
        "Valor unitário": valor
    })

# Salvar como JSON
caminho_arquivo = r"C:\Users\Davi\Documents\Projetos\FIAP\FASE 2\Cap7\base_insumos_agronomia.json"
with open(caminho_arquivo, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

caminho_arquivo