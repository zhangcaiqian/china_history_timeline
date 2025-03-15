#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
中国历史年表 - 数据处理脚本
处理朝代、事件和人物数据，生成可视化所需的JSON格式
"""

import os
import json
import pandas as pd
import numpy as np

def load_data():
    """加载CSV数据文件"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    dynasties_df = pd.read_csv(os.path.join(data_dir, 'dynasties.csv'))
    events_df = pd.read_csv(os.path.join(data_dir, 'events.csv'))
    figures_df = pd.read_csv(os.path.join(data_dir, 'figures.csv'))
    
    return dynasties_df, events_df, figures_df

def process_dynasties(dynasties_df):
    """处理朝代数据"""
    # 处理年份（将公元前年份表示为负数）
    dynasties_df['start_year'] = dynasties_df['start_year'].astype(int)
    dynasties_df['end_year'] = dynasties_df['end_year'].astype(int)
    
    # 计算每个朝代的持续时间
    dynasties_df['duration'] = dynasties_df['end_year'] - dynasties_df['start_year']
    
    # 转换为时间轴所需的格式
    dynasties_list = []
    for _, row in dynasties_df.iterrows():
        dynasty = {
            'id': row['dynasty'],
            'start_year': int(row['start_year']),
            'end_year': int(row['end_year']),
            'duration': int(row['duration']),
            'description': row['description'],
            'color': row['color'],
            'type': 'dynasty'
        }
        dynasties_list.append(dynasty)
    
    return dynasties_list

def process_events(events_df):
    """处理历史事件数据"""
    # 处理年份
    events_df['year'] = events_df['year'].astype(int)
    
    # 如果没有category列，添加默认分类
    if 'category' not in events_df.columns:
        # 根据事件标题和描述推断分类
        def infer_category(row):
            title = str(row['event']).lower() if pd.notna(row['event']) else ''
            desc = str(row['description']).lower() if pd.notna(row['description']) else ''
            text = title + ' ' + desc
            
            # 简单的关键词匹配来推断分类
            if any(word in text for word in ['战争', '战役', '起义', '军队', '将军', '攻打', '征服', '入侵']):
                return '军事'
            elif any(word in text for word in ['皇帝', '政权', '改革', '制度', '法律', '朝廷', '官员', '宰相']):
                return '政治'
            elif any(word in text for word in ['文学', '艺术', '哲学', '思想', '宗教', '教育', '文化', '诗人']):
                return '文化'
            elif any(word in text for word in ['经济', '商业', '贸易', '农业', '税收', '货币', '财政']):
                return '经济'
            elif any(word in text for word in ['发明', '科技', '技术', '天文', '医学', '工程', '建筑']):
                return '科技'
            else:
                return '其他'
        
        events_df['category'] = events_df.apply(infer_category, axis=1)
    
    # 转换为时间轴所需的格式
    events_list = []
    for _, row in events_df.iterrows():
        event = {
            'id': f"event_{row.name}",
            'year': int(row['year']),
            'title': row['event'],
            'description': row['description'],
            'dynasty': row['dynasty'],
            'importance': int(row['importance']),
            'category': row['category'],
            'image_url': row['image_url'] if pd.notna(row['image_url']) else None,
            'type': 'event'
        }
        events_list.append(event)
    
    return events_list

def process_figures(figures_df):
    """处理历史人物数据"""
    # 处理年份
    figures_df['birth_year'] = figures_df['birth_year'].astype(int)
    figures_df['death_year'] = figures_df['death_year'].astype(int)
    
    # 转换为时间轴所需的格式
    figures_list = []
    for _, row in figures_df.iterrows():
        figure = {
            'id': f"figure_{row.name}",
            'name': row['name'],
            'birth_year': int(row['birth_year']),
            'death_year': int(row['death_year']),
            'dynasty': row['dynasty'],
            'description': row['description'],
            'importance': int(row['importance']),
            'image_url': row['image_url'] if pd.notna(row['image_url']) else None,
            'type': 'figure'
        }
        figures_list.append(figure)
    
    return figures_list

def create_timeline_data(dynasties_list, events_list, figures_list):
    """创建完整的时间轴数据"""
    # 合并所有数据
    timeline_data = {
        'dynasties': dynasties_list,
        'events': events_list,
        'figures': figures_list
    }
    
    # 计算时间范围
    all_years = []
    for dynasty in dynasties_list:
        all_years.extend([dynasty['start_year'], dynasty['end_year']])
    
    for event in events_list:
        all_years.append(event['year'])
    
    for figure in figures_list:
        all_years.extend([figure['birth_year'], figure['death_year']])
    
    timeline_data['time_range'] = {
        'min_year': min(all_years),
        'max_year': max(all_years)
    }
    
    return timeline_data

def save_processed_data(timeline_data):
    """保存处理后的数据为JSON文件"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    with open(os.path.join(data_dir, 'timeline_data.json'), 'w', encoding='utf-8') as f:
        json.dump(timeline_data, f, ensure_ascii=False, indent=2)
    
    print("数据处理完成，已保存到 timeline_data.json")

def main():
    """主函数"""
    print("开始处理中国历史年表数据...")
    
    # 加载数据
    dynasties_df, events_df, figures_df = load_data()
    
    # 处理数据
    dynasties_list = process_dynasties(dynasties_df)
    events_list = process_events(events_df)
    figures_list = process_figures(figures_df)
    
    # 创建时间轴数据
    timeline_data = create_timeline_data(dynasties_list, events_list, figures_list)
    
    # 保存处理后的数据
    save_processed_data(timeline_data)

if __name__ == "__main__":
    main()
