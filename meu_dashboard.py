import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="Barbie Beauty Analytics",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-color: #fff0f6;
        color: #5a1740;
    }

    section[data-testid="stSidebar"] {
        background-color: #ff69b4;
        border-right: 2px solid #ff1493;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .kpi-card {
        background: #ffffff;
        border: 2px solid #ffb6d9;
        border-left: 6px solid #ff1493;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 15px;
        box-shadow: 0 5px 15px rgba(255, 20, 147, 0.15);
    }

    .kpi-title {
        color: #c21870;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }

    .kpi-value {
        color: #8b0a50;
        font-size: 1.65rem;
        font-weight: 700;
    }

    .kpi-sub {
        color: #ff1493;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 4px;
    }

    hr {
        border-color: #ffb6d9;
    }

    button[data-baseweb="tab"] {
        color: #c21870;
        font-weight: 600;
    }

    button[aria-selected="true"] {
        color: #ff1493 !important;
        border-bottom-color: #ff1493 !important;
    }

    h1 {
        color: #ff1493 !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: #c21870 !important;
    }

    .stCaption {
        color: #a83b70 !important;
    }

    div[data-testid="stDataFrame"] {
        border: 2px solid #ffb6d9;
        border-radius: 10px;
    }

    .stDownloadButton button {
        background-color: #ff1493;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
    }

    .stDownloadButton button:hover {
        background-color: #db0a7a;
        color: white;
    }

    div[data-baseweb="select"] > div {
        background-color: #fff5fa;
        border-color: #ff9ccc;
    }

    div[data-baseweb="select"] span {
        color: #8b0a50;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def gerar_dados():

    np.random.seed(42)

    datas = pd.date_range(
        start="2023-01-01",
        end="2023-12-31",
        freq="D"
    )

    categorias = [
        "Batom",
        "Base",
        "Corretivo",
        "Blush",
        "Máscara de Cílios",
        "Paleta de Sombras"
    ]

    marcas = [
        "Maybelline",
        "MAC",
        "Ruby Rose",
        "O Boticário",
        "Natura",
        "Quem Disse, Berenice?"
    ]

    canais = [
        "Loja Física",
        "E-commerce",
        "Instagram",
        "Marketplace"
    ]

    produtos = [
        "Batom Matte",
        "Base Líquida",
        "Corretivo Cremoso",
        "Blush Compacto",
        "Máscara de Cílios",
        "Paleta de Sombras"
    ]

    dados = {
        "Data": np.random.choice(datas, 1200),

        "Produto": np.random.choice(
            produtos,
            1200
        ),

        "Categoria": np.random.choice(
            categorias,
            1200,
            p=[0.20, 0.20, 0.15, 0.15, 0.15, 0.15]
        ),

        "Marca": np.random.choice(
            marcas,
            1200
        ),

        "Canal": np.random.choice(
            canais,
            1200,
            p=[0.30, 0.35, 0.20, 0.15]
        ),

        "Valor": np.random.uniform(
            25,
            450,
            1200
        ).round(2),

        "Quantidade": np.random.randint(
            1,
            5,
            1200
        )
    }

    df = pd.DataFrame(dados)

    df["Mês"] = df["Data"].dt.strftime("%Y-%m")

    return df


df = gerar_dados()


st.sidebar.markdown("### 💄 Filtros de Beleza")
st.sidebar.caption(
    "Selecione os parâmetros para analisar as vendas de maquiagem:"
)


marcas_disponiveis = list(
    df["Marca"].unique()
)

filtro_marca = st.sidebar.multiselect(
    "Marca",
    options=marcas_disponiveis,
    default=marcas_disponiveis
)


categorias_disponiveis = list(
    df["Categoria"].unique()
)

filtro_categoria = st.sidebar.multiselect(
    "Categoria de Maquiagem",
    options=categorias_disponiveis,
    default=categorias_disponiveis
)


canais_disponiveis = list(
    df["Canal"].unique()
)

filtro_canal = st.sidebar.multiselect(
    "Canal de Venda",
    options=canais_disponiveis,
    default=canais_disponiveis
)


df_filtrado = df[
    (df["Marca"].isin(filtro_marca)) &
    (df["Categoria"].isin(filtro_categoria)) &
    (df["Canal"].isin(filtro_canal))
]


st.title("💄 Barbie Beauty Analytics")
st.caption(
    "Dashboard de Inteligência de Vendas e Desempenho do Mercado de Maquiagem"
)

st.markdown("---")


if df_filtrado.empty:

    st.warning(
        "Nenhuma venda encontrada com os filtros selecionados. "
        "Ajuste os filtros na barra lateral."
    )

    st.stop()


receita_total = df_filtrado["Valor"].sum()

total_transacoes = len(df_filtrado)

ticket_medio = (
    receita_total /
    total_transacoes
)

top_categoria = (
    df_filtrado["Categoria"]
    .value_counts()
    .index[0]
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💗 Receita Total</div>
        <div class="kpi-value">
            R$ {receita_total:,.2f}
        </div>
        <div class="kpi-sub">
            ● Vendas de Maquiagem
        </div>
    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💄 Total de Vendas</div>
        <div class="kpi-value">
            {total_transacoes:,}
        </div>
        <div class="kpi-sub">
            ● Pedidos Realizados
        </div>
    </div>
    """, unsafe_allow_html=True)


with c3:

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🎀 Ticket Médio</div>
        <div class="kpi-value">
            R$ {ticket_medio:,.2f}
        </div>
        <div class="kpi-sub">
            ● Valor Médio por Pedido
        </div>
    </div>
    """, unsafe_allow_html=True)


with c4:

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💋 Categoria Mais Vendida</div>
        <div class="kpi-value"
             style="font-size: 1.35rem;">
            {top_categoria}
        </div>
        <div class="kpi-sub">
            ● Maior Frequência
        </div>
    </div>
    """, unsafe_allow_html=True)


tab_graficos, tab_marcas, tab_dados = st.tabs([
    "💗 Evolução de Vendas",
    "💄 Marcas e Categorias",
    "👜 Registros de Vendas"
])


with tab_graficos:

    col_esq, col_dir = st.columns([1.5, 1])


    with col_esq:

        st.subheader("💗 Receita Mensal")

        df_mensal = (
            df_filtrado
            .groupby(
                "Mês",
                as_index=False
            )["Valor"]
            .sum()
        )


        grafico_area = alt.Chart(
            df_mensal
        ).mark_area(
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    alt.GradientStop(
                        color="#ff1493",
                        offset=0
                    ),
                    alt.GradientStop(
                        color="rgba(255,105,180,0.08)",
                        offset=1
                    )
                ],
                x1=1,
                x2=1,
                y1=1,
                y2=0
            ),
            line={
                "color": "#ff1493",
                "size": 2.5
            }
        ).encode(

            x=alt.X(
                "Mês:N",
                title=None,
                axis=alt.Axis(
                    labelColor="#a83b70",
                    labelAngle=0
                )
            ),

            y=alt.Y(
                "Valor:Q",
                title="Receita (R$)",
                axis=alt.Axis(
                    labelColor="#a83b70",
                    gridColor="#ffc4df",
                    format="~s"
                )
            ),

            tooltip=[
                alt.Tooltip("Mês:N"),
                alt.Tooltip(
                    "Valor:Q",
                    format=",.2f",
                    title="Receita (R$)"
                )
            ]

        ).properties(
            height=320
        ).configure_view(
            strokeOpacity=0
        ).configure(
            background="transparent"
        )


        st.altair_chart(
            grafico_area,
            use_container_width=True
        )


    with col_dir:

        st.subheader("💋 Vendas por Categoria")

        df_cat = (
            df_filtrado
            .groupby(
                "Categoria",
                as_index=False
            )["Valor"]
            .sum()
            .sort_values(
                by="Valor",
                ascending=False
            )
        )


        grafico_barras = alt.Chart(
            df_cat
        ).mark_bar(
            cornerRadiusTopRight=8,
            cornerRadiusBottomRight=8,
            color="#ff1493"
        ).encode(

            x=alt.X(
                "Valor:Q",
                title=None,
                axis=alt.Axis(
                    labelColor="#a83b70",
                    gridColor="#ffc4df",
                    format="~s"
                )
            ),

            y=alt.Y(
                "Categoria:N",
                sort="-x",
                title=None,
                axis=alt.Axis(
                    labelColor="#8b0a50"
                )
            ),

            tooltip=[
                alt.Tooltip("Categoria:N"),
                alt.Tooltip(
                    "Valor:Q",
                    format=",.2f",
                    title="Total (R$)"
                )
            ]

        ).properties(
            height=320
        ).configure_view(
            strokeOpacity=0
        ).configure(
            background="transparent"
        )


        st.altair_chart(
            grafico_barras,
            use_container_width=True
        )


with tab_marcas:

    st.subheader("💄 Receita por Marca")

    df_marcas = (
        df_filtrado
        .groupby(
            "Marca",
            as_index=False
        )["Valor"]
        .sum()
        .sort_values(
            by="Valor",
            ascending=False
        )
    )


    grafico_marcas = alt.Chart(
        df_marcas
    ).mark_bar(
        cornerRadiusTopLeft=8,
        cornerRadiusTopRight=8,
        color="#ff69b4"
    ).encode(

        x=alt.X(
            "Marca:N",
            title=None,
            axis=alt.Axis(
                labelColor="#8b0a50",
                labelAngle=-25
            )
        ),

        y=alt.Y(
            "Valor:Q",
            title="Receita (R$)",
            axis=alt.Axis(
                labelColor="#a83b70",
                gridColor="#ffc4df",
                format="~s"
            )
        ),

        tooltip=[
            alt.Tooltip("Marca:N"),
            alt.Tooltip(
                "Valor:Q",
                format=",.2f",
                title="Receita (R$)"
            )
        ]

    ).properties(
        height=350
    ).configure_view(
        strokeOpacity=0
    ).configure(
        background="transparent"
    )


    st.altair_chart(
        grafico_marcas,
        use_container_width=True
    )


with tab_dados:

    st.subheader("👜 Registros de Vendas")

    st.dataframe(
        df_filtrado,
        use_container_width=True
    )


    csv = (
        df_filtrado
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        label="🎀 Baixar Vendas em CSV",
        data=csv,
        file_name="vendas_maquiagem_barbie.csv",
        mime="text/csv"
    )
