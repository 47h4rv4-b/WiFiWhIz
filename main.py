from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from ensemble_espdata import get_accuracy_data, get_energy_consumption_data
import plotly.graph_objects as go
import pandas as pd

app = FastAPI()

accuracy_data = get_accuracy_data()
energy_consumption_data = get_energy_consumption_data()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    accuracy_mean = accuracy_data["mean"]
    accuracy_std = accuracy_data["std"]
    
    energy_consumption_mean = energy_consumption_data["mean"]
    energy_consumption_std = energy_consumption_data["std"]
    
    # create a bar chart of the accuracy data
    accuracy_fig = go.Figure()
    accuracy_fig.add_trace(go.Bar(x=['Accuracy'], y=[accuracy_mean], error_y=dict(type='data', array=[accuracy_std])))
    accuracy_fig.update_layout(title='Accuracy of Crowd Counting Model', yaxis_title='Accuracy')
    accuracy_plot_div = accuracy_fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    # create a bar chart of the energy consumption data
    energy_fig = go.Figure()
    energy_fig.add_trace(go.Bar(x=['Energy Consumption'], y=[energy_consumption_mean], error_y=dict(type='data', array=[energy_consumption_std])))
    energy_fig.update_layout(title='Energy Consumption of Manufacturing Facility', yaxis_title='Energy Consumption')
    energy_plot_div = energy_fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    # render the HTML template with the plots
    html_content = f"""
    <html>
        <head>
            <title>Crowd Counting App</title>
        </head>
        <body>
            <h1>Crowd Counting App</h1>
            <p>This app shows the potential energy savings based on the accuracy of the crowd counting model.</p>
            {accuracy_plot_div}
            <br>
            <p>This app also shows the energy consumption of a manufacturing facility.</p>
            {energy_plot_div}
            <br>
            <form action="/accuracy" method="post">
                <button type="submit">Calculate Potential Energy Savings</button>
            </form>
        </body>
    </html>
    """
    
    return html_content

@app.post("/accuracy", response_class=HTMLResponse)
async def calculate_energy_savings(request: Request):
    accuracy_mean = accuracy_data["mean"]
    
    # calculate the potential energy savings
    energy_savings = round((1 - accuracy_mean) * 100, 2)
    
    # render the HTML template with the energy savings
    html_content = f"""
    <html>
        <head>
            <title>Crowd Counting App</title>
        </head>
        <body>
            <h1>Crowd Counting App</h1>
            <p>The potential energy savings based on the accuracy of the crowd counting model is {energy_savings}%.</p>
            <br>
            <form action="/" method="get">
                <button type="submit">Back to Home</button>
            </form>
        </body>
    </html>
    """
    
    return html_content
