###CS50 FINAL PROJECT###
#BY VICENTE ARTURO ZAMORA VASQUEZ#
#COUNTRY: BOLIVIA#
#CITY: SANTA CRUZ#

import dash
from dash import Dash, html, dcc, callback, Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import sqlite3

# execute 'scrap.py' as if it were written in the app.py file
with open('scrap.py') as scrap:
    exec(scrap.read())

# Connect to SQLite database
conn = sqlite3.connect('bol_wars.db')


# QUERY EVERYTHING FROM word_categories TABLE
query = 'SELECT * FROM word_categories'
df = pd.read_sql_query(query, conn)


# Rename row names in 'category"
row_names = {'opositores':'Oposición',
             'masistas':'Oficialismo',
             'economia':'Economía', 
             'politica':'Política', 
             'seguridad':'Seguridad', 
             'narcotrafico':'Narcotráfico'}


# Rename row names in 'sites'
row_names_sites = {'https://eldeber.com.bo/': 'El Deber',
    'https://erbol.com.bo/': 'Erbol',
    'https://correodelsur.com/': 'Correo del Sur',
    'https://www.lostiempos.com/': 'Los Tiempos',
    'https://www.opinion.com.bo/':'Opinion',
    'https://www.la-razon.com/':'La Razon',
    'https://elpotosi.net/':'El Potosi',
    'https://www.eldiario.net/portal/':'El Diario',
    'https://unitel.bo/':'Unitel',
    'https://www.atb.com.bo/':'ATB',
    'https://www.reduno.com.bo/':'Red Uno',
    'https://www.noticiasfides.com/':'Fides'
}


# Change 'category' row names for new row_names
df['category'] = df['category'].replace(row_names)


# Change 'site' row names for row_names_sites
df['site'] = df['site'].replace(row_names_sites)


# Convert 'count' to numeric
df['count'] = pd.to_numeric(df['count'])


# Convert 'date' to datetime format
df['date'] = pd.to_datetime(df['date'])


# Get last date in database
last_date = df['date'].iloc[-1]


# Custom marker colors for each category
color_dict = {
    'Oposición': 'orange',
    'Oficialismo': 'blue',
    'Economía': 'green',
    'Política': 'purple',
    'Seguridad': 'red',
    'Narcotráfico':'cyan'
}


# PORCENTAJE POR CATEGORIA A TRAVES DEL TIEMPO BAR CHART

# Create the pivot table and calculate percentages
pivot_df = pd.pivot_table(df, values='count', index='date', columns='category', aggfunc='sum', fill_value=0)

percentage_df = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# Create the Plotly Percentage figure PORCENTAJE POR CATEGORIA A TRAVES DEL TIEMPO
fig_line = px.bar(percentage_df, 
                  x=percentage_df.index, 
                  y=percentage_df.columns,
                  color_discrete_map=color_dict,
            )
fig_line.update_layout(

    legend=dict(
        title_text='',
        orientation="h",
        entrywidth=50,
        yanchor="bottom", 
        y=1.0, 
        xanchor="right", 
        x=1.00,
        font=dict(
            size=9
        )
    ),
    margin=dict(
        b=10,
        l=10,
        r=10,
        t=10,
    ),
    height=300,
)

fig_line.update_xaxes(title_text='')  # Set x-axis label to an empty string
fig_line.update_yaxes(title_text='')  # Set y-axis label to an empty string


### NOT USED FOR NOW
# Create line charts for each category
line_charts = []
for category in percentage_df.columns:
    line_chart = px.line(percentage_df, x=percentage_df.index, y=category,
                         title=f'{category} Percentage Over Time',
                         labels={'index': 'Date', category: 'Percentage'},
                         )
    line_charts.append(html.Div([dcc.Graph(figure=line_chart, id=f'{category}-line-chart')]))
####



### FOR SITE LINE CHARTS    
# Calculate the percentage for each category on each day
df_percent = df.groupby(['site', 'date', 'category']).agg({'count': 'sum'}).reset_index()
df_percent['percentage'] = df_percent.groupby(['site', 'date'])['count'].transform(lambda x: x / x.sum() * 100)

# Create line charts for each site
line_charts_sites = []
for site in df['site'].unique():
    filtered_data = df_percent[df_percent['site'] == site]
    line_chart_sites = px.line(filtered_data, 
                            x='date', 
                            y='percentage', 
                            color='category', 
                            line_group='category',
                            labels={'percentage': 'Percentage'}, 
                            #title=f'{site} De que habla',
                            color_discrete_map=color_dict,
                        )
    line_chart_sites.update_layout(
        showlegend=False,
        legend=dict(
            orientation='h',
            title_text='',
            yanchor='bottom',
            y=1.00,
            xanchor='right',
            x=1.00,
            font=dict(
                size=9
            )
        ),
        margin=dict(
            b=10,
            l=1,
            r=1,
            t=10,    
        ),
        height=250,
    )

    line_chart_sites.update_xaxes(title_text='')  # Set x-axis label to an empty string
    line_chart_sites.update_yaxes(title_text='')  # Set y-axis label to an empty string

    line_charts_sites.append(html.Div([dcc.Graph(figure=line_chart_sites, id=f'line-chart-{site}')]))




# ***---- DASH APP BEGINS ---***
    
#app = Dash(__name__)
app = dash.Dash(
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

app.title = "Bolivian Media Wars"

server = app.server

app.layout = html.Div([


    # DIV 1 BEGINS
    html.Div([

        # 1.1 DIV LOGO
        html.Div([
                html.Img(src=app.get_asset_url('bolivian_media_wars_logo.png'),
                style = {'height':'150px'},
                className = 'title_image'
                ),
        ], className='one-thrid column', id = 'title11'),

        #1.2 TITLE
        html.Div([
            html.P('"Bolivian Media Wars" es un proyecto finalizado como parte del curso CS50 de la Universidad de Harvard, concebido como un web scraper que analiza los principales sitios web de noticias en Bolivia. El objetivo es identificar palabras clave y clasificarlas en seis categorías: política, seguridad, economía, oficialismo, oposición y narcotráfico. Posteriormente, el proyecto genera gráficos interactivos que representan visualmente las tendencias de los medios bolivianos a lo largo del tiempo, permitiendo un análisis detallado de los temas más relevantes. Esta herramienta ofrece una visión profunda de la dinámica mediática en Bolivia, permitiendo a los usuarios comprender las preferencias y posturas editoriales de los medios, y proporcionando una valiosa perspectiva sobre la diversidad de opiniones presentes en el panorama mediático del país.',
                        style = {'color': '#000000',
                                 'padding-top':'20px',
                                 'padding-bottom':'20px',
                                 'padding-right':'20px',
                                 'padding-left':'20px',
                                 'text-align':'justify',
                                 
                                 },
                        className = 'title'
                        
                        ),

        ],id = 'title111'),
    # DIV 1 ENDS
    ], className = 'flex_container2'),


    # DIV 2 BEGINS
    html.Div([
        #DIV column first 1/2
        html.Div([


            # DIV 2.1 DATE DROPDOWN
            # DIV DATE TITLE FECHA
            html.Div([
                html.P('Fecha: ', id='date_dropdown_title'),
            ], style={'text-align':'right', 'font-size':'20px', 'font-weight':'bold', 'padding-left':'20px', 'flex':'1'}),

            # DIV DROPDOWN
            html.Div([
                dcc.Dropdown(
                    id='fecha',
                    options=[{'label':date.strftime('%Y-%m-%d'), 'value':date} for date in df['date'].unique()],
                    value=last_date,
                    style={
                        'width':'80%'
                    }
                ),
            #]),
            #], className='one-half column', id = 'title2'),
            #], style={'width':'50%', 'text-align-last':'center', 'padding-left':'10px'}),
            ], style={'text-align':'center', 'flex':'2'}),
        ], style={'border':'2px', 'flex':'1', 'display':'flex'}),   
        #], className='prueba_1'),
        # END DIV column first 1/2

        # DIV column second 1/2
        html.Div([
            html.P('DATOS HISTORICOS DE LOS MEDIOS', id='Datos Historicos'),
        ], className='prueba_2', style={'text-align':'center', 'font-weight':'bold'}),
    # DIV 2 ENDS
    #], className='flex_container'),
    ], style={'display':'flex', 'flex-direction':'row'}),






    # ***--- DIV CONTAINER_FLEX ---***
    html.Div([

        # DIV column 2/3
        html.Div([

            # DIV 3 BEGINS
            html.Div([

                # DIV 3.1 PIE CHART - PROMEDIO DE TODOS LOS MEDIOS
                html.Div([
                    html.Div([
                        html.P('De que hablan los medios hoy?'),

                    ], style={'text-align':'center', 'font-weight':'bold'}),


                    html.Div([
                        #dcc.Graph(id='promedio_todos_medios', style={'width':'100%', 'height':'100%'}),
                        dcc.Graph(id='promedio_todos_medios', style={'width':'100%', 'height':'100%'}),
                    ]),
         
                ], className='borde_pie_chart'),


                # DIV 3.1 BAR CHART - PORCENTAJE POR CATEGORIA
                html.Div([
                    html.Div([
                        html.P('Cuanto hablan de cada tema los medios')
                    ], style={'text-align':'center', 'font-weight':'bold'}),





                    html.Div([
                        dcc.Graph(id='porcentaje_categoria', style={'width':'100%', 'height':'100%'}),

                    ]),
     
                ]),

            # DIV 3 ENDS

            ]),


            #DIV 4 SUBPLOTS
            html.Div([
                html.P('De que Habla cada Medio?'),

                #DIV 4.1 SUBPLOT TRY1
                html.Div([
                    dcc.Graph(id='subplot1', style={'width':'100%', 'height':'100%'}, responsive='auto'),
                    ], style={'display': 'flex', 'flex-direction': 'column', 'width':'100%', 'height':'90vh'}),
                ], className='borde_pie_chart', style={'text-align':'center', 'font-weight':'bold'})
        # END DIV COLUMN 2/3

        ], className='prueba_1'), 



        # BEGIN DIV COLUMN 1/3
        html.Div([

            # DIV PORCENTAJE POR CATEGORIA A TRAVES DEL TIEMPO
            html.Div([
                dcc.Graph(
                    id='porcentaje_por_categoria',
                    figure=fig_line,
                    style={'width':'100%', 'height':'100%'})
            ], className='borde_bar_chart'),
            
            # DIV LINE TRY 1

            html.Div([
                html.Div([
                    html.P('El Deber'),
                    line_charts_sites[0]
                ], style={'flex':'1', 'min-width':'0'}),
                html.Div([
                    html.P('Erbol'),
                    line_charts_sites[1]
                ], style={'flex':'1', 'min-width':'0'}),
        
            ],style={'display':'flex', 'flex-direction':'row', 'text-align':'center', 'font-weight':'bold'}),


            html.Div([
                html.Div([
                    html.P('Correo del Sur'),
                    line_charts_sites[7]
                ], style={'flex':'1', 'min-width':'0'}),
                html.Div([
                    html.P('Los Tiempos'),
                    line_charts_sites[9]
                ], style={'flex':'1', 'min-width':'0'}),
            ],style={'display':'flex', 'flex-direction':'row', 'text-align':'center', 'font-weight':'bold'}),

            html.Div([
                html.Div([
                    html.P('Opinion'),
                    line_charts_sites[8]
                ], style={'flex':'1', 'min-width':'0'}),
                html.Div([
                    html.P('La Razon'),
                    line_charts_sites[4]
                ], style={'flex':'1', 'min-width':'0'}),
            ],style={'display':'flex', 'flex-direction':'row', 'text-align':'center', 'font-weight':'bold'}),


            html.Div([
                html.Div([
                    html.P('El Potosi'),
                    line_charts_sites[6]
                ], style={'flex':'1', 'min-width':'0'}),
                html.Div([
                    html.P('El Diario'),
                    line_charts_sites[10]
                ], style={'flex':'1', 'min-width':'0'}),
            ],style={'display':'flex', 'flex-direction':'row', 'text-align':'center', 'font-weight':'bold'}),


            html.Div([
                html.Div([
                    html.P('Unitel'),
                    line_charts_sites[3]
                ], style={'flex':'1', 'min-width':'0'}),
                html.Div([
                    html.P('ATB'),
                    line_charts_sites[12]
                ], style={'flex':'1', 'min-width':'0'}),
            ],style={'display':'flex', 'flex-direction':'row', 'text-align':'center', 'font-weight':'bold'}),


            html.Div([
                html.Div([
                    html.P('Red Uno'),
                    line_charts_sites[2]
                ], style={'flex':'1', 'min-width':'0'}),
                html.Div([
                    html.P('Fides'),
                    line_charts_sites[5]
                ], style={'flex':'1', 'min-width':'0'}),
            ],style={'display':'flex', 'flex-direction':'row', 'text-align':'center', 'font-weight':'bold'}),



        # FIN DIV COLUMN 1/3

        ], className='prueba_1'),


    #Fin flexbox
    ], style={'display':'flex', 'flex-direction':'row'})
    


# MAIN APP ENDS
], id = 'mainContainer')








#***CALLBACKS***CALLBACKS***CALLBACKS***

# CB 1.1 PIE CHART - PROMEDIO DE TODOS LOS MEDIOS
@app.callback(
    Output('promedio_todos_medios', 'figure'),
    Input('fecha', 'value'),
)
def update_graph(selected_date):
    
    # create new dataframe from df where 'date' is 'selected_date'
    dff = df[(df['date']==selected_date)]

    # Assign 'color_dict' colors to dff dataframe
    dff['marker_color'] = dff['category'].map(color_dict)
    
    # Graph Pie chart
    fig = go.Figure(data=[go.Pie(labels=dff['category'], values=dff['count'], marker=dict(colors=dff['marker_color']))])
    fig.update_layout(

        legend=dict(orientation="h", 
                    entrywidth=50,
                    yanchor="bottom", 
                    y=1.12, 
                    xanchor="right", 
                    x=1,
                    font=dict(
                        size=9
                    ),
        ),
        margin=dict(
            b=10,
            l=10,
            r=10,
            t=10,
            pad=0
        ),
        height=400,
    )
    
    return fig


# CB 1.2 BAR CHART - PORCENTAJE POR CATEGORIA
@app.callback(
    Output('porcentaje_categoria', 'figure'),
    Input('fecha', 'value'),
)

def update_graph(selected_date):
    
    # Filter data based
    dff = df[(df['date']==selected_date)]
    dff['marker_color'] = dff['category'].map(color_dict)

    filtered_df = dff.groupby(['site', 'category'])['id'].count().reset_index(name='total_count')
    filtered_df['marker_color'] = filtered_df['category'].map(color_dict)

    # List of specific sites to Include
    selected_sites = ['El Deber', 'Erbol', 'Correo del Sur', 'Los Tiempos', 'Opinion', 'La Razon','El Potosi',
                      'El Diario', 'Unitel', 'ATB', 'Red Uno', 'Fides']

    # Filter the DataFrame on selected sites
    filtered_df_selected_sites = filtered_df[filtered_df['site'].isin(selected_sites)]

    # Graph bar chart
    fig = px.bar(filtered_df_selected_sites, 
                 x='site', 
                 y='total_count', 
                 color='category', 
                 color_discrete_map=color_dict
            )
    fig.update_layout(
        legend=dict(
            title_text='',
            orientation="h",
            entrywidth=50, 
            yanchor="bottom", 
            y=1.00, 
            xanchor="right", 
            x=1,
            font=dict(
                size=9
            )
        ),
        margin=dict(
            b=10,
            l=10,
            r=10,
            t=10,
        )
    )

    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')

    return fig
    


# 1.3 CB SUBPLOTS
@app.callback(
    Output('subplot1', 'figure'),
    Input('fecha', 'value')
)



def update_pie_chart(selected_date):
    
    dff_eldeber = df[(df['date']==selected_date) & (df['site'] == 'El Deber')]
    dff_erbol = df[(df['date']==selected_date) & (df['site'] == 'Erbol')]
    dff_correodelsur = df[(df['date']==selected_date) & (df['site'] == 'Correo del Sur')]
    dff_lostiempos = df[(df['date']==selected_date) & (df['site'] == 'Los Tiempos')]
    dff_opinion = df[(df['date']==selected_date) & (df['site'] == 'Opinion')]
    dff_larazon = df[(df['date']==selected_date) & (df['site'] == 'La Razon')]
    dff_elpotosi = df[(df['date']==selected_date) & (df['site'] == 'El Potosi')]
    dff_eldiario = df[(df['date']==selected_date) & (df['site'] == 'El Diario')]
    dff_unitel = df[(df['date']==selected_date) & (df['site'] == 'Unitel')]
    dff_atb = df[(df['date']==selected_date) & (df['site'] == 'ATB')]
    dff_reduno = df[(df['date']==selected_date) & (df['site'] == 'Red Uno')]
    dff_fides = df[(df['date']==selected_date) & (df['site'] == 'Fides')]




   

    #Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows = 4, cols = 3, vertical_spacing=0.05, specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}],
                                                    [{'type':'pie'}, {'type':'pie'}, {'type':'pie'}],
                                                    [{'type':'pie'}, {'type':'pie'}, {'type':'pie'}],
                                                    [{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]
                                                   ])
    fig.add_trace(go.Pie(labels=dff_eldeber['category'], values=dff_eldeber['count'], name = 'eldeber_subplot', domain=dict(x=[0, 0.33]), title='El Deber', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_eldeber['category']])), 1, 1),
    fig.add_trace(go.Pie(labels=dff_erbol['category'], values=dff_erbol['count'], name = 'erbol_subplot', domain=dict(x=[0.34, 0.66]), title='Erbol', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_erbol['category']])), 1, 2),
    fig.add_trace(go.Pie(labels=dff_correodelsur['category'], values=dff_correodelsur['count'], name = 'correodelsur_subplot', domain=dict(x=[0.67, 1.0]), title='Correo del Sur', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_correodelsur['category']])), 1, 3),
    fig.add_trace(go.Pie(labels=dff_lostiempos['category'], values=dff_lostiempos['count'], name = 'lostiempos_subplot', domain=dict(x=[0.00, 0.33]), title='Los Tiempos', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_lostiempos['category']])), 2, 1),
    fig.add_trace(go.Pie(labels=dff_opinion['category'], values=dff_opinion['count'], name = 'opinion_subplot', domain=dict(x=[0.34, 0.66]), title='Opinión', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_opinion['category']])), 2, 2),
    fig.add_trace(go.Pie(labels=dff_larazon['category'], values=dff_larazon['count'], name = 'larazon_subplot', domain=dict(x=[0.67, 1.0]), title='La Razón', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_larazon['category']])), 2, 3),
    fig.add_trace(go.Pie(labels=dff_elpotosi['category'], values=dff_elpotosi['count'], name = 'elpotosi_subplot', domain=dict(x=[0.0, 0.33]), title='El Potosi', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_elpotosi['category']])), 3, 1),
    fig.add_trace(go.Pie(labels=dff_eldiario['category'], values=dff_eldiario['count'], name = 'eldiario_subplot', domain=dict(x=[0.34, 0.66]), title='El Diario', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_eldiario['category']])), 3, 2),
    fig.add_trace(go.Pie(labels=dff_unitel['category'], values=dff_unitel['count'], name = 'unitel_subplot', domain=dict(x=[0.67, 1.0]), title='Unitel', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_unitel['category']])), 3, 3),
    fig.add_trace(go.Pie(labels=dff_atb['category'], values=dff_atb['count'], name = 'atb_subplot', domain=dict(x=[0.0, 0.33]), title='ATB', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_atb['category']])), 4, 1),
    fig.add_trace(go.Pie(labels=dff_reduno['category'], values=dff_reduno['count'], name = 'reduno_subplot', domain=dict(x=[0.34, 0.66]), title='Red Uno', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_reduno['category']])), 4, 2),
    fig.add_trace(go.Pie(labels=dff_fides['category'], values=dff_fides['count'], name = 'fides_subplot', domain=dict(x=[0.67, 1.0]), title='Fides', titleposition='top center', titlefont=dict(size=14), marker=dict(colors=[color_dict.get(category, 'rgb(169, 169, 169)') for category in dff_fides['category']])), 4, 3)
    



    fig.update_traces(textposition='inside')


    fig.update_layout(

        legend=dict(orientation="h",
                    entrywidth=50, 
                    yanchor="bottom", 
                    y=1.05, 
                    xanchor="right", 
                    x=1,
                    font=dict(
                        size=9
                    ),
        ),
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        autosize=True,
        margin=dict(l=5, r=5, t=0, b=0)
        
    )
    
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
