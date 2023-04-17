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
    accuracy_fig.add_trace(
        go.Bar(
            x=["Accuracy"],
            y=[accuracy_mean],
            error_y=dict(type="data", array=[accuracy_std]),
        )
    )
    accuracy_fig.update_layout(
        title="Accuracy of Crowd Counting Model", yaxis_title="Accuracy"
    )
    accuracy_plot_div = accuracy_fig.to_html(full_html=False, include_plotlyjs="cdn")

    # create a bar chart of the energy consumption data
    energy_fig = go.Figure()
    energy_fig.add_trace(
        go.Bar(
            x=["Energy Consumption"],
            y=[energy_consumption_mean],
            error_y=dict(type="data", array=[energy_consumption_std]),
        )
    )
    energy_fig.update_layout(
        title="Energy Consumption of Manufacturing Facility",
        yaxis_title="Energy Consumption",
    )
    energy_plot_div = energy_fig.to_html(full_html=False, include_plotlyjs="cdn")

    # render the HTML template with the plots
    html_content = f"""
    <html>
        <head>
            <title>Crowd Counting App</title>
            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.6.0/css/bootstrap.min.css" integrity="sha512-QBfh6l0eIgucU6VRsUfaXT4Zp7KjfyO9O1bwhOr4SLWEyV3Q2jK8upay7LdSv3q3g2i1/XVo8Wd13cBv/r5P5w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
            <!-- Custom CSS -->
            <style>
                body {{
                    padding: 2rem;
                }}
                h1 {{
                    margin-top: 2rem;
                    margin-bottom: 2rem;
                }}
                .plot-div {{
                    margin-top: 2rem;
                }}
                .form-button {{
                    margin-top: 2rem;
                }}
                .form-button button {{
                    width: 100%;
                    font-size: 1.2rem;
                }}
                .form-back {{
                    margin-top: 2rem;
                }}
                .form-back button {{
                    width: 100%;
                    font-size: 1.2rem;
                }}
            </style>
        </head>
        <body>
            <h1 class="text-center">Crowd Counting App</h1>
            <p class="text-center">This app shows the potential energy savings based on the accuracy of the crowd counting model.</p>
            <div class="row justify-content-center plot-div">
                <div class="col-md-6 col-lg-4">
                    {accuracy_plot_div}
                </div>
            </div>
            <p class="text-center">This app also shows the energy consumption of a manufacturing facility.</p>
            <div class="row justify-content-center plot-div">
                <div class="col-md-6 col-lg-4">
                    {energy_plot_div}
                </div>
            </div>
            <br>
            <div class="text-center">
                <form action="/accuracy" method="post">
                    <button type="submit" class="btn btn-primary btn-lg">Calculate Potential Energy Savings</button>
                </form>
            </div>
        </body>
        </html>
        """


    return html_content


@app.post("/accuracy", response_class=HTMLResponse)
async def calculate_energy_savings(request: Request):
    accuracy_mean = accuracy_data["mean"]

    # calculate the potential energy savings based on the accuracy of the crowd counting model
    # set the noise reduction factor to 0.76
    noise_reduction_factor = 0.76
    
    # calculate the potential energy savings
    energy_savings = -((1 - (accuracy_mean * (1 - noise_reduction_factor))))  


    
    # render the HTML template with the energy savings
    html_content = f"""
    <html>
        <head>
            <title>Crowd Counting App</title>
            <style>
                body {{
                    background-color: #F5F5F5;
                    font-family: Arial, sans-serif;
                }}
                h1 {{
                    text-align: center;
                    color: #333333;
                    margin-top: 30px;
                }}
                p {{
                    text-align: center;
                    color: #555555;
                    font-size: 18px;
                    margin-top: 10px;
                }}
                button {{
                    background-color: #3366CC;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                    font-size: 16px;
                    margin-top: 20px;
                    cursor: pointer;
                }}
                button:hover {{
                    background-color: #265BA3;
                }}
            </style>
        </head>
        <body>
            <h1>Crowd Counting App</h1>
            <p>The potential energy savings based on the accuracy of the crowd counting model is {energy_savings}%.</p>
            <form action="/" method="get">
                <button type="submit">Back to Home</button>
            </form>
        </body>
    </html>
    """
    
    return html_content
