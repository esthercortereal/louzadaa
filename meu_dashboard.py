import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="Barbie Analytics Hub",
    page_icon="🎀",
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
        font-weight: 600;
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
    datas = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    categorias = ["Consoles", "Jogos Físicos", "Acessórios", "Game Pass", "Hardware PC"]
    plataformas = ["Xbox Series X|S", "PC Game Pass", "Xbox Cloud Gaming"]

    dados = {
        "Data": np.random.choice(datas, 1200),
        "Categoria": np.random.choice(
            categorias,
            1200,
            p=[0.15, 0.30, 0.20, 0.25, 0.10]
        ),
        "Plataforma": np.random.choice(
            plataformas,
            1200,
            p=[0.50, 0.30, 0.20]
        ),
        "Valor": np.random.uniform(40, 4200, 1200).round(2),
        "Quantidade": np.random.randint(1, 4, 1200)
    }

    df = pd.DataFrame(dados)
    df["Mês"] = df["Data"].dt.strftime("%Y-%m")

    return df


df = gerar_dados()

st.sidebar.markdown("### 🎀 Filtros Barbie")
st.sidebar.caption("Selecione os parâmetros para recalcular os indicadores:")

plataformas_disponiveis = list(df["Plataforma"].unique())

filtro_plataforma = st.sidebar.multiselect(
    "Plataforma",
    options=plataformas_disponiveis,
    default=plataformas_disponiveis
)

categorias_disponiveis = list(df["Categoria"].unique())

filtro_categoria = st.sidebar.multiselect(
    "Categoria de Produto",
    options=categorias_disponiveis,
    default=categorias_disponiveis
)

df_filtrado = df[
    (df["Plataforma"].isin(filtro_plataforma)) &
    (df["Categoria"].isin(filtro_categoria))
]

st.title("🎀 Barbie Global Sales & Subscriptions")
st.caption("Dashboard de Inteligência Operacional e Desempenho do Ecossistema de Jogos")
st.markdown("---")

if df_filtrado.empty:
    st.warning(
        "Nenhum registro encontrado com os filtros selecionados. "
        "Por favor, ajuste as opções na barra lateral."
    )
    st.stop()

receita_total = df_filtrado["Valor"].sum()
total_transacoes = len(df_filtrado)
ticket_medio = receita_total / total_transacoes
top_categoria = df_filtrado["Categoria"].value_counts().index[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💗 Receita Acumulada</div>
        <div class="kpi-value">R$ {receita_total:,.2f}</div>
        <div class="kpi-sub">● Vendas Brutas</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🎀 Volume de Pedidos</div>
        <div class="kpi-value">{total_transacoes:,}</div>
        <div class="kpi-sub">● Transações Processadas</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💄 Ticket Médio</div>
        <div class="kpi-value">R$ {ticket_medio:,.2f}</div>
        <div class="kpi-sub">● Valor Médio/Pedido</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">👛 Categoria Líder</div>
        <div class="kpi-value" style="font-size: 1.35rem;">{top_categoria}</div>
        <div class="kpi-sub">● Maior Frequência</div>
    </div>
    """, unsafe_allow_html=True)


tab_graficos, tab_detalhes, tab_dados = st.tabs([
    "🎀 Evolução e Segmentação",
    "💗 Repartição por Plataforma",
    "👜 Registros Brutos"
])


with tab_graficos:

    col_esq, col_dir = st.columns([1.5, 1])

    with col_esq:

        st.subheader("💗 Receita Mensal Consolidada")

        df_mensal = df_filtrado.groupby(
            "Mês",
            as_index=False
        )["Valor"].sum()

        grafico_area = alt.Chart(df_mensal).mark_area(
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    alt.GradientStop(
                        color="#ff1493",
                        offset=0
                    ),
                    alt.GradientStop(
                        color="rgba(255, 105, 180, 0.08)",
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

        st.subheader("🎀 Receita por Categoria")

        df_cat = df_filtrado.groupby(
            "Categoria",
            as_index=False
        )["Valor"].sum().sort_values(
            by="Valor",
            ascending=False
        )

        grafico_barras = alt.Chart(df_cat).mark_bar(
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


with tab_detalhes:

    st.subheader("💄 Desempenho por Meio de Acesso")

    df_plat = df_filtrado.groupby(
        "Plataforma",
        as_index=False
    )["Valor"].sum()

    grafico_plat = alt.Chart(df_plat).mark_bar(
        cornerRadiusTopLeft=8,
        cornerRadiusTopRight=8,
        color="#ff69b4"
    ).encode(
        x=alt.X(
            "Plataforma:N",
            title=None,
            axis=alt.Axis(
                labelColor="#8b0a50",
                labelAngle=0
            )
        ),
        y=alt.Y(
            "Valor:Q",
            title="Total de Vendas (R$)",
            axis=alt.Axis(
                labelColor="#a83b70",
                gridColor="#ffc4df",
                format="~s"
            )
        ),
        tooltip=[
            alt.Tooltip("Plataforma:N"),
            alt.Tooltip(
                "Valor:Q",
                format=",.2f"
            )
        ]
    ).properties(
        height=300
    ).configure_view(
        strokeOpacity=0
    ).configure(
        background="transparent"
    )

    st.altair_chart(
        grafico_plat,
        use_container_width=True
    )


with tab_dados:

    st.subheader("👜 Base Filtrada")

    st.dataframe(
        df_filtrado,
        use_container_width=True
    )

    csv = df_filtrado.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="🎀 Descarregar Recorte em CSV",
        data=csv,
        file_name="vendas_barbie_filtradas.csv",
        mime="text/csv"
    )
