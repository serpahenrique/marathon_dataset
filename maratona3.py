import pandas as pd
import plotly.express as px


dados_maratona = pd.read_csv("marathon.csv")

coluna_tempo = "Time"
coluna_genero = "Gender"
coluna_pais = "Country"
coluna_data = "Date"
coluna_cidade = "City"
coluna_evento = "Event"

dados_maratona[coluna_tempo] = pd.to_timedelta(
    dados_maratona[coluna_tempo]
)

dados_maratona[coluna_data] = pd.to_datetime(
    dados_maratona[coluna_data],
    format="%d.%m.%Y"
)

dados_maratona["Year"] = (
    dados_maratona[coluna_data].dt.year
)

def obter_top_10_menores_tempos():

    top_10_menores_tempos = (
        dados_maratona
        .sort_values(by=coluna_tempo)
        .head(10)
    )

    return top_10_menores_tempos

def obter_top_10_masculino():

    dados_masculinos = dados_maratona[
        dados_maratona[coluna_genero]
        .str.upper()
        .isin(["MEN"])
    ]

    top_10_masculino = (
        dados_masculinos
        .sort_values(by=coluna_tempo)
        .head(10)
    )

    return top_10_masculino

def obter_top_10_feminino():

    dados_femininos = dados_maratona[
        dados_maratona[coluna_genero]
        .str.upper()
        .isin(["WOMEN"])
    ]

    top_10_feminino = (
        dados_femininos
        .sort_values(by=coluna_tempo)
        .head(10)
    )

    return top_10_feminino

def obter_media_por_quinquenio_e_genero():

    copia_dos_dados = dados_maratona.copy()

    copia_dos_dados["Quinquenio"] = (
        copia_dos_dados["Year"] // 5
    ) * 5

    media_por_quinquenio = (
        copia_dos_dados
        .groupby(
            ["Quinquenio", coluna_genero]
        )[coluna_tempo]
        .mean()
        .reset_index()
    )

    return media_por_quinquenio

def obter_top_5_paises_mais_rapidos():

    filtro_paises = ~dados_maratona[
        coluna_pais
    ].str.upper().isin(
        ["KEN", "ETH"]
    )

    dados_filtrados = dados_maratona[
        filtro_paises
    ]

    top_5_paises = (
        dados_filtrados
        .groupby(coluna_pais)[coluna_tempo]
        .min()
        .sort_values()
        .head(5)
        .reset_index()
    )

    return top_5_paises


def gerar_grafico_pizza_cidades():

    quantidade_por_cidade = (
        dados_maratona[coluna_cidade]
        .value_counts()
        .head(10)
        .reset_index()
    )

    quantidade_por_cidade.columns = [
        "Cidade",
        "Quantidade"
    ]

    grafico = px.pie(
        quantidade_por_cidade,
        names="Cidade",
        values="Quantidade",
        title="Top 10 Cidades com Mais Maratonas"
    )

    grafico.show()


def gerar_grafico_media_genero():

    media_genero = (
        dados_maratona
        .groupby(coluna_genero)[coluna_tempo]
        .mean()
        .reset_index()
    )

    media_genero["Tempo em Horas"] = (
        media_genero[coluna_tempo]
        .dt.total_seconds() / 3600
    )

    grafico = px.bar(
        media_genero,
        x=coluna_genero,
        y="Tempo em Horas",
        title="Média de Tempo por Gênero",
        text_auto=".2f"
    )

    grafico.show()



print("\nTOP 10 MENORES TEMPOS\n")
print(obter_top_10_menores_tempos())

print("\nTOP 10 MASCULINO\n")
print(obter_top_10_masculino())

print("\nTOP 10 FEMININO\n")
print(obter_top_10_feminino())

print("\nMÉDIA POR QUINQUÊNIO E GÊNERO\n")
print(obter_media_por_quinquenio_e_genero())

print("\nTOP 5 PAÍSES MAIS RÁPIDOS\n")
print(obter_top_5_paises_mais_rapidos())

gerar_grafico_pizza_cidades()

gerar_grafico_media_genero()