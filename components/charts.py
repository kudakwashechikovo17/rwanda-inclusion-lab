import plotly.express as px
import streamlit as st


DEFAULT_COLORS = ["#0B2545", "#13315C", "#00C896", "#6EC3A3", "#7BC8F6"]
LABEL_COLOR = "#263238"


def _set_readable_labels(fig):
    fig.update_layout(
        font=dict(color=LABEL_COLOR, size=14),
        legend=dict(font=dict(color=LABEL_COLOR)),
        coloraxis_colorbar=dict(
            tickfont=dict(color=LABEL_COLOR),
            title_font=dict(color=LABEL_COLOR),
        ),
    )
    fig.update_xaxes(
        tickfont=dict(color=LABEL_COLOR),
        title_font=dict(color=LABEL_COLOR),
    )
    fig.update_yaxes(
        tickfont=dict(color=LABEL_COLOR),
        title_font=dict(color=LABEL_COLOR),
    )
    return fig


def render_bar_chart(df, x_col, y_col, title, x_title=None, y_title=None):
    if df is None or df.empty:
        st.info("No comparison data available for the selected filter set.")
        return

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color_discrete_sequence=["#00C896"],
        title=title,
        text=y_col,
    )
    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        textfont=dict(color=LABEL_COLOR),
    )
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_x=0.05,
        height=420,
        margin=dict(l=20, r=20, t=50, b=30),
        xaxis_title=x_title or x_col,
        yaxis_title=y_title or y_col,
    )
    _set_readable_labels(fig)
    st.plotly_chart(fig, use_container_width=True)


def render_line_chart(df, x_col, y_col, title):
    if df is None or df.empty:
        st.info("No trend data is available for this indicator.")
        return
    fig = px.line(df, x=x_col, y=y_col, markers=True, color_discrete_sequence=["#13315C"])
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=title,
        title_x=0.05,
        height=360,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    _set_readable_labels(fig)
    st.plotly_chart(fig, use_container_width=True)


def render_scatter(df, x_col, y_col, color_col=None, title="Comparison"):
    if df is None or df.empty:
        st.info("No scatter plot data is available.")
        return
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col if color_col else None, title=title)
    fig.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    _set_readable_labels(fig)
    st.plotly_chart(fig, use_container_width=True)
