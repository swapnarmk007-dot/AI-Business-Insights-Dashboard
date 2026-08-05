import pandas as pd
import plotly.express as px


def create_feature_importance(model, feature_names):

    # Check if model supports feature importance
    if not hasattr(model, "feature_importances_"):
        return None

    importance = pd.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_
    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    ).head(15)

    fig = px.bar(
        importance,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top 15 Important Features",
        color="Importance"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        height=600
    )

    return fig.to_html(full_html=False)