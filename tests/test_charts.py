import pandas as pd
import streamlit as st

from components.charts import LABEL_COLOR, render_bar_chart, render_line_chart, render_scatter


def test_chart_renderers_use_high_contrast_labels(monkeypatch):
    figures = []
    monkeypatch.setattr(st, "plotly_chart", lambda figure, **kwargs: figures.append(figure))
    frame = pd.DataFrame(
        {
            "area": ["Kigali", "Huye"],
            "value": [20.0, 12.0],
            "group": ["Urban", "Rural"],
        }
    )

    render_bar_chart(frame, "area", "value", "Bar")
    render_line_chart(frame, "area", "value", "Line")
    render_scatter(frame, "area", "value", color_col="group", title="Scatter")

    assert len(figures) == 3
    for figure in figures:
        assert figure.layout.font.color == LABEL_COLOR
        assert figure.layout.xaxis.tickfont.color == LABEL_COLOR
        assert figure.layout.xaxis.title.font.color == LABEL_COLOR
        assert figure.layout.yaxis.tickfont.color == LABEL_COLOR
        assert figure.layout.yaxis.title.font.color == LABEL_COLOR

    assert figures[0].data[0].textfont.color == LABEL_COLOR