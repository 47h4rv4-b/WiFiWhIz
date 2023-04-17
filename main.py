from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from ensemble_espdata import get_accuracy_data
import plotly.graph_objects as go
import pandas as pd

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    accuracy_data = get_accuracy_data()

    accuracy_mean = accuracy_data['accuracy']
    accuracy_std = accuracy_data['potential_savings']
    
    # create a bar chart of the accuracy data
    data = [go.Bar(x=['Accuracy'], y=[accuracy_mean], error_y=dict(type='data', array=[accuracy_std]))]
    layout = go.Layout(title='Accuracy of Crowd Counting Model', yaxis_title='Accuracy')
    fig = go.Figure(data=data, layout=layout)
    plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    # render the HTML template with the plot
    html_content = """
    <html>
        <head>
            <title>Crowd Counting App</title>
        </head>
        <body>
            <h1>Crowd Counting App</h1>
            <p>This app shows the potential energy savings based on the accuracy of the crowd counting model.</p>
            {}
            <br>
            <form action="/accuracy" method="post">
                <button type="submit">Calculate Potential Energy Savings</button>
            </form>
        </body>
    </html>
    """.format(plot_div)
    
    return html_content


@app.post("/accuracy", response_class=HTMLResponse)
async def calculate_energy_savings(request: Request):
    accuracy_data = get_accuracy_data()
    accuracy_mean = accuracy_data['accuracy']
    
    # calculate the potential energy savings
    energy_savings = round((1 - accuracy_mean) * 100, 2)
    
    # render the HTML template with the energy savings
    html_content = """
    <html>
        <head>
            <title>Crowd Counting App</title>
        </head>
        <body>
            <h1>Crowd Counting App</h1>
            <p>The potential energy savings based on the accuracy of the crowd counting model is {}%.</p>
            <br>
            <form action="/" method="get">
                <button type="submit">Back to Home</button>
            </form>
        </body>
    </html>
    """.format(energy_savings)
    
    return html_content
