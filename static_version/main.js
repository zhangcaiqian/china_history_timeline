// 全局变量
let timelineData = null;
let timeRange = [-2100, 2025]; // 默认时间范围
let searchTerm = '';
let selectedCategory = 'all';
let minImportance = 1;

// 初始化页面
document.addEventListener('DOMContentLoaded', function() {
    // 加载数据
    fetch('timeline_data.json')
        .then(response => response.json())
        .then(data => {
            timelineData = data;
            initializeTimeRangeSlider();
            updateTimelines();
            setupEventListeners();
        })
        .catch(error => console.error('加载数据失败:', error));
});

// 初始化时间范围滑块
function initializeTimeRangeSlider() {
    const slider = document.getElementById('time-range-slider');
    
    noUiSlider.create(slider, {
        start: [-2100, 2025],
        connect: true,
        range: {
            'min': -2100,
            'max': 2025
        },
        step: 1
    });
    
    slider.noUiSlider.on('update', function(values, handle) {
        timeRange = [parseInt(values[0]), parseInt(values[1])];
        updateTimeRangeDisplay();
        updateTimelines();
    });
}

// 更新时间范围显示
function updateTimeRangeDisplay() {
    document.getElementById('min-year').textContent = formatYear(timeRange[0]);
    document.getElementById('max-year').textContent = formatYear(timeRange[1]);
}

// 格式化年份显示
function formatYear(year) {
    if (year < 0) {
        return `公元前${Math.abs(year)}年`;
    } else {
        return `${year}年`;
    }
}

// 设置事件监听器
function setupEventListeners() {
    // 搜索框
    document.getElementById('search-input').addEventListener('input', function(e) {
        searchTerm = e.target.value.trim();
        updateTimelines();
    });
    
    // 分类筛选
    document.getElementById('category-dropdown').addEventListener('change', function(e) {
        selectedCategory = e.target.value;
        updateTimelines();
    });
    
    // 重要性筛选
    document.getElementById('importance-slider').addEventListener('input', function(e) {
        minImportance = parseInt(e.target.value);
        updateTimelines();
    });
}

// 更新所有时间轴
function updateTimelines() {
    if (!timelineData) return;
    
    updateDynastyTimeline();
    updateEventTimeline();
    updateFigureTimeline();
}

// 更新朝代时间轴
function updateDynastyTimeline() {
    const filteredDynasties = timelineData.dynasties.filter(dynasty => {
        // 时间范围筛选
        const endYear = dynasty.end_year > 2025 ? 2025 : dynasty.end_year;
        const inTimeRange = (dynasty.start_year <= timeRange[1] && endYear >= timeRange[0]);
        
        // 搜索筛选
        const matchesSearch = searchTerm === '' || 
            dynasty.dynasty.toLowerCase().includes(searchTerm.toLowerCase()) ||
            dynasty.description.toLowerCase().includes(searchTerm.toLowerCase());
        
        return inTimeRange && matchesSearch;
    });
    
    const data = [{
        x: filteredDynasties.map(d => [d.start_year, d.end_year]),
        y: filteredDynasties.map(d => d.dynasty),
        text: filteredDynasties.map(d => d.description),
        type: 'scatter',
        mode: 'lines',
        line: {
            width: 20,
            color: filteredDynasties.map(d => d.color)
        },
        hoverinfo: 'text',
        hoverlabel: {
            bgcolor: '#FFF',
            bordercolor: '#333',
            font: {size: 14}
        }
    }];
    
    const layout = {
        height: 400,
        margin: {l: 100, r: 50, t: 30, b: 50},
        xaxis: {
            range: timeRange,
            title: '年份',
            tickformat: '.0f'
        },
        yaxis: {
            title: '朝代',
            automargin: true
        },
        hovermode: 'closest'
    };
    
    Plotly.newPlot('dynasty-timeline', data, layout);
}

// 更新历史事件时间轴
function updateEventTimeline() {
    const filteredEvents = timelineData.events.filter(event => {
        // 时间范围筛选
        const inTimeRange = (event.year >= timeRange[0] && event.year <= timeRange[1]);
        
        // 搜索筛选
        const matchesSearch = searchTerm === '' || 
            event.event.toLowerCase().includes(searchTerm.toLowerCase()) ||
            event.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
            event.dynasty.toLowerCase().includes(searchTerm.toLowerCase());
        
        // 分类筛选
        const matchesCategory = selectedCategory === 'all' || event.category === selectedCategory;
        
        // 重要性筛选
        const meetsImportance = event.importance >= minImportance;
        
        return inTimeRange && matchesSearch && matchesCategory && meetsImportance;
    });
    
    const data = [{
        x: filteredEvents.map(e => e.year),
        y: filteredEvents.map(e => e.event),
        text: filteredEvents.map(e => `<b>${e.event}</b><br>${e.description}<br>朝代: ${e.dynasty}<br>重要性: ${e.importance}<br>分类: ${e.category}`),
        type: 'scatter',
        mode: 'markers',
        marker: {
            size: filteredEvents.map(e => e.importance * 5),
            color: filteredEvents.map(e => getCategoryColor(e.category)),
            opacity: 0.8
        },
        hoverinfo: 'text',
        hoverlabel: {
            bgcolor: '#FFF',
            bordercolor: '#333',
            font: {size: 14}
        }
    }];
    
    const layout = {
        height: 500,
        margin: {l: 150, r: 50, t: 30, b: 50},
        xaxis: {
            range: timeRange,
            title: '年份',
            tickformat: '.0f'
        },
        yaxis: {
            title: '历史事件',
            automargin: true
        },
        hovermode: 'closest'
    };
    
    Plotly.newPlot('event-timeline', data, layout);
}

// 更新历史人物时间轴
function updateFigureTimeline() {
    const filteredFigures = timelineData.figures.filter(figure => {
        // 时间范围筛选
        const inTimeRange = (figure.birth_year <= timeRange[1] && figure.death_year >= timeRange[0]);
        
        // 搜索筛选
        const matchesSearch = searchTerm === '' || 
            figure.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            figure.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
            figure.dynasty.toLowerCase().includes(searchTerm.toLowerCase());
        
        // 重要性筛选
        const meetsImportance = figure.importance >= minImportance;
        
        return inTimeRange && matchesSearch && meetsImportance;
    });
    
    const data = [{
        x: filteredFigures.map(f => [f.birth_year, f.death_year]),
        y: filteredFigures.map(f => f.name),
        text: filteredFigures.map(f => `<b>${f.name}</b><br>${f.description}<br>朝代: ${f.dynasty}<br>生卒年: ${formatYear(f.birth_year)} - ${formatYear(f.death_year)}<br>重要性: ${f.importance}`),
        type: 'scatter',
        mode: 'lines',
        line: {
            width: 10,
            color: filteredFigures.map(f => getDynastyColor(f.dynasty))
        },
        hoverinfo: 'text',
        hoverlabel: {
            bgcolor: '#FFF',
            bordercolor: '#333',
            font: {size: 14}
        }
    }];
    
    const layout = {
        height: 500,
        margin: {l: 100, r: 50, t: 30, b: 50},
        xaxis: {
            range: timeRange,
            title: '年份',
            tickformat: '.0f'
        },
        yaxis: {
            title: '历史人物',
            automargin: true
        },
        hovermode: 'closest'
    };
    
    Plotly.newPlot('figure-timeline', data, layout);
}

// 获取分类颜色
function getCategoryColor(category) {
    const colorMap = {
        '政治': '#3498DB',
        '军事': '#E74C3C',
        '文化': '#2ECC71',
        '经济': '#F39C12',
        '科技': '#9B59B6'
    };
    
    return colorMap[category] || '#95A5A6';
}

// 获取朝代颜色
function getDynastyColor(dynasty) {
    if (!timelineData) return '#95A5A6';
    
    const dynastyObj = timelineData.dynasties.find(d => d.dynasty === dynasty);
    return dynastyObj ? dynastyObj.color : '#95A5A6';
}
