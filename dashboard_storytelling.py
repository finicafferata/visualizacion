"""
Dashboard Storytelling - Liderazgo Femenino Global
La Paradoja del Liderazgo Femenino en el Mundo Empresarial

Implementado 100% con Plotly Dash
"""

import dash
from dash import dcc, html, Input, Output, callback, dash_table, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from colorsys import rgb_to_hls, hls_to_rgb

# Cargar y procesar datos
df = pd.read_csv('firms-with-female-top-manager-of-firms-bars.csv')
df['percentage'] = df['Firms with female top manager (% of firms)'].round(1)
df_countries = df[df['Code'].notna()].copy()
df_regions = df[df['Code'].isna()].copy()

# Configuraciones de storytelling
STORY_MODES = {
    'despertar': {
        'title': '🌅 ACTO I: El Despertar',
        'subtitle': 'La realidad oculta del liderazgo femenino global',
        'description': 'En un mundo donde las mujeres son el 50% de la población, solo el 18.6% de las empresas tienen liderazgo femenino. Esta disparidad revela una historia más profunda.',
        'chart_type': 'map',
        'year': 2017
    },
    'investigacion': {
        'title': '🔍 ACTO II: La Investigación',
        'subtitle': 'Los países que esperarías que lideren... no lo hacen',
        'description': 'Bolivia, Ecuador y Perú lideran globalmente, mientras que los países desarrollados quedan atrás. ¿Qué factores explican esta paradoja?',
        'chart_type': 'countries',
        'year': 2017
    },
    'reflexion': {
        'title': '🤔 ACTO III: La Reflexión',
        'subtitle': '¿Qué hemos aprendido y hacia dónde vamos?',
        'description': 'La evolución temporal revela patrones complejos. Algunos países avanzan, otros retroceden. ¿Cuál es el camino hacia la equidad?',
        'chart_type': 'regions',
        'year': 2017
    },
    'libre': {
        'title': '🎯 Exploración Libre',
        'subtitle': 'Explora los datos por tu cuenta',
        'description': 'Usa los controles para descubrir patrones únicos y crear tus propias conclusiones sobre el liderazgo femenino global.',
        'chart_type': 'map',
        'year': 2017
    }
}

# Configuraciones de regiones y grupos (manteniendo tu código original)
regiones_geograficas = {
    'East Asia & Pacific': 'EAP',
    'East Asia & Pacific (IDA & IBRD)': 'EAP (IDA & IBRD)',
    'East Asia & Pacific (excluding high income)': 'EAP (exc HI)',
    'Europe & Central Asia': 'ECA',
    'Europe & Central Asia (IDA & IBRD)': 'ECA (IDA & IBRD)',
    'Europe & Central Asia (excluding high income)': 'ECA (exc HI)',
    'Latin America & Caribbean': 'LAC',
    'Latin America & Caribbean (IDA & IBRD)': 'LAC (IDA & IBRD)',
    'Latin America & Caribbean (excluding high income)': 'LAC (exc HI)',
    'Middle East & North Africa': 'MENA',
    'Middle East & North Africa (IDA & IBRD)': 'MENA (IDA & IBRD)',
    'Middle East & North Africa (excluding high income)': 'MENA (exc HI)',
    'South Asia': 'SA',
    'South Asia (IDA & IBRD)': 'SA (IDA & IBRD)',
    'Sub-Saharan Africa': 'SSA',
    'Sub-Saharan Africa (IDA & IBRD)': 'SSA (IDA & IBRD)',
    'Sub-Saharan Africa (excluding high income)': 'SSA (exc HI)'
}

abreviaturas_grupos = {
    'Pre-demographic dividend': {'abreviatura': 'Pre-DD', 'categoria': 1},
    'Early-demographic dividend': {'abreviatura': 'Early-DD', 'categoria': 1},
    'Late-demographic dividend': {'abreviatura': 'Late-DD', 'categoria': 1},
    'Post-demographic dividend': {'abreviatura': 'Post-DD', 'categoria': 1},
    'Heavily indebted poor countries (HIPC)': {'abreviatura': 'HIPC', 'categoria': 2},
    'Fragile and conflict affected situations': {'abreviatura': 'Fragile', 'categoria': 2},
    'Least developed countries: UN classification': {'abreviatura': 'LDC', 'categoria': 2},
    'Low income': {'abreviatura': 'Low', 'categoria': 3},
    'Lower middle income': {'abreviatura': 'Lower Mid', 'categoria': 3},
    'Low & middle income': {'abreviatura': 'Low & Mid', 'categoria': 3},
    'Middle income': {'abreviatura': 'Middle', 'categoria': 3},
    'Upper middle income': {'abreviatura': 'Upper Mid', 'categoria': 3},
    'High income': {'abreviatura': 'High', 'categoria': 3},
    'IDA blend': {'abreviatura': 'IDA Blend', 'categoria': 4},
    'IDA only': {'abreviatura': 'IDA Only', 'categoria': 4},
    'IBRD only': {'abreviatura': 'IBRD Only', 'categoria': 4},
    'IDA & IBRD total': {'abreviatura': 'IDA & IBRD', 'categoria': 4},
    'IDA total': {'abreviatura': 'IDA Total', 'categoria': 4}
}

colores_categorias = {
    1: 'rgb(158,202,225)',   # Azul claro
    2: 'rgb(253,174,97)',    # Naranja
    3: 'rgb(214,96,77)',     # Rojo
    4: 'rgb(107,174,214)'    # Azul oscuro
}

# Procesar datos
df_regiones_geograficas = df_regions[df_regions['Entity'].isin(regiones_geograficas.keys())].copy()
grupos_economicos_lista = list(abreviaturas_grupos.keys())
df_grupos_economicos = df_regions[df_regions['Entity'].isin(grupos_economicos_lista)].copy()

# Configuración de colores para regiones
colores = px.colors.qualitative.Set2
colores_base = {
    'East Asia & Pacific': colores[0],
    'Europe & Central Asia': colores[1],
    'Latin America & Caribbean': colores[2],
    'Middle East & North Africa': colores[3],
    'South Asia': colores[4],
    'Sub-Saharan Africa': colores[5]
}

def shade_color(color, factor):
    if color.startswith('rgb'):
        color = color[4:-1].split(',')
        r, g, b = [int(c) / 255 for c in color]
    else:
        r, g, b = tuple(int(color.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4))
    h, l, s = rgb_to_hls(r, g, b)
    l = max(0, min(1, factor * l))
    r, g, b = hls_to_rgb(h, l, s)
    return f'rgb({int(r*255)}, {int(g*255)}, {int(b*255)})'

colores_regiones = {}
for region, abreviatura in regiones_geograficas.items():
    if 'IDA & IBRD' in region:
        colores_regiones[abreviatura] = shade_color(colores_base[region.split(' (')[0]], 0.7)
    elif 'excluding high income' in region:
        colores_regiones[abreviatura] = shade_color(colores_base[region.split(' (')[0]], 1.0)
    else:
        colores_regiones[abreviatura] = colores_base[region]

colores_grupos = {}
for grupo in grupos_economicos_lista:
    abreviatura = abreviaturas_grupos[grupo]['abreviatura']
    categoria = abreviaturas_grupos[grupo]['categoria']
    colores_grupos[abreviatura] = colores_categorias[categoria]

# Inicializar aplicación
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout principal con storytelling
app.layout = dbc.Container([
    # Store para el modo historia
    dcc.Store(id='story-mode', data='despertar'),
    
    # Header narrativo
    html.Div([
        html.H1("La Paradoja del Liderazgo Femenino Global", 
                className="text-center mb-2", 
                style={'fontWeight': 'bold', 'fontSize': '3rem', 'color': '#2C3E50'}),
        html.P("Un viaje por los datos que revelan la realidad del liderazgo empresarial femenino",
               className="text-center text-muted mb-4", style={'fontSize': '1.2rem'})
    ], className="mb-4"),
    
    # Panel de navegación de historia
    dbc.Card([
        dbc.CardBody([
            html.Div(id='narrative-header', className="mb-3"),
            
            # Botones de navegación de historia
            dbc.ButtonGroup([
                dbc.Button("🌅 Despertar", id="story-despertar", color="primary", outline=True),
                dbc.Button("🔍 Investigación", id="story-investigacion", color="info", outline=True),
                dbc.Button("🤔 Reflexión", id="story-reflexion", color="warning", outline=True),
                dbc.Button("🎯 Exploración Libre", id="story-libre", color="secondary", outline=True)
            ], className="d-flex justify-content-center mb-3"),
            
            # Descripción narrativa
            html.Div(id='narrative-content', className="text-center")
        ])
    ], className="mb-4"),
    
    # Métricas globales destacadas (dinámicas)
    html.Div(id='global-metrics', className="mb-4"),
    
    # Controles principales (solo visible en modo libre)
    html.Div([
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Año de Análisis:", className="fw-bold"),
                        dcc.Dropdown(
                            id='year-dropdown',
                            options=[{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
                            value=2017,
                            clearable=False
                        )
                    ], width=6),
                    dbc.Col([
                        html.Label("Tipo de Visualización:", className="fw-bold"),
                        dcc.Dropdown(
                            id='chart-type',
                            options=[
                                {'label': '🗺️ Mapa Mundial', 'value': 'map'},
                                {'label': '🏆 Top Países', 'value': 'countries'},
                                {'label': '🌎 Por Región', 'value': 'regions'},
                                {'label': '💰 Por Grupo Económico', 'value': 'economic'}
                            ],
                            value='map',
                            clearable=False
                        )
                    ], width=6)
                ])
            ])
        ], className="mb-4")
    ], id="main-controls-panel"),
    
    # Visualización principal
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading([
                        dcc.Graph(
                            id='main-visualization', 
                            style={'height': '600px'},
                            config={'displayModeBar': True}
                        )
                    ])
                ])
            ])
        ], width=9),
        
        # Panel de insights dinámicos
        dbc.Col([
            html.Div(id='insights-panel'),
            
            # Leyenda de regiones (solo visible cuando se muestran regiones)
            html.Div([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("🗺️ Significado de Regiones", className="mb-0")
                    ]),
                    dbc.CardBody([
                        html.Div([
                            html.P([html.Strong("EAP: "), "East Asia & Pacific"], className="mb-1 small"),
                            html.P([html.Strong("ECA: "), "Europe & Central Asia"], className="mb-1 small"),
                            html.P([html.Strong("LAC: "), "Latin America & Caribbean"], className="mb-1 small"),
                            html.P([html.Strong("MENA: "), "Middle East & North Africa"], className="mb-1 small"),
                            html.P([html.Strong("SA: "), "South Asia"], className="mb-1 small"),
                            html.P([html.Strong("SSA: "), "Sub-Saharan Africa"], className="mb-1 small"),
                            html.Hr(className="my-2"),
                            html.P([html.Strong("IDA & IBRD: "), "Incluye países del Banco Mundial"], className="mb-1 small"),
                            html.P([html.Strong("exc HI: "), "Excluyendo países de altos ingresos"], className="mb-0 small")
                        ])
                    ])
                ], color="light", className="mt-3")
            ], id="regions-legend", style={'display': 'none'}),
            
            # Leyenda de grupos económicos (solo visible cuando se muestran grupos)
            html.Div([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6("💰 Significado de Grupos Económicos", className="mb-0")
                    ]),
                    dbc.CardBody([
                        html.Div([
                            html.P([
                                html.Span("█", style={'color': 'rgb(158,202,225)', 'fontSize': '20px'}),
                                " ", html.Strong("Dividendo Demográfico")
                            ], className="mb-1 small"),
                            html.P("Pre-DD, Early-DD, Late-DD, Post-DD", className="mb-2 small text-muted", style={'marginLeft': '25px'}),
                            
                            html.P([
                                html.Span("█", style={'color': 'rgb(253,174,97)', 'fontSize': '20px'}),
                                " ", html.Strong("Países Vulnerables")
                            ], className="mb-1 small"),
                            html.P("HIPC, Fragile, LDC", className="mb-2 small text-muted", style={'marginLeft': '25px'}),
                            
                            html.P([
                                html.Span("█", style={'color': 'rgb(214,96,77)', 'fontSize': '20px'}),
                                " ", html.Strong("Niveles de Ingreso")
                            ], className="mb-1 small"),
                            html.P("Low, Lower Mid, Upper Mid, High", className="mb-2 small text-muted", style={'marginLeft': '25px'}),
                            
                            html.P([
                                html.Span("█", style={'color': 'rgb(107,174,214)', 'fontSize': '20px'}),
                                " ", html.Strong("Clasificación Bancaria")
                            ], className="mb-1 small"),
                            html.P("IDA, IBRD (Banco Mundial)", className="mb-0 small text-muted", style={'marginLeft': '25px'})
                        ])
                    ])
                ], color="light", className="mt-3")
            ], id="economic-legend", style={'display': 'none'})
        ], width=3)
    ]),
    
    # Selector de país (siempre visible)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("🔍 Seleccionar País para Análisis Comparativo", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id='country-dropdown',
                                options=[{'label': country, 'value': country} for country in sorted(df_countries['Entity'].unique())],
                                value='World',
                                placeholder="Selecciona un país..."
                            )
                        ], width=8),
                        dbc.Col([
                            dbc.Switch(
                                id="show-insights",
                                label="Mostrar Insights",
                                value=True
                            )
                        ], width=4)
                    ])
                ])
            ], color="primary", outline=True, className="mb-3")
        ], width=12)
    ]),
    
    # Análisis comparativo
    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📈 Evolución Temporal")),
                    dbc.CardBody([
                        dcc.Graph(id='time-series', style={'height': '300px'})
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🔄 Comparación Directa")),
                    dbc.CardBody([
                        html.Div(id='comparison-content')
                    ])
                ])
            ], width=6)
        ])
    ], id="analysis-panel"),
    
    # Footer con llamada a la acción
    html.Hr(className="mt-5"),
    dbc.Alert([
        html.H5("💡 Reflexión Final"),
        html.P("Los datos revelan que la equidad de género en el liderazgo empresarial no depende únicamente del desarrollo económico. "),
        html.P("¿Qué factores culturales, políticos y sociales explican estas diferencias?"),
    ], color="info", className="text-center")
    
], fluid=True)

# Callbacks para storytelling
@callback(
    [Output('story-mode', 'data'),
     Output('narrative-header', 'children'),
     Output('narrative-content', 'children'),
     Output('main-controls-panel', 'style'),
     Output('story-despertar', 'color'),
     Output('story-investigacion', 'color'),
     Output('story-reflexion', 'color'),
     Output('story-libre', 'color')],
    [Input('story-despertar', 'n_clicks'),
     Input('story-investigacion', 'n_clicks'),
     Input('story-reflexion', 'n_clicks'),
     Input('story-libre', 'n_clicks')],
    prevent_initial_call=False
)
def update_story_mode(despertar, investigacion, reflexion, libre):
    ctx = dash.callback_context
    
    # Determinar qué botón se presionó
    if not ctx.triggered:
        mode = 'despertar'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        mode = button_id.replace('story-', '')
    
    story = STORY_MODES[mode]
    
    # Header narrativo
    header = html.Div([
        html.H3(story['title'], className="text-primary mb-2"),
        html.H5(story['subtitle'], className="text-muted mb-0")
    ])
    
    # Contenido narrativo
    content = html.P(story['description'], className="lead")
    
    # Mostrar/ocultar controles principales según el modo
    controls_style = {'display': 'none'} if mode != 'libre' else {'display': 'block'}
    
    # Colores de botones
    colors = ['outline'] * 4
    if mode == 'despertar':
        colors[0] = 'primary'
    elif mode == 'investigacion':
        colors[1] = 'info'
    elif mode == 'reflexion':
        colors[2] = 'warning'
    else:
        colors[3] = 'secondary'
    
    return mode, header, content, controls_style, colors[0], colors[1], colors[2], colors[3]

# Callback para métricas globales dinámicas
@callback(
    Output('global-metrics', 'children'),
    [Input('story-mode', 'data'),
     Input('year-dropdown', 'value')],
    prevent_initial_call=False
)
def update_global_metrics(story_mode, selected_year):
    # Usar año de historia o seleccionado
    if story_mode != 'libre':
        year = STORY_MODES[story_mode]['year']
    else:
        year = selected_year
    
    # Calcular métricas para el año seleccionado
    df_year = df_countries[df_countries['Year'] == year]
    
    if not df_year.empty:
        # Usar valor de "World" si existe, sino promedio calculado
        world_data = df_year[df_year['Entity'] == 'World']
        if not world_data.empty:
            global_avg = world_data['percentage'].iloc[0]
            global_label = "World"
        else:
            global_avg = df_year['percentage'].mean()
            global_label = "Promedio Mundial"
            
        max_row = df_year.loc[df_year['percentage'].idxmax()]
        max_country = max_row['Entity']
        max_value = max_row['percentage']
    else:
        # Fallback a todos los años si no hay datos
        global_avg = df_countries['percentage'].mean()
        global_label = "Promedio Mundial"
        max_row = df_countries.loc[df_countries['percentage'].idxmax()]
        max_country = max_row['Entity']
        max_value = max_row['percentage']
        year_text = f"({max_row['Year']})"
    
    # Diferencia regional (usar datos disponibles)
    df_regions_year = df_regiones_geograficas[df_regiones_geograficas['Year'] == year]
    if df_regions_year.empty:
        df_regions_year = df_regiones_geograficas[df_regiones_geograficas['Year'] == 2017]
    
    if not df_regions_year.empty:
        regional_max = df_regions_year['percentage'].max()
        regional_min = df_regions_year['percentage'].min()
        regional_ratio = regional_max / regional_min if regional_min > 0 else 0
    else:
        regional_ratio = 7  # Fallback
    
    # Total de países con datos para ese año
    total_countries = len(df_year) if not df_year.empty else len(df_countries['Entity'].unique())
    
    metrics_row = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(f"{global_avg:.1f}%", className="text-primary text-center mb-0"),
                    html.P(global_label, className="text-center text-muted mb-0"),
                    html.Small(f"{year}", className="text-center text-muted")
                ])
            ], className="h-100")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(f"{max_value:.1f}%", className="text-success text-center mb-0"),
                    html.P(f"{max_country} (Líder)", className="text-center text-muted mb-0", 
                           style={'fontSize': '0.9rem'}),
                    html.Small(f"Máximo global ({max_row['Year']})" if 'year_text' in locals() else "Máximo global", 
                              className="text-center text-muted")
                ])
            ], className="h-100")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(f"{regional_ratio:.1f}x", className="text-danger text-center mb-0"),
                    html.P("Diferencia Regional", className="text-center text-muted mb-0"),
                    html.Small("Máx vs Mín", className="text-center text-muted")
                ])
            ], className="h-100")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(f"{total_countries}", className="text-info text-center mb-0"),
                    html.P("Países Analizados", className="text-center text-muted mb-0"),
                    html.Small(f"Año {year}", className="text-center text-muted")
                ])
            ], className="h-100")
        ], width=3),
    ])
    
    return metrics_row

# Callback principal para visualizaciones
@callback(
    [Output('main-visualization', 'figure'),
     Output('time-series', 'figure'),
     Output('insights-panel', 'children'),
     Output('comparison-content', 'children'),
     Output('regions-legend', 'style'),
     Output('economic-legend', 'style')],
    [Input('story-mode', 'data'),
     Input('year-dropdown', 'value'),
     Input('chart-type', 'value'),
     Input('country-dropdown', 'value'),
     Input('show-insights', 'value')],
    prevent_initial_call=False
)
def update_visualizations(story_mode, selected_year, chart_type, selected_country, show_insights):
    # Usar configuración de historia o controles manuales
    if story_mode != 'libre':
        story_config = STORY_MODES[story_mode]
        chart_type = story_config['chart_type']
        selected_year = story_config['year']
    
    # Crear visualización principal
    if chart_type == 'map':
        main_fig = create_world_map(selected_year, story_mode)
    elif chart_type == 'countries':
        main_fig = create_countries_chart(selected_year, story_mode)
    elif chart_type == 'regions':
        main_fig = create_regions_chart(selected_year)
    else:  # economic
        main_fig = create_economic_groups_chart(selected_year)
    
    # Serie temporal
    time_fig = create_time_series(selected_country)
    
    # Panel de insights
    insights = create_insights_panel(selected_year, chart_type, story_mode, show_insights)
    
    # Contenido de comparación
    comparison = create_comparison_content(selected_year, selected_country, chart_type)
    
    # Mostrar/ocultar leyendas según el tipo de gráfico
    regions_legend_style = {'display': 'block'} if chart_type == 'regions' else {'display': 'none'}
    economic_legend_style = {'display': 'block'} if chart_type == 'economic' else {'display': 'none'}
    
    return main_fig, time_fig, insights, comparison, regions_legend_style, economic_legend_style

# Funciones de visualización mejoradas
def create_world_map(year, story_mode):
    df_year = df_countries[df_countries['Year'] == year]
    
    fig = px.choropleth(
        df_year,
        locations="Code",
        color="percentage",
        hover_name="Entity",
        title=f'Porcentaje de Empresas con Liderazgo Femenino ({year})',
        color_continuous_scale="Viridis",
        labels={'percentage': 'Porcentaje (%)'},
        range_color=[0, df_year['percentage'].max()]
    )
    
    # Añadir anotaciones según el modo historia
    if story_mode == 'despertar':
        # Resaltar el promedio mundial
        global_avg = df_year['percentage'].mean()
        fig.add_annotation(
            text=f"Promedio Mundial: {global_avg:.1f}%",
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            showarrow=False,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black"
        )
    
    fig.update_layout(
        title_x=0.5,
        geo=dict(showframe=False, showcoastlines=True),
        height=600
    )
    
    return fig

def create_countries_chart(year, story_mode):
    df_year = df_countries[df_countries['Year'] == year]
    df_top = df_year.nlargest(15, 'percentage')
    
    fig = px.bar(
        df_top,
        x='Entity',
        y='percentage',
        title=f'Top 15 Países - Liderazgo Femenino ({year})',
        labels={'Entity': 'País', 'percentage': 'Porcentaje (%)'},
        color='percentage',
        color_continuous_scale='Viridis'
    )
    
    # Añadir línea de referencia usando el valor de "World" si existe
    world_data = df_countries[(df_countries['Entity'] == 'World') & (df_countries['Year'] == year)]
    
    if not world_data.empty:
        world_value = world_data['percentage'].iloc[0]
        reference_label = f"World: {world_value:.1f}%"
        reference_value = world_value
    else:
        # Fallback al promedio calculado si no existe World
        reference_value = df_year['percentage'].mean()
        reference_label = f"Promedio Mundial: {reference_value:.1f}%"
    
    fig.add_hline(
        y=reference_value, 
        line_dash="dash", 
        line_color="red",
        annotation_text=reference_label
    )
    
    if story_mode == 'investigacion':
        # Resaltar el país líder del año
        leader_country = df_top.iloc[0]['Entity']
        leader_value = df_top.iloc[0]['percentage']
        
        # Encontrar el líder absoluto de todos los tiempos
        absolute_leader = df_countries.loc[df_countries['percentage'].idxmax()]
        
        if leader_country == absolute_leader['Entity']:
            annotation_text = f"¡{leader_country} lidera este año!"
        else:
            annotation_text = f"¡{leader_country} lidera en {year}!\n(Líder absoluto: {absolute_leader['Entity']} {absolute_leader['percentage']:.1f}% en {absolute_leader['Year']})"
        
        fig.add_annotation(
            text=annotation_text,
            x=0, y=leader_value,
            arrowhead=2,
            arrowcolor="red",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="red"
        )
    
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title_x=0.5, height=600)
    
    return fig

def create_regions_chart(year):
    df_year = df_regiones_geograficas[df_regiones_geograficas['Year'] == year].copy()
    
    if df_year.empty:
        df_year = df_regiones_geograficas[df_regiones_geograficas['Year'] == 2017].copy()
    
    df_year['RegionAbreviada'] = df_year['Entity'].map(regiones_geograficas)
    
    fig = px.bar(
        df_year.sort_values(by="percentage", ascending=False),
        x="RegionAbreviada",
        y="percentage",
        color="RegionAbreviada",
        color_discrete_map={reg: colores_regiones[reg] for reg in df_year['RegionAbreviada'].unique()},
        text_auto=True,
        title="Porcentaje de Mujeres en Puestos de Alta Dirección por Región en 2017",
        labels={'RegionAbreviada': 'Región', 'percentage': 'Porcentaje'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis_title=None,
        yaxis_title=None,
        xaxis={'categoryorder':'total descending', 'tickangle':-45},
        margin=dict(b=150),
        height=600,
        title_x=0.5
    )
    
    fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    
    return fig

def create_economic_groups_chart(year):
    df_year = df_grupos_economicos[df_grupos_economicos['Year'] == year].copy()
    
    if df_year.empty:
        df_year = df_grupos_economicos[df_grupos_economicos['Year'] == 2017].copy()
    
    df_year['GrupoAbreviado'] = df_year['Entity'].map(lambda x: abreviaturas_grupos[x]['abreviatura'])
    df_year['GrupoAbreviado'] = pd.Categorical(
        df_year['GrupoAbreviado'], 
        categories=[abreviaturas_grupos[x]['abreviatura'] for x in grupos_economicos_lista], 
        ordered=True
    )
    df_year = df_year.sort_values('GrupoAbreviado')
    
    fig = px.bar(
        df_year,
        x="GrupoAbreviado",
        y="percentage",
        color="GrupoAbreviado",
        color_discrete_map=colores_grupos,
        text_auto=True,
        title="Porcentaje de Mujeres en Puestos de Alta Dirección por Grupo Económico en 2017",
        labels={'GrupoAbreviado': 'Grupo Económico', 'percentage': 'Porcentaje'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis_title=None,
        yaxis_title=None,
        xaxis={'tickangle':-45},
        margin=dict(b=200),
        height=600,
        title_x=0.5
    )
    
    fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    
    return fig

def create_time_series(country):
    if country == 'World':
        df_time = df_countries.groupby('Year')['percentage'].mean().reset_index()
        title = "Evolución del Promedio Mundial"
    else:
        df_time = df_countries[df_countries['Entity'] == country]
        title = f"Evolución: {country}"
    
    fig = px.line(
        df_time,
        x='Year',
        y='percentage',
        title=title,
        labels={'Year': 'Año', 'percentage': 'Porcentaje (%)'},
        markers=True
    )
    
    fig.update_layout(title_x=0.5, showlegend=False, height=300)
    
    return fig

def create_insights_panel(year, chart_type, story_mode, show_insights):
    if not show_insights:
        return []
    
    # Insights específicos por modo de historia
    insights_by_mode = {
        'despertar': [
            "🚨 Solo 1 de cada 5 empresas tiene liderazgo femenino",
            "🌍 Existe una brecha de 64 puntos entre países",
            "💡 Las empresas diversas superan financieramente a las homogéneas"
        ],
        'investigacion': [
            "🇧🇴 Bolivia lidera con 26.3% - ¿Sorprendente?",
            "🏛️ Los países desarrollados no dominan el ranking",
            "📊 No hay correlación directa PIB-equidad"
        ],
        'reflexion': [
            "📈 Progreso lento: +2.1% en una década",
            "🌏 Asia del Este lidera regionalmente (32.7%)",
            "⚖️ La equidad requiere políticas específicas"
        ],
        'libre': [
            f"📅 Analizando datos de {year}",
            f"📊 Visualización: {chart_type}",
            "🎯 Explora patrones únicos"
        ]
    }
    
    insights = insights_by_mode.get(story_mode, [])
    
    cards = []
    for insight in insights:
        cards.append(
            dbc.Card([
                dbc.CardBody([
                    html.P(insight, className="mb-0 small")
                ])
            ], color="light", className="mb-2")
        )
    
    return [
        html.H6("💡 Insights Clave", className="mb-3"),
        *cards
    ]

def create_comparison_content(year, country, chart_type):
    if country == 'World':
        return html.P("Selecciona un país específico para ver comparaciones", className="text-muted")
    
    # Obtener datos del país
    country_data = df_countries[
        (df_countries['Entity'] == country) & 
        (df_countries['Year'] == year)
    ]
    
    if country_data.empty:
        return html.P(f"No hay datos disponibles para {country} en {year}", className="text-muted")
    
    country_value = country_data['percentage'].iloc[0]
    global_avg = df_countries[df_countries['Year'] == year]['percentage'].mean()
    
    comparison_items = [
        html.H6(f"📍 {country}", className="mb-2"),
        html.P(f"Valor: {country_value:.1f}%", className="mb-1"),
        html.P(f"vs Mundial: {country_value - global_avg:+.1f}pp", 
               className=f"mb-1 {'text-success' if country_value > global_avg else 'text-danger'}"),
        html.Hr(),
        html.Small(f"Promedio mundial: {global_avg:.1f}%", className="text-muted")
    ]
    
    return comparison_items

if __name__ == '__main__':
    import os
    
    # Configuración para producción
    debug_mode = os.getenv('ENVIRONMENT', 'development') == 'development'
    port = int(os.getenv('PORT', 8054))
    
    if debug_mode:
        print("🎭 Dashboard Storytelling iniciado en http://localhost:8054")
        print("📖 Experiencia narrativa sobre liderazgo femenino global")
        print("🎯 Navegación guiada en 3 actos + exploración libre")
    
    app.run(debug=debug_mode, port=port, host='0.0.0.0')