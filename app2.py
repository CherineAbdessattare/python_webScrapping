import csv
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State


with open('products.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]


brands = list(set([row['Brand'] for row in data]))


app = dash.Dash(__name__,external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'])

app.layout = html.Div(
    className='container',
    children=[
    html.H2('Jumia Smartphones :', className='display-4 mt-3 mb-5'),
    html.Label('Marque de smartphone:' , className='lead'),
    dcc.Dropdown(
        id='brand-dropdown',
        options=[{'label': brand, 'value': brand} for brand in brands],
        placeholder='Sélectionnez une marque',
    ),
    html.Label('Prix maximal:' , className='lead'),
    dcc.Input(
        id='max-price-input',
        type='number',
        placeholder='Entrez le prix maximal',
        className='form-control mb-3'
    ),
    html.Button('Rechercher', id='search-button', n_clicks=0, className='btn btn-info mb-5'),
    html.Table(id='results-table'),
])

@app.callback(
    Output('results-table', 'children'),
    Input('search-button', 'n_clicks'),
    State('brand-dropdown', 'value'),
    State('max-price-input', 'value')
)
def update_results_table(n_clicks, selected_brand, max_price):
    if n_clicks > 0 and selected_brand and max_price:
        max_price = float(max_price)
        filtered_data = [row for row in data if row['Brand'] == selected_brand and float(row['Price']) <= max_price]
        table_rows = []
        for row in filtered_data:
            table_rows.append(
                html.Tr([
                    html.Td(row['Brand']),
                    html.Td(row['Price']),
                    html.Td(row['Name']),
                    html.Td(html.Img(src=row['Image'], height=100, width=100)),
                    html.Td(html.A('Afficher les détails', href=row['Link'], target='_blank'))
                    
                ])
            )
        return html.Table(
            className='table',
            children=[
                html.Thead(
                    html.Tr([
                        html.Th('Marque'),
                        html.Th('Prix'),
                        html.Th('Nom'),
                        html.Th('Image'),
                        html.Th('Afficher les détails')
                    ])
                ),
                html.Tbody(table_rows)
            ]
        )
    else:
        return []

if __name__ == '__main__':
    app.run_server(debug=True)
