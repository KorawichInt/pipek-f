import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/image-dashboard")

image_result_interval = dcc.Interval(
    id="image-result-interval",
    interval=1000,  # in milliseconds
    n_intervals=0,
)


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(["Food Dashboard"]),
                        html.Div(id="header"),
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "height": "100%",
                        "margin": "20px",
                    }
                
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(["Image Ids"]),
                        html.H5(id="upload-image-ids"),
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "alignItems": "left",
                        "height": "100%",
                        "margin": "10px",
                    }
                
                ),
                
            ]
        ),

        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),

        dbc.Row(
            [
                dbc.Row(
                    [
                        html.H2(["Image Results"]),
                        html.Div(id="image-results"),   # id
                        # html.Div(id="image-results"),   # type
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "alignItems": "left",
                        "height": "100%",
                        "margin": "10px",
                    }
                ),
            
                dbc.Row(
                    [
                        html.H2(["Recommendation"]),
                        # html.Div(id="image-results"),   # recommend
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "alignItems": "left",
                        "height": "100%",
                        "margin": "10px",
                    }
                ),
            ]
        ),
        dbc.Row(
                    [
                        html.Div(id="upload-status"),
                    ],
                    style={
                        "margin-left": "10px",
                    }
                ),
        image_result_interval,
        dcc.Store(id="image-ids"),
    ],
)
