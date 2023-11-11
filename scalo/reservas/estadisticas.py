
from django.urls import reverse
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from datetime import datetime
import locale
from django_plotly_dash import DjangoDash
from reservas.models import Predios,Deportes,Canchas,Reservas
from django.db.models import Sum, Count

locale.setlocale(locale.LC_TIME, 'es_ES.utf-8')
app = DjangoDash('dash_example')

app.css.append_css({
    "external_url": "scalo/reservas/static/css/style.css"  # Ajusta la ruta según sea necesario
})

app.layout = html.Div([ dcc.Loading(
            id="loading-1",
            type="graph",
            children=html.Div([
    html.H1("Ventas por categoría", style={
            'padding-top': '1.125rem',
            'padding-bottom': '1rem',
            'padding-left': '2%',
            'font-size': '40px',
            'font-family': '"Lexend", sans-serif',
            'font-weight': 'bolder',
            'color': '#042F2F',
        }),
    html.Br(),
    html.Div(
        [
        html.Div([
            html.Div([
                html.H1("Reservas por cancha", style={
                    'padding-top': '1.125rem',
                    'padding-bottom': '1.125rem',
                    'font-size': '28px',
                    'font-family': '"Lexend", sans-serif',
                    'color': '#042F2F',
                }), 
                html.Div([
                    dcc.Dropdown(
                        id='category-dropdown',
                        value='Todos',
                        clearable=False,
                        style={
                        'border-radius': '28px',
                        'background-color': '#ABF7F7',
                        'border': 'none',
                        }
                    )
                ],style={
                    'width': '30%',
                    'border-radius': '28px',
                    'padding': '10px 14px',
                    'background-color': '#ABF7F7',
                    'border': '1px solid #E0E0E0',
                    'box-shadow': '4px 4px 4px 0px rgba(0, 0, 0, 0.25)',
                    'font-family': '"Lexend", sans-serif',
                    'font-weight': 'bolder',
                    'height': '57px',
                    }),
            ],style={
                    'width': '100%',
                    'display': 'flex',
                    'justify-content': 'space-around',
                    'align-items': 'center',
                }),
            html.Br(),
            dcc.Graph(
                id='category-bar-chart',
                style={'transition': 'all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)',}
            )
            ],id='bar-id',style={
                'width': '45%',
                'display': 'inline-block',
                'padding': '0 10px',
                'background-color': '#ECFDFD',
                'box-shadow': '0px 2px 15px 0px rgba(56, 204, 204, 0.31), 0px 0px 4px 0px rgba(0, 0, 0, 0.4), 0px 4px 4px 0px rgba(0, 0, 0, 0.25)',
                'margin': '1.25rem',
                'border-radius': '24px',
                'padding': '1.25rem',
                'font-family': '"Lexend", sans-serif',
                'font-weight': 'bolder',
                'transition': 'all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)',
        }),
        html.Div([
            dcc.Graph(
                id='category-pie-chart',
                style={'transition': 'all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)',}
            )
            ],id='pie-id',style={
                'width': '45%',
                'display': 'inline-block',
                'padding': '0 10px',
                'background-color': '#ECFDFD',
                'box-shadow': '0px 2px 15px 0px rgba(56, 204, 204, 0.31), 0px 0px 4px 0px rgba(0, 0, 0, 0.4), 0px 4px 4px 0px rgba(0, 0, 0, 0.25)',
                'margin': '1.25rem',
                'border-radius': '24px',
                'padding': '1.25rem',
                'font-family': '"Lexend", sans-serif',
                'font-weight': 'bolder',
                'transition': 'all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)',
            })
        ], style={
            'width': '100%',
            'display': 'flex',
            'justify-content': 'center'
            }),
    html.Div([
        html.Div([
            html.H1("Ganancias por Cancha a lo largo de los Meses", style={
                'padding-top': '0.725rem',
                'padding-left': '1.125rem',
                'font-size': '28px',
                'font-family': '"Lexend", sans-serif',
                'color': '#042F2F',
            }),
            dcc.Dropdown(
                id='object-dropdown',
                options=[{'label':'Canchas' , 'value': 'cancha' },{'label':'Deportes','value':'deporte' } ],
                value='deporte',
                clearable=False,
                style={
                    'border-radius': '28px',
                    'background-color': '#ABF7F7',
                    'border': 'none',
                    'width': '150px',
                }
            ),
            dcc.Dropdown(
                id='year-dropdown',
                clearable=False,
                value=f'{datetime.now().year}',
                style={
                    'border-radius': '28px',
                    'background-color': '#ABF7F7',
                    'border': 'none',
                    'width': '150px',
                }
            )
        ],style={
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'gap': '100px',
            'font-family': '"Lexend", sans-serif',
            'font-weight': 'bolder',
        }),
        html.Br(),
        dcc.Graph(
            id='object-line',
            style={'transition': 'all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)',}
        ),
        dcc.RangeSlider(min=1, max=12, step=1, id='my-range-slider', value=[datetime.now().month-3,datetime.now().month],
                        marks={i: datetime(2000, i, 1).strftime('%B') for i in range(1, 13)}),
        ],id='line-id',style={
                'display': 'block',
                'justify-self': 'center',
                'padding': '0 10px',
                'background-color': '#ECFDFD',
                'box-shadow': '0px 2px 15px 0px rgba(56, 204, 204, 0.31), 0px 0px 4px 0px rgba(0, 0, 0, 0.4), 0px 4px 4px 0px rgba(0, 0, 0, 0.25)',
                'margin': '1.25rem',
                'border-radius': '24px',
                'padding': '1.25rem',
                'font-family': '"Lexend", sans-serif',
                'font-weight': 'bolder',
                'transition': 'all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)',
        })   
], style={
    'width': '100%',
}),
            fullscreen=True
        ),])
    

@app.callback(
    dash.dependencies.Output('category-pie-chart', 'figure'),
    [dash.dependencies.Input('category-dropdown', 'value')]
)

def update_category_pie_chart(selected_category, user):
    if user.is_authenticated:
        predio = Predios.objects.filter(user_id=user.id).first()
        canchas= Canchas.objects.filter(predio_id=predio)

        ganancias_por_deporte = Reservas.objects.filter(cancha_id__in=canchas).values('cancha_id__deporte_id__descripcion').annotate(
        ganancia=Sum('precio')
        )
        data = [{'deporte': item['cancha_id__deporte_id__descripcion'], 'ganancia': item['ganancia']} for item in ganancias_por_deporte]
        print(data)
        #filtered_df = df if selected_category == 'All Category' else df[df.variety == selected_category]
        dfd = pd.DataFrame(data)

        #category_df = filtered_df.groupby(['variety'])['sepal.length'].sum().reset_index()

        figure = px.pie(dfd, values='ganancia', names='deporte', title='Ganancia por categoría')
        
        figure.update_layout(
            title='Ganancia por categoría',
            plot_bgcolor='black',
            paper_bgcolor='#ECFDFD', 
            title_font=dict(family='Lexend, bold', size=28, color='#042F2F'),  # Establecer la fuente del título
            font=dict(family='Lexend', size=14, color='#042F2F'),  # Establecer la fuente del texto general
        )
        
        figure.update_traces(textfont=dict(family='Lexend', size=14, color='white'))
        figure.update_traces(marker=dict(colors=['#042F2F', '#38CCCC', '#ABF7F7', '#133C55', '#235789', '#246EB9']))
        figure.update_traces(hoverlabel=dict(font=dict(family='Lexend', size=14, color='white')))
        figure.update_traces(pull=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1] )
    else:
        return None
    return figure


@app.callback(
    dash.dependencies.Output('category-dropdown', 'options'),
    dash.dependencies.Output('category-bar-chart', 'figure'),
    [dash.dependencies.Input('category-dropdown', 'value'),
    ])
    
def update_category_bar_chart(selected_category, user):
    
    df = dfReservas(user)

    filtered_df = df if selected_category == 'Todos' else df[df.deporte == selected_category]
    category_df = filtered_df.groupby(['cancha']).size().reset_index(name='reservas')

    figure = px.bar(category_df, x='cancha', y='reservas', labels={'cancha': 'Canchas', 'reservas': 'Reservas'})
    
    figure.update_layout(
        plot_bgcolor='#ECFDFD',
        paper_bgcolor='#ECFDFD', 
        title_font=dict(family='Lexend, bold', size=28, color='#042F2F'),  # Establecer la fuente del título
        font=dict(family='Lexend', size=14, color='#042F2F'),  # Establecer la fuente del texto general
    )
        
    figure.update_traces(textfont=dict(family='Lexend', size=14, color='white'))
    figure.update_traces(marker=dict(color=['#042F2F', '#38CCCC', '#ABF7F7', '#133C55', '#235789', '#246EB9']))
    figure.update_traces(hoverlabel=dict(font=dict(family='Lexend', size=14, color='white')))

    options= [{'label': 'Todos', 'value': 'Todos'}] + [{'label': deporte, 'value': deporte} for deporte in df['deporte'].drop_duplicates()]


    return options, figure

@app.callback(
    dash.dependencies.Output('object-line', 'figure'),
    dash.dependencies.Output('year-dropdown', 'options'),
    [dash.dependencies.Input('object-dropdown', 'value'),
     dash.dependencies.Input('my-range-slider', 'value'),
     dash.dependencies.Input('year-dropdown', 'value'),])

def update_object_line(selected_category, date_range, year, user):
    df = dfReservas(user)
    options=[{'label': anio, 'value': anio} for anio in df['fecha'].dt.year.unique().tolist()]
    df=df[df['fecha'].dt.year == int(year)]
    df['mes'] = df['fecha'].dt.month  # Agrega una columna 'mes'
    if date_range is not None:
        df = df[df['mes'].between(date_range[0], date_range[1])]
    df = df.sort_values(by='fecha')


    figure = px.line(
        df,
        x='fecha',
        y='ganancia',
        color=selected_category,
        labels={'ganancia': 'Ganancias', 'fecha': 'Fecha'},
    )

    figure.update_traces(mode='lines+markers')
    figure.update_layout(
        plot_bgcolor='#ECFDFD',
        paper_bgcolor='#ECFDFD', 
        title_font=dict(family='Lexend, bold', size=28, color='#042F2F'),  # Establecer la fuente del título
        font=dict(family='Lexend', size=14, color='#042F2F'),  # Establecer la fuente del texto general
    )
        
    figure.update_traces(textfont=dict(family='Lexend', size=14, color='white'))
    figure.update_traces(marker=dict(color=['#042F2F', '#38CCCC', '#ABF7F7', '#133C55', '#235789', '#246EB9']))
    figure.update_traces(hoverlabel=dict(font=dict(family='Lexend', size=14, color='white')))


    return figure, options

def dfReservas(user):
    predio = Predios.objects.filter(user_id=user.id).first()
    canchas = Canchas.objects.filter(predio_id=predio)

    reservas_info = Reservas.objects.filter(cancha_id__in=canchas).select_related('cancha_id__deporte_id').values(
        'cancha_id__nombre',
        'fecha_ini',
        'precio',
        'cancha_id__deporte_id__descripcion'
    )

    # Convierte el resultado en un DataFrame
    df = pd.DataFrame(list(reservas_info))

    # Renombra las columnas para que coincidan con la estructura deseada
    df.columns = ['cancha', 'fecha', 'ganancia', 'deporte']
    return df