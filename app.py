#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
中国历史年表 - Web应用
使用Dash和Plotly创建交互式历史时间轴可视化
"""

import os
import json
import dash
from dash import dcc, html, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 初始化Dash应用
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG, 'https://fonts.googleapis.com/css2?family=ZCOOL+XiaoWei&display=swap'],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)
server = app.server
app.title = '中国历史年表'

# 加载数据
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, 'data')

# 读取处理后的时间轴数据
with open(os.path.join(data_dir, 'timeline_data.json'), 'r', encoding='utf-8') as f:
    timeline_data = json.load(f)

# 提取数据
dynasties = timeline_data['dynasties']
events = timeline_data['events']
figures = timeline_data['figures']
time_range = timeline_data['time_range']

# 定义颜色和样式
colors = {
    'background': '#111111',
    'text': '#FFFFFF',
    'primary': '#375A7F',
    'secondary': '#444444',
    'accent': '#00bc8c',
    'danger': '#E74C3C'
}

# 自定义CSS样式
styles = {
    'container': {
        'backgroundColor': colors['background'],
        'color': colors['text'],
        'fontFamily': '"ZCOOL XiaoWei", serif',
        'padding': '20px'
    },
    'header': {
        'textAlign': 'center',
        'marginBottom': '30px',
        'borderBottom': f'1px solid {colors["secondary"]}',
        'paddingBottom': '20px'
    },
    'title': {
        'fontSize': '3rem',
        'color': colors['accent'],
        'marginBottom': '10px'
    },
    'subtitle': {
        'fontSize': '1.5rem',
        'color': colors['text'],
        'fontWeight': 'normal'
    },
    'timeline': {
        'height': 'calc(100vh - 250px)',
        'minHeight': '500px',
        'backgroundColor': colors['background'],
        'border': f'1px solid {colors["secondary"]}',
        'borderRadius': '5px',
        'padding': '10px'
    },
    'controls': {
        'backgroundColor': colors['secondary'],
        'padding': '15px',
        'borderRadius': '5px',
        'marginBottom': '20px'
    },
    'detail-panel': {
        'backgroundColor': colors['secondary'],
        'padding': '15px',
        'borderRadius': '5px',
        'marginTop': '20px',
        'minHeight': '200px'
    },
    'detail-title': {
        'color': colors['accent'],
        'borderBottom': f'1px solid {colors["text"]}',
        'paddingBottom': '10px',
        'marginBottom': '15px'
    },
    'detail-content': {
        'color': colors['text'],
        'fontSize': '1.1rem',
        'lineHeight': '1.5'
    },
    'detail-image': {
        'maxWidth': '100%',
        'maxHeight': '300px',
        'borderRadius': '5px',
        'marginBottom': '15px'
    },
    'footer': {
        'textAlign': 'center',
        'marginTop': '30px',
        'paddingTop': '20px',
        'borderTop': f'1px solid {colors["secondary"]}',
        'color': colors['text']
    }
}

# 创建朝代时间轴数据
def create_dynasty_timeline():
    """创建朝代时间轴图表"""
    fig = go.Figure()
    
    # 添加朝代条带
    for dynasty in dynasties:
        fig.add_trace(go.Scatter(
            x=[dynasty['start_year'], dynasty['end_year'], dynasty['end_year'], dynasty['start_year'], dynasty['start_year']],
            y=[0, 0, 1, 1, 0],
            fill="toself",
            fillcolor=dynasty['color'],
            line=dict(width=0),
            name=dynasty['id'],
            text=f"{dynasty['id']} ({dynasty['start_year']}年 - {dynasty['end_year']}年)",
            hoverinfo="text",
            hoverlabel=dict(
                bgcolor=dynasty['color'],
                font_size=16,
                font_family='"ZCOOL XiaoWei", serif'
            ),
            showlegend=False
        ))
    
    # 添加朝代标签
    for dynasty in dynasties:
        # 计算朝代中间位置
        mid_year = (dynasty['start_year'] + dynasty['end_year']) / 2
        
        # 只为持续时间较长的朝代添加标签
        if dynasty['duration'] > 50:
            fig.add_annotation(
                x=mid_year,
                y=0.5,
                text=dynasty['id'],
                showarrow=False,
                font=dict(
                    family='"ZCOOL XiaoWei", serif',
                    size=14,
                    color='black'
                ),
                align="center",
                bgcolor="rgba(255, 255, 255, 0.7)",
                bordercolor="black",
                borderwidth=1,
                borderpad=4,
                opacity=0.8
            )
    
    # 设置布局
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            family='"ZCOOL XiaoWei", serif',
            size=14,
            color=colors['text']
        ),
        margin=dict(l=20, r=20, t=0, b=20),
        xaxis=dict(
            title="年份",
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            zeroline=False,
            showline=True,
            linecolor='rgba(255, 255, 255, 0.5)',
            tickfont=dict(size=12),
            tickformat=".0f",  # 显示整数年份
            range=[time_range['min_year'], time_range['max_year']]
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.1, 1.1]
        ),
        hovermode="closest",
        dragmode="pan",
        height=250
    )
    
    # 添加年份标记线
    for year in range(time_range['min_year'], time_range['max_year'] + 1, 100):
        if year == 0:
            # 公元元年特殊标记
            fig.add_shape(
                type="line",
                x0=year,
                y0=0,
                x1=year,
                y1=1,
                line=dict(
                    color="red",
                    width=2,
                    dash="dash",
                ),
            )
        else:
            # 每100年添加一条垂直标记线
            fig.add_shape(
                type="line",
                x0=year,
                y0=0,
                x1=year,
                y1=1,
                line=dict(
                    color="rgba(255, 255, 255, 0.2)",
                    width=1,
                ),
            )
    
    return fig

# 创建事件时间轴数据
def create_events_timeline():
    """创建历史事件时间轴图表"""
    fig = go.Figure()
    
    # 按重要性排序事件
    sorted_events = sorted(events, key=lambda x: x['importance'], reverse=True)
    
    # 添加事件标记
    for event in sorted_events:
        size = event['importance'] * 8  # 根据重要性调整大小
        fig.add_trace(go.Scatter(
            x=[event['year']],
            y=[0.5],
            mode='markers',
            marker=dict(
                size=size,
                color=colors['danger'],
                line=dict(width=2, color='white'),
                symbol='diamond',
                opacity=0.8
            ),
            name=event['title'],
            text=f"{event['title']} ({event['year']}年)<br>{event['description']}",
            hoverinfo="text",
            hoverlabel=dict(
                bgcolor=colors['secondary'],
                font_size=14,
                font_family='"ZCOOL XiaoWei", serif'
            ),
            customdata=[event['id']],  # 存储事件ID用于回调
            showlegend=False
        ))
    
    # 设置布局
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            family='"ZCOOL XiaoWei", serif',
            size=14,
            color=colors['text']
        ),
        margin=dict(l=20, r=20, t=0, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            zeroline=False,
            showline=True,
            linecolor='rgba(255, 255, 255, 0.5)',
            tickfont=dict(size=12),
            tickformat=".0f",  # 显示整数年份
            range=[time_range['min_year'], time_range['max_year']]
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.1, 1.1]
        ),
        hovermode="closest",
        height=150
    )
    
    return fig

# 创建人物时间轴数据
def create_figures_timeline():
    """创建历史人物时间轴图表"""
    fig = go.Figure()
    
    # 按重要性排序人物
    sorted_figures = sorted(figures, key=lambda x: x['importance'], reverse=True)
    
    # 添加人物生命线
    for i, figure in enumerate(sorted_figures):
        # 计算y位置，使人物分布在不同高度
        y_pos = 0.2 + (i % 3) * 0.3  # 分成3层显示
        
        # 添加人物生命线
        fig.add_trace(go.Scatter(
            x=[figure['birth_year'], figure['death_year']],
            y=[y_pos, y_pos],
            mode='lines',
            line=dict(
                color=colors['primary'],
                width=figure['importance'] * 1.5,  # 根据重要性调整宽度
                dash='solid'
            ),
            name=figure['name'],
            text=f"{figure['name']} ({figure['birth_year']}年 - {figure['death_year']}年)<br>{figure['description']}",
            hoverinfo="text",
            hoverlabel=dict(
                bgcolor=colors['secondary'],
                font_size=14,
                font_family='"ZCOOL XiaoWei", serif'
            ),
            customdata=[figure['id']],  # 存储人物ID用于回调
            showlegend=False
        ))
        
        # 添加人物标记点
        fig.add_trace(go.Scatter(
            x=[figure['birth_year']],
            y=[y_pos],
            mode='markers',
            marker=dict(
                size=figure['importance'] * 4,
                color=colors['primary'],
                line=dict(width=1, color='white'),
                symbol='circle'
            ),
            showlegend=False,
            hoverinfo="skip"
        ))
    
    # 设置布局
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            family='"ZCOOL XiaoWei", serif',
            size=14,
            color=colors['text']
        ),
        margin=dict(l=20, r=20, t=0, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            zeroline=False,
            showline=True,
            linecolor='rgba(255, 255, 255, 0.5)',
            tickfont=dict(size=12),
            tickformat=".0f",  # 显示整数年份
            range=[time_range['min_year'], time_range['max_year']]
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.1, 1.1]
        ),
        hovermode="closest",
        height=200
    )
    
    return fig

# 应用布局
app.layout = html.Div(style=styles['container'], children=[
    # 页面标题
    html.Div(style=styles['header'], children=[
        html.H1('中国历史年表', style=styles['title']),
        html.H2('探索中华文明的时间长河', style=styles['subtitle'])
    ]),
    
    # 控制面板
    html.Div(style=styles['controls'], children=[
        # 搜索和筛选区域
        dbc.Row([
            # 搜索功能
            dbc.Col([
                html.Label('搜索'),
                dbc.InputGroup([
                    dbc.Input(id='search-input', placeholder='输入关键词搜索朝代、事件或人物', type='text'),
                    dbc.InputGroupText(
                        html.I(className="fas fa-search")
                    ),
                ])
            ], width=6),
            
            # 事件分类筛选
            dbc.Col([
                html.Label('事件分类'),
                dcc.Dropdown(
                    id='event-category-filter',
                    options=[
                        {'label': '全部', 'value': 'all'},
                        {'label': '政治', 'value': '政治'},
                        {'label': '军事', 'value': '军事'},
                        {'label': '文化', 'value': '文化'},
                        {'label': '经济', 'value': '经济'},
                        {'label': '科技', 'value': '科技'}
                    ],
                    value='all',
                    clearable=False,
                    style={
                        'color': '#000000',
                        'background-color': '#f8f9fa'
                    }
                )
            ], width=3),
            
            # 重要性筛选
            dbc.Col([
                html.Label('重要性'),
                dcc.Slider(
                    id='importance-filter',
                    min=1,
                    max=5,
                    value=1,
                    marks={i: str(i) for i in range(1, 6)},
                    step=1
                )
            ], width=3)
        ], className='mb-3'),
        
        # 时间范围和显示选项
        dbc.Row([
            dbc.Col([
                html.Label('时间范围'),
                dcc.RangeSlider(
                    id='time-range-slider',
                    min=time_range['min_year'],
                    max=time_range['max_year'],
                    value=[time_range['min_year'], time_range['max_year']],
                    marks={year: str(year) for year in range(time_range['min_year'], time_range['max_year'] + 1, 500)},
                    step=10
                )
            ], width=8),
            dbc.Col([
                html.Label('显示选项'),
                dbc.Checklist(
                    id='display-options',
                    options=[
                        {'label': ' 朝代', 'value': 'dynasties'},
                        {'label': ' 事件', 'value': 'events'},
                        {'label': ' 人物', 'value': 'figures'},
                    ],
                    value=['dynasties', 'events', 'figures'],
                    inline=True,
                    switch=True
                )
            ], width=4)
        ])
    ]),
    
    # 时间轴容器
    html.Div(style=styles['timeline'], children=[
        # 朝代时间轴
        html.Div(id='dynasty-timeline-container', children=[
            dcc.Graph(
                id='dynasty-timeline',
                figure=create_dynasty_timeline(),
                config={'displayModeBar': False, 'scrollZoom': True}
            )
        ]),
        
        # 事件时间轴
        html.Div(id='events-timeline-container', children=[
            dcc.Graph(
                id='events-timeline',
                figure=create_events_timeline(),
                config={'displayModeBar': False, 'scrollZoom': True}
            )
        ]),
        
        # 人物时间轴
        html.Div(id='figures-timeline-container', children=[
            dcc.Graph(
                id='figures-timeline',
                figure=create_figures_timeline(),
                config={'displayModeBar': False, 'scrollZoom': True}
            )
        ])
    ]),
    
    # 详情面板
    html.Div(id='detail-panel', style=styles['detail-panel'], children=[
        html.H3('点击时间轴上的元素查看详情', style=styles['detail-title']),
        html.Div(id='detail-content', style=styles['detail-content'])
    ]),
    
    # 存储当前选中项的隐藏元素
    dcc.Store(id='selected-item-store'),
    
    # 页脚
    html.Footer(style=styles['footer'], children=[
        html.P('中国历史年表 © 2025')
    ])
])

# 回调函数：更新时间轴
@app.callback(
    [Output('dynasty-timeline', 'figure'),
     Output('events-timeline', 'figure'),
     Output('figures-timeline', 'figure')],
    [Input('time-range-slider', 'value'),
     Input('search-input', 'value'),
     Input('event-category-filter', 'value'),
     Input('importance-filter', 'value'),
     Input('dynasty-timeline', 'relayoutData'),
     Input('events-timeline', 'relayoutData'),
     Input('figures-timeline', 'relayoutData')]
)
def update_timelines(time_range_value, search_term, event_category, min_importance, 
                     dynasty_relayout, events_relayout, figures_relayout):
    # 确定触发回调的组件
    trigger_id = ctx.triggered_id
    
    # 如果是通过时间轴缩放触发的回调，实现联动
    xaxis_range = None
    if trigger_id in ['dynasty-timeline', 'events-timeline', 'figures-timeline']:
        # 获取触发时间轴的缩放范围
        relayout_data = dynasty_relayout if trigger_id == 'dynasty-timeline' else \
                        events_relayout if trigger_id == 'events-timeline' else figures_relayout
        
        if relayout_data and 'xaxis.range[0]' in relayout_data and 'xaxis.range[1]' in relayout_data:
            xaxis_range = [relayout_data['xaxis.range[0]'], relayout_data['xaxis.range[1]']]
    
    # 如果没有通过时间轴缩放触发，使用滑块范围
    if xaxis_range is None:
        xaxis_range = time_range_value
    
    # 过滤搜索条件
    filtered_events = events
    filtered_figures = figures
    
    # 根据搜索关键词过滤
    if search_term:
        search_term = search_term.lower()
        # 过滤事件
        filtered_events = [event for event in events if 
                          search_term in event['title'].lower() or 
                          search_term in event['description'].lower() or
                          search_term in event['dynasty'].lower()]
        
        # 过滤人物
        filtered_figures = [figure for figure in figures if 
                           search_term in figure['name'].lower() or 
                           search_term in figure['description'].lower() or
                           search_term in figure['dynasty'].lower()]
    
    # 根据事件分类过滤
    if event_category and event_category != 'all':
        filtered_events = [event for event in filtered_events if event['category'] == event_category]
    
    # 根据重要性过滤
    if min_importance:
        filtered_events = [event for event in filtered_events if event['importance'] >= min_importance]
        filtered_figures = [figure for figure in filtered_figures if figure['importance'] >= min_importance]
    
    # 更新朝代时间轴
    dynasty_fig = create_dynasty_timeline()
    dynasty_fig.update_layout(xaxis=dict(range=xaxis_range))
    
    # 创建并更新过滤后的事件时间轴
    events_fig = go.Figure()
    
    # 按重要性排序事件
    sorted_events = sorted(filtered_events, key=lambda x: x['importance'], reverse=True)
    
    # 添加事件标记
    for event in sorted_events:
        size = event['importance'] * 8  # 根据重要性调整大小
        # 根据分类设置颜色
        category_colors = {
            '政治': '#FF5733',  # 红色
            '军事': '#C70039',  # 深红色
            '文化': '#FFC300',  # 黄色
            '经济': '#DAF7A6',  # 浅绿色
            '科技': '#3498DB',  # 蓝色
            '其他': '#9B59B6'   # 紫色
        }
        color = category_colors.get(event['category'], colors['danger'])
        
        events_fig.add_trace(go.Scatter(
            x=[event['year']],
            y=[0.5],
            mode='markers',
            marker=dict(
                size=size,
                color=color,
                line=dict(width=2, color='white'),
                symbol='diamond',
                opacity=0.8
            ),
            name=event['title'],
            text=f"{event['title']} ({event['year']}年)<br>{event['description']}<br>分类: {event['category']}",
            hoverinfo="text",
            hoverlabel=dict(
                bgcolor=colors['secondary'],
                font_size=14,
                font_family='"ZCOOL XiaoWei", serif'
            ),
            customdata=[event['id']],  # 存储事件ID用于回调
            showlegend=False
        ))
    
    # 设置事件时间轴布局
    events_fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            family='"ZCOOL XiaoWei", serif',
            size=14,
            color=colors['text']
        ),
        margin=dict(l=20, r=20, t=0, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            zeroline=False,
            showline=True,
            linecolor='rgba(255, 255, 255, 0.5)',
            tickfont=dict(size=12),
            tickformat=".0f",  # 显示整数年份
            range=xaxis_range
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.1, 1.1]
        ),
        hovermode="closest",
        height=150
    )
    
    # 创建并更新过滤后的人物时间轴
    figures_fig = go.Figure()
    
    # 按重要性排序人物
    sorted_figures = sorted(filtered_figures, key=lambda x: x['importance'], reverse=True)
    
    # 添加人物生命线
    for i, figure in enumerate(sorted_figures):
        # 计算y位置，使人物分布在不同高度
        y_pos = 0.2 + (i % 3) * 0.3  # 分成3层显示
        
        # 添加人物生命线
        figures_fig.add_trace(go.Scatter(
            x=[figure['birth_year'], figure['death_year']],
            y=[y_pos, y_pos],
            mode='lines',
            line=dict(
                color=colors['primary'],
                width=figure['importance'] * 1.5,  # 根据重要性调整宽度
                dash='solid'
            ),
            name=figure['name'],
            text=f"{figure['name']} ({figure['birth_year']}年 - {figure['death_year']}年)<br>{figure['description']}",
            hoverinfo="text",
            hoverlabel=dict(
                bgcolor=colors['secondary'],
                font_size=14,
                font_family='"ZCOOL XiaoWei", serif'
            ),
            customdata=[figure['id']],  # 存储人物ID用于回调
            showlegend=False
        ))
        
        # 添加人物标记点
        figures_fig.add_trace(go.Scatter(
            x=[figure['birth_year']],
            y=[y_pos],
            mode='markers',
            marker=dict(
                size=figure['importance'] * 4,
                color=colors['primary'],
                line=dict(width=1, color='white'),
                symbol='circle'
            ),
            showlegend=False,
            hoverinfo="skip"
        ))
    
    # 设置人物时间轴布局
    figures_fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            family='"ZCOOL XiaoWei", serif',
            size=14,
            color=colors['text']
        ),
        margin=dict(l=20, r=20, t=0, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            zeroline=False,
            showline=True,
            linecolor='rgba(255, 255, 255, 0.5)',
            tickfont=dict(size=12),
            tickformat=".0f",  # 显示整数年份
            range=xaxis_range
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[-0.1, 1.1]
        ),
        hovermode="closest",
        height=200
    )
    
    return dynasty_fig, events_fig, figures_fig

# 回调函数：显示/隐藏时间轴组件
@app.callback(
    [Output('dynasty-timeline-container', 'style'),
     Output('events-timeline-container', 'style'),
     Output('figures-timeline-container', 'style')],
    [Input('display-options', 'value')]
)
def toggle_timeline_display(display_options):
    # 设置显示样式
    dynasty_style = {'display': 'block' if 'dynasties' in display_options else 'none'}
    events_style = {'display': 'block' if 'events' in display_options else 'none'}
    figures_style = {'display': 'block' if 'figures' in display_options else 'none'}
    
    return dynasty_style, events_style, figures_style

# 回调函数：点击事件或人物时更新详情面板
@app.callback(
    [Output('detail-content', 'children'),
     Output('selected-item-store', 'data')],
    [Input('events-timeline', 'clickData'),
     Input('figures-timeline', 'clickData')],
    [State('selected-item-store', 'data')]
)
def update_detail_panel(events_click, figures_click, selected_item):
    # 确定触发回调的组件
    trigger_id = ctx.triggered_id
    
    # 初始化返回值
    detail_content = []
    selected_data = selected_item or {}
    
    # 如果点击了事件
    if trigger_id == 'events-timeline' and events_click:
        event_id = events_click['points'][0]['customdata'][0]
        
        # 查找对应事件
        for event in events:
            if event['id'] == event_id:
                # 更新选中项
                selected_data = {
                    'type': 'event',
                    'id': event_id,
                    'data': event
                }
                
                # 创建详情内容
                detail_content = [
                    html.H3(f"{event['title']} ({event['year']}年)", style={'color': colors['accent']}),
                    html.Div([
                        html.Img(src=event['image_url'], style=styles['detail-image']) if event['image_url'] else None,
                        html.P(event['description']),
                        html.P(f"朝代: {event['dynasty']}", style={'fontStyle': 'italic'})
                    ])
                ]
                break
    
    # 如果点击了人物
    elif trigger_id == 'figures-timeline' and figures_click:
        figure_id = figures_click['points'][0]['customdata'][0]
        
        # 查找对应人物
        for figure in figures:
            if figure['id'] == figure_id:
                # 更新选中项
                selected_data = {
                    'type': 'figure',
                    'id': figure_id,
                    'data': figure
                }
                
                # 创建详情内容
                detail_content = [
                    html.H3(f"{figure['name']} ({figure['birth_year']}-{figure['death_year']})", style={'color': colors['accent']}),
                    html.Div([
                        html.Img(src=figure['image_url'], style=styles['detail-image']) if figure['image_url'] else None,
                        html.P(figure['description']),
                        html.P(f"朝代: {figure['dynasty']}", style={'fontStyle': 'italic'})
                    ])
                ]
                break
    
    # 如果没有点击事件，但有已选中项，保持当前显示
    elif selected_item:
        if selected_item['type'] == 'event':
            event = selected_item['data']
            detail_content = [
                html.H3(f"{event['title']} ({event['year']}年)", style={'color': colors['accent']}),
                html.Div([
                    html.Img(src=event['image_url'], style=styles['detail-image']) if event['image_url'] else None,
                    html.P(event['description']),
                    html.P(f"朝代: {event['dynasty']}", style={'fontStyle': 'italic'})
                ])
            ]
        elif selected_item['type'] == 'figure':
            figure = selected_item['data']
            detail_content = [
                html.H3(f"{figure['name']} ({figure['birth_year']}-{figure['death_year']})", style={'color': colors['accent']}),
                html.Div([
                    html.Img(src=figure['image_url'], style=styles['detail-image']) if figure['image_url'] else None,
                    html.P(figure['description']),
                    html.P(f"朝代: {figure['dynasty']}", style={'fontStyle': 'italic'})
                ])
            ]
    
    # 如果没有点击事件且没有已选中项，显示默认消息
    else:
        detail_content = [html.P('点击时间轴上的事件或人物查看详细信息')]
    
    return detail_content, selected_data

# 启动服务器
if __name__ == '__main__':
    # 获取环境变量中的端口，如果不存在则使用默认端口8051
    port = int(os.environ.get('PORT', 8051))
    app.run_server(debug=False, host='0.0.0.0', port=port)
