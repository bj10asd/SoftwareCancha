
from django.urls import reverse
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from reservas.models import Predios,Deportes,Canchas,Reservas
from django.db.models import Sum, Count

deportes=list(Deportes.objects.values('descripcion'))
deportes.append({'descripcion': 'Todos'})
print(deportes)
app = DjangoDash('dash_example')

app.layout = html.Div([
    html.H1("Ventas por categoría"),
    html.Div([
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': i['descripcion'], 'value': i['descripcion']} for i in deportes],
            value='Todos'
        )
    ],style={'width': '30%'}),
    html.Br(),
    html.Div([
        dcc.Graph(
            id='category-bar-chart'
        )
    ],style={'width': '45%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(
            id='category-pie-chart'
        )
    ],style={'width': '45%', 'display': 'inline-block', 'padding': '0 20'})
])

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
    else:
        return None
    return figure


@app.callback(
    dash.dependencies.Output('category-bar-chart', 'figure'),
    [dash.dependencies.Input('category-dropdown', 'value')])
    
def update_category_bar_chart(selected_category, user):
    
    predio = Predios.objects.filter(user_id=user.id).first()
    canchas= Canchas.objects.filter(predio_id=predio)

    #reservas_por_cancha = Reservas.objects.filter(cancha_id__in=canchas).values('cancha_id__nombre', 'cancha_id__deporte_id__descripcion').annotate(
    #cantidad_de_reservas=Count('id')
    #)
    #data = [{'cancha': item['cancha_id__nombre'], 'reservas': item['cantidad_de_reservas'], 'deporte':item['cancha_id__deporte_id__descripcion']} for item in reservas_por_cancha]
    #filtered_df = df if selected_category == 'All Category' else df[df.variety == selected_category]
    #df = pd.DataFrame(data)
    #filtered_df = df if selected_category == 'All Category' else df[df.deporte == selected_category]
    #category_df = filtered_df.groupby(['variety'])['sepal.length'].sum().reset_index()


    reservas_info = Reservas.objects.filter(cancha_id__in=canchas).select_related('cancha_id__deporte_id').values(
    'cancha_id__nombre',
    'fecha_ini__year',
    'fecha_ini__month',
    'precio',
    'cancha_id__deporte_id__descripcion'
    )

    # Convierte el resultado en un DataFrame
    df = pd.DataFrame(list(reservas_info))

    # Renombra las columnas para que coincidan con la estructura deseada
    df.columns = ['cancha', 'año', 'mes', 'ganancia', 'deporte']

    filtered_df = df if selected_category == 'Todos' else df[df.deporte == selected_category]
    category_df = filtered_df.groupby(['cancha']).size().reset_index(name='reservas')

    figure = px.bar(category_df, x='cancha', y='reservas', color='cancha', title='Reservas por cancha')

    return figure