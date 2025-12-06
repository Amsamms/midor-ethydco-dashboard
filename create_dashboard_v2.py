#!/usr/bin/env python3
"""
MIDOR-ETHYDCO Integration Dashboard V2
Modern, stunning design with language toggle
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# ============================================================================
# DATA EXTRACTION
# ============================================================================

def load_metrics():
    """Extract key metrics from the Excel file."""
    metrics = {}

    # Product Prices
    metrics['prices'] = {
        'H2': 2000, 'C2H6': 400, 'C2H4': 400, 'LPG': 729,
        'C5+': 620, 'Methanol': 450, 'Ethylene_MTO': 1200, 'Propylene_MTO': 900
    }

    # Streams
    metrics['streams'] = {
        'names': ['Flare Gas OLD', 'Flare Gas New', 'Refinery Gas', 'PSA Purge', 'Sweep Gas', 'Penex'],
        'names_ar': ['غاز الشعلة القديم', 'غاز الشعلة الجديد', 'غاز المصفاة', 'تنظيف PSA', 'غاز الكنس', 'بنيكس'],
        'flow_kgh': [4122, 2989, 48459.44, 62786.45, 3723.42, 2088.12],
        'flow_ty': [32976, 23912, 387675.54, 502291.59, 29787.34, 16704.93],
    }

    # Products
    metrics['products'] = {
        'H2': 39444.77, 'CH4': 251737.80, 'C2H6': 59230.02, 'C2H4': 2062.40,
        'C3H8': 57097.95, 'C3H6': 2915.37, 'iC4': 32898.08, 'nC4': 43014.61,
        'C4=': 4631.79, 'C5+': 21733.10, 'CO': 65956.12, 'CO2': 408747.17
    }

    # Stream components
    metrics['stream_components'] = {
        'H2': [4031.75, 3420.66, 16074.74, 10645.69, 2766.34, 2505.59],
        'CH4': [8659.03, 5530.73, 194089.88, 39689.32, 2692.79, 1076.05],
        'C2': [3640.52, 1992.00, 45949.35, 27.45, 7396.02, 2287.08],
        'C3': [4389.92, 3206.61, 36257.20, 48.31, 9011.38, 7099.90],
        'C4': [5636.10, 4645.15, 60600.94, 56.60, 6288.14, 3317.54],
        'C5+': [4396.36, 2768.20, 10851.65, 0, 1397.49, 2319.40],
        'CO': [5313.69, 4069.12, 29206.57, 24952.88, 0, 2413.85],
        'CO2': [2499.26, 2279.22, 0, 401936.87, 135.20, 1896.61]
    }

    # Calculation results
    metrics['calc1'] = {
        'total_LPG': 125508.57, 'total_C5+': 21733.10,
        'LPG_value': 91495749.75, 'C5+_value': 13474523.07,
        'net_value': 76231321.92
    }

    metrics['calc2'] = {
        'total_H2': 39444.77, 'H2_value': 78889537.01,
        'net_value': 61561956.72,
        'H2_sources': {'Off-Gas': 16074.74, 'Flare OLD': 4031.75, 'Flare New': 3420.66,
                       'PSA Purge': 10645.69, 'Sweep Gas': 2766.34, 'Penex': 2505.59}
    }

    metrics['calc3'] = {
        'MIDOR_C2_supply': 59005.34, 'ETHYDCO_C2_need_min': 83600,
        'ETHYDCO_C2_need_max': 121600, 'coverage_min': 0.7058,
        'coverage_max': 0.4852, 'C2_value': 23602135.55
    }

    metrics['calc5'] = {
        'H2_required': 65665.68, 'H2_available': 39444.77,
        'H2_deficit': 26220.91, 'H2_utilization': 0.6007,
        'total_methanol': 224069.87
    }

    metrics['calc6'] = {
        'methanol_in_gasoline': 79539.50, 'methanol_for_MTO': 144530.37,
        'ethylene_from_MTO': 40468.50, 'propylene_from_MTO': 60702.75,
        'methanol_value': 35792775.30, 'ethylene_value': 16187401.19,
        'propylene_value': 44252308.01, 'phase34_net': 96232484.50
    }

    metrics['summary'] = {
        'phase12_gross': 176064779.38, 'phase12_NG_cost': 76231321.92,
        'phase12_net': 99833457.46, 'phase34_net': 96232484.50,
        'total_net': 196065941.97
    }

    return metrics

# ============================================================================
# CHART GENERATORS - Optimized for readability
# ============================================================================

def create_phase_donut(metrics, lang='en'):
    """Create donut chart for phase distribution."""
    if lang == 'ar':
        labels = ['المرحلة 1+2: استرداد الغاز', 'المرحلة 3+4: الميثانول']
        title = 'توزيع القيمة حسب المرحلة'
    else:
        labels = ['Phase 1+2: Gas Recovery', 'Phase 3+4: Methanol & MTO']
        title = 'Value Distribution by Phase'

    values = [metrics['summary']['phase12_net'], metrics['summary']['phase34_net']]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(colors=['#06b6d4', '#f59e0b'], line=dict(color='white', width=3)),
        textinfo='percent',
        textfont=dict(size=16, color='white', family='Inter'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>',
        direction='clockwise',
        sort=False
    )])

    fig.update_layout(
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5,
                   font=dict(size=12, family='Inter', color='#f1f5f9')),
        annotations=[dict(text=f'<b>${sum(values)/1e6:.0f}M</b>', x=0.5, y=0.5,
                         font=dict(size=28, family='Inter', color='#f1f5f9'), showarrow=False)],
        margin=dict(t=20, b=70, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=320,
        autosize=True
    )

    return fig

def create_product_bars(metrics, lang='en'):
    """Create horizontal bar chart for product values."""
    if lang == 'ar':
        products = ['غاز مسال (LPG)', 'نافثا (C5+)', 'هيدروجين (H2)', 'إيثان (C2)',
                   'ميثانول', 'إيثيلين MTO', 'بروبيلين MTO']
        title = 'قيم المنتجات السنوية'
        xaxis_title = 'القيمة (مليون دولار/سنة)'
    else:
        products = ['LPG (C3+C4)', 'Naphtha (C5+)', 'Hydrogen (H2)', 'Ethane (C2)',
                   'Methanol Blend', 'Ethylene (MTO)', 'Propylene (MTO)']
        title = 'Annual Product Values'
        xaxis_title = 'Value ($ Million/year)'

    values = [
        metrics['calc1']['LPG_value'] / 1e6,
        metrics['calc1']['C5+_value'] / 1e6,
        metrics['calc2']['H2_value'] / 1e6,
        metrics['calc3']['C2_value'] / 1e6,
        metrics['calc6']['methanol_value'] / 1e6,
        metrics['calc6']['ethylene_value'] / 1e6,
        metrics['calc6']['propylene_value'] / 1e6
    ]

    colors = ['#06b6d4', '#06b6d4', '#0ea5e9', '#0ea5e9', '#f59e0b', '#f59e0b', '#f59e0b']

    fig = go.Figure(data=[
        go.Bar(
            y=products,
            x=values,
            orientation='h',
            marker=dict(color=colors, line=dict(width=0)),
            text=[f'${v:.1f}M' for v in values],
            textposition='outside',
            textfont=dict(size=13, family='Inter', color='#f1f5f9'),
            hovertemplate='<b>%{y}</b><br>$%{x:.1f}M<extra></extra>'
        )
    ])

    fig.update_layout(
        xaxis=dict(title=dict(text=xaxis_title, font=dict(size=12, color='#f1f5f9')),
                   tickfont=dict(size=11, color='#f1f5f9'),
                   gridcolor='rgba(255,255,255,0.1)', showgrid=True, range=[0, max(values)*1.35]),
        yaxis=dict(tickfont=dict(size=11, family='Inter', color='#f1f5f9'), autorange='reversed'),
        margin=dict(t=30, b=60, l=120, r=70),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        bargap=0.35,
        autosize=True
    )

    return fig

def create_cost_benefit_bars(metrics, lang='en'):
    """Create grouped bar chart for cost-benefit analysis."""
    if lang == 'ar':
        categories = ['المرحلة 1+2', 'المرحلة 3+4']
        legend_labels = ['القيمة الإجمالية', 'تكلفة الغاز الطبيعي', 'القيمة الصافية']
        title = 'تحليل التكلفة والعائد'
    else:
        categories = ['Phase 1+2', 'Phase 3+4']
        legend_labels = ['Gross Value', 'NG Makeup Cost', 'Net Value']
        title = 'Cost-Benefit Analysis'

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name=legend_labels[0],
        x=categories,
        y=[metrics['summary']['phase12_gross']/1e6, metrics['calc6']['phase34_net']/1e6],
        marker_color='#22c55e',
        text=[f"${metrics['summary']['phase12_gross']/1e6:.0f}M", f"${metrics['calc6']['phase34_net']/1e6:.0f}M"],
        textposition='outside',
        textfont=dict(size=12, color='#f1f5f9')
    ))

    fig.add_trace(go.Bar(
        name=legend_labels[1],
        x=categories,
        y=[metrics['summary']['phase12_NG_cost']/1e6, 0],
        marker_color='#ef4444',
        text=[f"${metrics['summary']['phase12_NG_cost']/1e6:.0f}M", "$0M"],
        textposition='outside',
        textfont=dict(size=12, color='#f1f5f9')
    ))

    fig.add_trace(go.Bar(
        name=legend_labels[2],
        x=categories,
        y=[metrics['summary']['phase12_net']/1e6, metrics['summary']['phase34_net']/1e6],
        marker_color='#0ea5e9',
        text=[f"${metrics['summary']['phase12_net']/1e6:.0f}M", f"${metrics['summary']['phase34_net']/1e6:.0f}M"],
        textposition='outside',
        textfont=dict(size=12, color='#f1f5f9')
    ))

    yaxis_title = 'القيمة (مليون $)' if lang == 'ar' else 'Value ($ Million)'

    fig.update_layout(
        barmode='group',
        legend=dict(orientation='h', yanchor='bottom', y=1.08, xanchor='center', x=0.5,
                   font=dict(size=11, color='#f1f5f9')),
        xaxis=dict(tickfont=dict(size=12, family='Inter', color='#f1f5f9')),
        yaxis=dict(title=dict(text=yaxis_title, font=dict(size=11, color='#f1f5f9')),
                   tickfont=dict(size=10, color='#f1f5f9'), gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(t=80, b=40, l=60, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        bargap=0.25,
        autosize=True
    )

    return fig

def create_sankey(metrics, lang='en'):
    """Create Sankey diagram for material/value flow."""
    if lang == 'ar':
        labels = ['غاز الشعلة', 'غاز المصفاة', 'PSA + كنس', 'بنيكس',
                 'استرداد H2', 'استرداد LPG', 'استرداد C5+', 'استرداد C2',
                 'CO/CO2', 'ميثانول', 'منتجات MTO', 'القيمة الصافية']
    else:
        labels = ['Flare Gas', 'Refinery Gas', 'PSA + Sweep', 'Penex',
                 'H2 Recovery', 'LPG Recovery', 'C5+ Recovery', 'C2 Recovery',
                 'CO/CO2', 'Methanol', 'MTO Products', 'Net Value']

    # Source -> Target connections
    source = [0,0,0, 1,1,1,1, 2,2,2, 3,3,3, 4, 5, 6, 7, 8, 9, 10]
    target = [4,5,6, 4,5,6,7, 4,5,8, 4,5,6, 11, 11, 11, 11, 9, 10, 11]
    value =  [7.5,7.6,7.2, 16,36,11,46, 13,9,25, 2.5,7,2.3, 79, 91, 13, 24, 224, 101, 60]

    node_colors = ['#f97316', '#f97316', '#f97316', '#f97316',
                   '#0ea5e9', '#06b6d4', '#06b6d4', '#0ea5e9',
                   '#8b5cf6', '#f59e0b', '#f59e0b', '#22c55e']

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color='white', width=2),
            label=labels,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color='rgba(100,100,100,0.15)'
        )
    )])

    fig.update_layout(
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        font=dict(size=12, family='Inter', color='#f1f5f9'),
        autosize=True
    )

    return fig

def create_gauge(value, max_val, title, lang='en'):
    """Create a modern gauge chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value * 100,
        number={'suffix': '%', 'font': {'size': 36, 'family': 'Inter', 'color': '#f1f5f9'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': '#f1f5f9',
                    'tickfont': {'size': 10, 'color': '#f1f5f9'}},
            'bar': {'color': '#06b6d4', 'thickness': 0.8},
            'bgcolor': 'rgba(0,0,0,0.05)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239,68,68,0.2)'},
                {'range': [50, 75], 'color': 'rgba(245,158,11,0.2)'},
                {'range': [75, 100], 'color': 'rgba(34,197,94,0.2)'}
            ],
        }
    ))

    fig.update_layout(
        margin=dict(t=20, b=10, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        height=200,
        font=dict(family='Inter', color='#f1f5f9'),
        autosize=True
    )

    return fig

def create_h2_balance(metrics, lang='en'):
    """Create H2 balance visualization."""
    if lang == 'ar':
        categories = ['H2 المتوفر', 'H2 المطلوب', 'العجز']
        title = 'توازن الهيدروجين لإنتاج الميثانول'
    else:
        categories = ['H2 Available', 'H2 Required', 'Deficit']
        title = 'H2 Balance for Methanol'

    values = [metrics['calc5']['H2_available']/1000,
              metrics['calc5']['H2_required']/1000,
              metrics['calc5']['H2_deficit']/1000]
    colors = ['#22c55e', '#0ea5e9', '#ef4444']

    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f'{v:.1f}K' for v in values],
            textposition='outside',
            textfont=dict(size=14, family='Inter', color='#f1f5f9'),
            width=0.6
        )
    ])

    utilization = metrics['calc5']['H2_utilization'] * 100
    fig.add_annotation(
        x=1, y=max(values)*1.1,
        text=f"<b>Utilization: {utilization:.0f}%</b>" if lang == 'en' else f"<b>نسبة الاستخدام: {utilization:.0f}%</b>",
        showarrow=False,
        font=dict(size=14, color='#0ea5e9', family='Inter')
    )

    fig.update_layout(
        yaxis=dict(title=dict(text='Quantity (kt/year)' if lang == 'en' else 'الكمية (ألف طن/سنة)', font=dict(size=10, color='#f1f5f9')),
                   gridcolor='rgba(255,255,255,0.1)', tickfont=dict(size=10, color='#f1f5f9')),
        xaxis=dict(tickfont=dict(size=10, family='Inter', color='#f1f5f9')),
        margin=dict(t=40, b=30, l=50, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        autosize=True
    )

    return fig

def create_stream_heatmap(metrics, lang='en'):
    """Create component distribution heatmap."""
    if lang == 'ar':
        streams = ['شعلة قديم', 'شعلة جديد', 'مصفاة', 'PSA', 'كنس', 'بنيكس']
    else:
        streams = ['Flare OLD', 'Flare New', 'Refinery', 'PSA', 'Sweep', 'Penex']

    components = ['H2', 'CH4', 'C2', 'C3', 'C4', 'C5+', 'CO', 'CO2']

    z = []
    for comp in components:
        row = metrics['stream_components'][comp]
        total = sum(row)
        if total > 0:
            z.append([v/1000 for v in row])  # Convert to thousands
        else:
            z.append([0]*6)

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=streams,
        y=components,
        colorscale='Viridis',
        text=[[f'{v:.0f}' if v > 0 else '' for v in row] for row in z],
        texttemplate='%{text}',
        textfont={"size": 10, "color": "white"},
        hovertemplate='%{y} in %{x}: %{z:.1f}K t/y<extra></extra>',
        colorbar=dict(title=dict(text='kt/y', font=dict(size=11, color='#f1f5f9')), tickfont=dict(size=10, color='#f1f5f9'))
    ))

    fig.update_layout(
        xaxis=dict(tickfont=dict(size=10, family='Inter', color='#f1f5f9'), side='bottom',
                   tickangle=-45),
        yaxis=dict(tickfont=dict(size=10, family='Inter', color='#f1f5f9'), autorange='reversed'),
        margin=dict(t=20, b=60, l=50, r=80),
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        autosize=True
    )

    return fig

def create_methanol_allocation(metrics, lang='en'):
    """Create methanol allocation pie."""
    if lang == 'ar':
        labels = ['مزج البنزين', 'تحويل MTO']
    else:
        labels = ['Gasoline Blending', 'MTO Conversion']

    values = [metrics['calc6']['methanol_in_gasoline'], metrics['calc6']['methanol_for_MTO']]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(colors=['#06b6d4', '#f59e0b'], line=dict(color='white', width=2)),
        textinfo='percent+label',
        textposition='outside',
        textfont=dict(size=12, family='Inter', color='#f1f5f9'),
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} t/y<br>%{percent}<extra></extra>'
    )])

    fig.update_layout(
        showlegend=False,
        margin=dict(t=30, b=30, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        autosize=True
    )

    return fig


# ============================================================================
# HTML GENERATION
# ============================================================================

def generate_stream_cards(metrics):
    """Generate stream detail cards HTML."""
    cards = []
    for i in range(6):
        flow_val = metrics['streams']['flow_ty'][i] / 1000
        card = f'''
        <div class="data-card">
            <div class="data-card-header">{metrics['streams']['names'][i]} <span class="ar-only">({metrics['streams']['names_ar'][i]})</span></div>
            <div class="data-card-value">{flow_val:.1f}K <span style="font-size: 0.8rem; color: var(--gray);">t/y</span></div>
            <div class="data-row"><span>H2</span><span>{metrics['stream_components']['H2'][i]:,.0f} t/y</span></div>
            <div class="data-row"><span>CH4</span><span>{metrics['stream_components']['CH4'][i]:,.0f} t/y</span></div>
            <div class="data-row"><span>C2</span><span>{metrics['stream_components']['C2'][i]:,.0f} t/y</span></div>
            <div class="data-row"><span>C3</span><span>{metrics['stream_components']['C3'][i]:,.0f} t/y</span></div>
            <div class="data-row"><span>C4</span><span>{metrics['stream_components']['C4'][i]:,.0f} t/y</span></div>
            <div class="data-row"><span>C5+</span><span>{metrics['stream_components']['C5+'][i]:,.0f} t/y</span></div>
        </div>
        '''
        cards.append(card)
    return ''.join(cards)

def generate_prices_table(metrics):
    """Generate product prices table rows."""
    rows = []
    for k, v in metrics['prices'].items():
        rows.append(f'<tr><td>{k}</td><td>${v:,}</td></tr>')
    return ''.join(rows)

def generate_html(metrics):
    """Generate the complete modern HTML dashboard."""

    # Pre-generate stream cards and price table
    stream_cards_html = generate_stream_cards(metrics)
    prices_table_html = generate_prices_table(metrics)

    # Pre-generate all charts for both languages
    charts = {
        'en': {
            'donut': create_phase_donut(metrics, 'en'),
            'products': create_product_bars(metrics, 'en'),
            'cost_benefit': create_cost_benefit_bars(metrics, 'en'),
            'sankey': create_sankey(metrics, 'en'),
            'gauge_min': create_gauge(metrics['calc3']['coverage_min'], 100, 'Min Coverage', 'en'),
            'gauge_max': create_gauge(metrics['calc3']['coverage_max'], 100, 'Max Coverage', 'en'),
            'h2_balance': create_h2_balance(metrics, 'en'),
            'heatmap': create_stream_heatmap(metrics, 'en'),
            'methanol': create_methanol_allocation(metrics, 'en')
        },
        'ar': {
            'donut': create_phase_donut(metrics, 'ar'),
            'products': create_product_bars(metrics, 'ar'),
            'cost_benefit': create_cost_benefit_bars(metrics, 'ar'),
            'sankey': create_sankey(metrics, 'ar'),
            'gauge_min': create_gauge(metrics['calc3']['coverage_min'], 100, 'تغطية الحد الأدنى', 'ar'),
            'gauge_max': create_gauge(metrics['calc3']['coverage_max'], 100, 'تغطية الحد الأقصى', 'ar'),
            'h2_balance': create_h2_balance(metrics, 'ar'),
            'heatmap': create_stream_heatmap(metrics, 'ar'),
            'methanol': create_methanol_allocation(metrics, 'ar')
        }
    }

    # Extract values for KPIs
    total_value = metrics['summary']['total_net']
    phase12 = metrics['summary']['phase12_net']
    phase34 = metrics['summary']['phase34_net']

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIDOR-ETHYDCO Integration Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        :root {{
            --primary: #0ea5e9;
            --primary-dark: #0284c7;
            --secondary: #06b6d4;
            --accent: #f59e0b;
            --success: #22c55e;
            --danger: #ef4444;
            --dark: #0f172a;
            --dark-light: #1e293b;
            --gray: #64748b;
            --light: #f1f5f9;
            --white: #ffffff;
            --glass: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            --shadow-sm: 0 10px 40px -10px rgba(0, 0, 0, 0.15);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, var(--dark) 0%, #1a1a2e 50%, var(--dark-light) 100%);
            min-height: 100vh;
            color: var(--white);
            overflow-x: hidden;
        }}

        body.rtl {{
            direction: rtl;
            font-family: 'Cairo', sans-serif;
        }}

        /* Animated background */
        .bg-animation {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }}

        .bg-animation::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 20% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(245, 158, 11, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 40% 40%, rgba(14, 165, 233, 0.1) 0%, transparent 40%);
            animation: rotate 30s linear infinite;
        }}

        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}

        /* Header */
        .header {{
            padding: 30px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(20px);
            background: rgba(15, 23, 42, 0.8);
            border-bottom: 1px solid var(--glass-border);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .logo {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .logo-icon {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 800;
            box-shadow: 0 10px 30px rgba(6, 182, 212, 0.3);
        }}

        .logo-text h1 {{
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--white) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .logo-text span {{
            font-size: 0.85rem;
            color: var(--gray);
        }}

        /* Language Toggle */
        .lang-toggle {{
            display: flex;
            background: var(--glass);
            border-radius: 50px;
            padding: 5px;
            border: 1px solid var(--glass-border);
        }}

        .lang-btn {{
            padding: 10px 25px;
            border: none;
            background: transparent;
            color: var(--gray);
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            border-radius: 50px;
            transition: all 0.3s ease;
            font-family: inherit;
        }}

        .lang-btn.active {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: var(--white);
            box-shadow: 0 5px 20px rgba(6, 182, 212, 0.4);
        }}

        .lang-btn:hover:not(.active) {{
            color: var(--white);
        }}

        /* Navigation */
        .nav {{
            display: flex;
            justify-content: center;
            gap: 10px;
            padding: 20px 50px;
            flex-wrap: wrap;
        }}

        .nav-btn {{
            padding: 14px 28px;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            color: var(--gray);
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            font-family: inherit;
        }}

        .nav-btn:hover {{
            background: rgba(14, 165, 233, 0.2);
            border-color: var(--primary);
            color: var(--white);
            transform: translateY(-2px);
        }}

        .nav-btn.active {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-color: transparent;
            color: var(--white);
            box-shadow: 0 10px 30px rgba(6, 182, 212, 0.3);
        }}

        /* Main Content */
        .content {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 30px 50px 60px;
        }}

        .tab-content {{
            display: none;
            animation: fadeIn 0.5s ease;
        }}

        .tab-content.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* KPI Section */
        .kpi-section {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 25px;
            margin-bottom: 40px;
        }}

        .kpi-card {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 35px;
            position: relative;
            overflow: hidden;
            transition: all 0.4s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow);
            border-color: var(--primary);
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        }}

        .kpi-card.accent::before {{
            background: linear-gradient(90deg, var(--accent) 0%, #fbbf24 100%);
        }}

        .kpi-card.success::before {{
            background: linear-gradient(90deg, var(--success) 0%, #4ade80 100%);
        }}

        .kpi-card.main {{
            grid-row: span 2;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
        }}

        .kpi-label {{
            font-size: 1rem;
            color: var(--gray);
            margin-bottom: 15px;
            font-weight: 500;
        }}

        .kpi-value {{
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--white) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
            margin-bottom: 15px;
        }}

        .kpi-card.main .kpi-value {{
            font-size: 5.5rem;
        }}

        .kpi-sublabel {{
            font-size: 0.9rem;
            color: var(--gray);
        }}

        .kpi-icon {{
            position: absolute;
            top: 25px;
            right: 25px;
            font-size: 2.5rem;
            opacity: 0.15;
        }}

        .rtl .kpi-icon {{
            right: auto;
            left: 25px;
        }}

        /* Chart Cards */
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
            margin-bottom: 30px;
        }}

        .chart-grid.three {{
            grid-template-columns: repeat(3, 1fr);
        }}

        .chart-card {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 25px;
            transition: all 0.4s ease;
        }}

        .chart-card:hover {{
            border-color: var(--primary);
            box-shadow: var(--shadow-sm);
        }}

        .chart-card.full {{
            grid-column: 1 / -1;
        }}

        .chart-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--white);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .chart-title::before {{
            content: '';
            width: 4px;
            height: 20px;
            background: linear-gradient(180deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 2px;
        }}

        /* Data Cards */
        .data-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .data-card {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 25px;
            transition: all 0.3s ease;
        }}

        .data-card:hover {{
            transform: translateY(-3px);
            border-color: var(--secondary);
        }}

        .data-card-header {{
            font-weight: 600;
            font-size: 1rem;
            color: var(--secondary);
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--glass-border);
        }}

        .data-card-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--white);
            margin-bottom: 5px;
        }}

        .data-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px dashed rgba(255,255,255,0.1);
            font-size: 0.9rem;
        }}

        .data-row:last-child {{
            border-bottom: none;
        }}

        .data-row span:first-child {{
            color: var(--gray);
        }}

        .data-row span:last-child {{
            color: var(--white);
            font-weight: 500;
        }}

        /* Gauge Container */
        .gauge-container {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}

        .gauge-card {{
            text-align: center;
        }}

        .gauge-label {{
            font-size: 0.9rem;
            color: var(--gray);
            margin-top: 10px;
        }}

        /* Table Styles */
        .table-container {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 25px;
            overflow-x: auto;
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .data-table th {{
            background: rgba(14, 165, 233, 0.2);
            color: var(--secondary);
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
        }}

        .rtl .data-table th {{
            text-align: right;
        }}

        .data-table td {{
            padding: 15px;
            border-bottom: 1px solid var(--glass-border);
            color: var(--white);
            font-size: 0.9rem;
        }}

        .data-table tr:hover td {{
            background: rgba(255,255,255,0.05);
        }}

        .data-table .value {{
            color: var(--success);
            font-weight: 600;
        }}

        .data-table .cost {{
            color: var(--danger);
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px;
            color: var(--gray);
            font-size: 0.85rem;
        }}

        /* Responsive */
        @media (max-width: 1200px) {{
            .kpi-section {{
                grid-template-columns: 1fr 1fr;
            }}
            .kpi-card.main {{
                grid-column: 1 / -1;
                grid-row: auto;
            }}
            .chart-grid.three {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (max-width: 900px) {{
            .header {{
                padding: 20px 25px;
                flex-direction: column;
                gap: 20px;
            }}
            .content {{
                padding: 20px 25px 40px;
            }}
            .chart-grid {{
                grid-template-columns: 1fr;
            }}
            .chart-grid.three {{
                grid-template-columns: 1fr;
            }}
            .kpi-section {{
                grid-template-columns: 1fr;
            }}
            .kpi-card.main .kpi-value {{
                font-size: 3.5rem;
            }}
            .nav {{
                padding: 15px 20px;
            }}
            .nav-btn {{
                padding: 12px 20px;
                font-size: 0.85rem;
            }}
            .gauge-container {{
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }}
            .data-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Mobile phones */
        @media (max-width: 480px) {{
            .header {{
                padding: 15px;
                gap: 15px;
            }}
            .logo-text h1 {{
                font-size: 1.2rem;
            }}
            .logo-text span {{
                font-size: 0.75rem;
            }}
            .logo-icon {{
                width: 40px;
                height: 40px;
                font-size: 20px;
            }}
            .lang-toggle {{
                width: 100%;
                justify-content: center;
            }}
            .lang-btn {{
                padding: 8px 20px;
                font-size: 0.85rem;
            }}
            .nav {{
                padding: 10px 15px;
                gap: 8px;
            }}
            .nav-btn {{
                padding: 10px 14px;
                font-size: 0.8rem;
                border-radius: 10px;
            }}
            .content {{
                padding: 15px 15px 30px;
            }}
            .kpi-card {{
                padding: 20px;
                border-radius: 16px;
            }}
            .kpi-card.main .kpi-value {{
                font-size: 2.8rem;
            }}
            .kpi-value {{
                font-size: 2.5rem;
            }}
            .kpi-label {{
                font-size: 0.9rem;
            }}
            .kpi-sublabel {{
                font-size: 0.8rem;
            }}
            .kpi-icon {{
                font-size: 2rem;
                top: 15px;
                right: 15px;
            }}
            .chart-card {{
                padding: 15px;
                border-radius: 16px;
            }}
            .chart-title {{
                font-size: 1rem;
                margin-bottom: 15px;
            }}
            .gauge-container {{
                grid-template-columns: 1fr;
                gap: 15px;
            }}
            .gauge-label {{
                font-size: 0.8rem;
            }}
            .data-card {{
                padding: 20px;
                border-radius: 16px;
            }}
            .data-card-header {{
                font-size: 0.9rem;
            }}
            .data-card-value {{
                font-size: 1.6rem;
            }}
            .data-row {{
                font-size: 0.85rem;
            }}
            .table-container {{
                padding: 15px;
                border-radius: 16px;
                overflow-x: auto;
            }}
            .data-table th,
            .data-table td {{
                padding: 10px 8px;
                font-size: 0.8rem;
            }}
            .footer {{
                padding: 25px 15px;
                font-size: 0.75rem;
            }}
        }}

        /* Extra small phones */
        @media (max-width: 360px) {{
            .kpi-card.main .kpi-value {{
                font-size: 2.2rem;
            }}
            .kpi-value {{
                font-size: 2rem;
            }}
            .nav-btn {{
                padding: 8px 10px;
                font-size: 0.75rem;
            }}
        }}

        /* Hide elements based on language */
        .en-only {{ display: block; }}
        .ar-only {{ display: none; }}
        .rtl .en-only {{ display: none; }}
        .rtl .ar-only {{ display: block; }}
    </style>
</head>
<body>
    <div class="bg-animation"></div>

    <header class="header">
        <div class="logo">
            <div class="logo-icon">M</div>
            <div class="logo-text">
                <h1 class="en-only">MIDOR-ETHYDCO Integration</h1>
                <h1 class="ar-only">تكامل ميدور وإيثيدكو</h1>
                <span class="en-only">Petrochemical Integration Analysis</span>
                <span class="ar-only">تحليل التكامل البتروكيماوي</span>
            </div>
        </div>
        <div class="lang-toggle">
            <button class="lang-btn active" onclick="setLanguage('en')">English</button>
            <button class="lang-btn" onclick="setLanguage('ar')">العربية</button>
        </div>
    </header>

    <nav class="nav">
        <button class="nav-btn active" onclick="showTab('overview')">
            <span class="en-only">Overview</span>
            <span class="ar-only">نظرة عامة</span>
        </button>
        <button class="nav-btn" onclick="showTab('financial')">
            <span class="en-only">Financial Analysis</span>
            <span class="ar-only">التحليل المالي</span>
        </button>
        <button class="nav-btn" onclick="showTab('process')">
            <span class="en-only">Process Flow</span>
            <span class="ar-only">تدفق العمليات</span>
        </button>
        <button class="nav-btn" onclick="showTab('detailed')">
            <span class="en-only">Detailed Data</span>
            <span class="ar-only">البيانات التفصيلية</span>
        </button>
    </nav>

    <main class="content">
        <!-- OVERVIEW TAB -->
        <div id="overview" class="tab-content active">
            <div class="kpi-section">
                <div class="kpi-card main">
                    <div class="kpi-label en-only">Total Annual Integration Value</div>
                    <div class="kpi-label ar-only">إجمالي قيمة التكامل السنوية</div>
                    <div class="kpi-value">${total_value/1e6:.0f}M</div>
                    <div class="kpi-sublabel en-only">Net value after all costs</div>
                    <div class="kpi-sublabel ar-only">القيمة الصافية بعد جميع التكاليف</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon">⚡</div>
                    <div class="kpi-label en-only">Phase 1+2: Gas Recovery</div>
                    <div class="kpi-label ar-only">المرحلة 1+2: استرداد الغاز</div>
                    <div class="kpi-value">${phase12/1e6:.0f}M</div>
                    <div class="kpi-sublabel en-only">LPG, H2, C2, C5+ Recovery</div>
                    <div class="kpi-sublabel ar-only">استرداد الغاز المسال والهيدروجين</div>
                </div>
                <div class="kpi-card accent">
                    <div class="kpi-icon">🧪</div>
                    <div class="kpi-label en-only">Phase 3+4: Methanol & MTO</div>
                    <div class="kpi-label ar-only">المرحلة 3+4: الميثانول</div>
                    <div class="kpi-value">${phase34/1e6:.0f}M</div>
                    <div class="kpi-sublabel en-only">Methanol Blending & Olefins</div>
                    <div class="kpi-sublabel ar-only">مزج الميثانول والأوليفينات</div>
                </div>
            </div>

            <div class="chart-grid">
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">Value Distribution</span>
                        <span class="ar-only">توزيع القيمة</span>
                    </div>
                    <div id="chart-donut-en"></div>
                    <div id="chart-donut-ar"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">Product Values</span>
                        <span class="ar-only">قيم المنتجات</span>
                    </div>
                    <div id="chart-products-en"></div>
                    <div id="chart-products-ar"></div>
                </div>
            </div>
        </div>

        <!-- FINANCIAL TAB -->
        <div id="financial" class="tab-content">
            <div class="chart-grid">
                <div class="chart-card full">
                    <div class="chart-title">
                        <span class="en-only">Cost-Benefit Analysis</span>
                        <span class="ar-only">تحليل التكلفة والعائد</span>
                    </div>
                    <div id="chart-costbenefit-en"></div>
                    <div id="chart-costbenefit-ar"></div>
                </div>
            </div>

            <div class="table-container">
                <div class="chart-title">
                    <span class="en-only">Financial Summary</span>
                    <span class="ar-only">الملخص المالي</span>
                </div>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th class="en-only">Product</th>
                            <th class="ar-only">المنتج</th>
                            <th class="en-only">Quantity (t/y)</th>
                            <th class="ar-only">الكمية (طن/سنة)</th>
                            <th class="en-only">Value ($/y)</th>
                            <th class="ar-only">القيمة ($/سنة)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>LPG (C3+C4)</td>
                            <td>{metrics['calc1']['total_LPG']:,.0f}</td>
                            <td class="value">${metrics['calc1']['LPG_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>C5+ (Naphtha)</td>
                            <td>{metrics['calc1']['total_C5+']:,.0f}</td>
                            <td class="value">${metrics['calc1']['C5+_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>Hydrogen (H2)</td>
                            <td>{metrics['calc2']['total_H2']:,.0f}</td>
                            <td class="value">${metrics['calc2']['H2_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>Ethane (C2)</td>
                            <td>{metrics['calc3']['MIDOR_C2_supply']:,.0f}</td>
                            <td class="value">${metrics['calc3']['C2_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>Methanol Blend</td>
                            <td>{metrics['calc6']['methanol_in_gasoline']:,.0f}</td>
                            <td class="value">${metrics['calc6']['methanol_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>Ethylene (MTO)</td>
                            <td>{metrics['calc6']['ethylene_from_MTO']:,.0f}</td>
                            <td class="value">${metrics['calc6']['ethylene_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>Propylene (MTO)</td>
                            <td>{metrics['calc6']['propylene_from_MTO']:,.0f}</td>
                            <td class="value">${metrics['calc6']['propylene_value']:,.0f}</td>
                        </tr>
                        <tr style="background: rgba(239,68,68,0.1);">
                            <td><strong class="en-only">NG Makeup Cost</strong><strong class="ar-only">تكلفة الغاز الطبيعي</strong></td>
                            <td>-</td>
                            <td class="cost">-${metrics['summary']['phase12_NG_cost']:,.0f}</td>
                        </tr>
                        <tr style="background: rgba(34,197,94,0.2);">
                            <td><strong class="en-only">TOTAL NET VALUE</strong><strong class="ar-only">إجمالي القيمة الصافية</strong></td>
                            <td>-</td>
                            <td class="value"><strong>${metrics['summary']['total_net']:,.0f}</strong></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- PROCESS TAB -->
        <div id="process" class="tab-content">
            <div class="chart-grid">
                <div class="chart-card full">
                    <div class="chart-title">
                        <span class="en-only">Material & Value Flow</span>
                        <span class="ar-only">تدفق المواد والقيمة</span>
                    </div>
                    <div id="chart-sankey-en"></div>
                    <div id="chart-sankey-ar"></div>
                </div>
            </div>

            <div class="chart-grid">
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">ETHYDCO C2 Feed Coverage</span>
                        <span class="ar-only">تغطية تغذية الإيثان لإيثيدكو</span>
                    </div>
                    <div class="gauge-container">
                        <div class="gauge-card">
                            <div id="chart-gauge-min-en"></div>
                            <div id="chart-gauge-min-ar"></div>
                            <div class="gauge-label en-only">Min Demand Coverage</div>
                            <div class="gauge-label ar-only">تغطية الحد الأدنى</div>
                        </div>
                        <div class="gauge-card">
                            <div id="chart-gauge-max-en"></div>
                            <div id="chart-gauge-max-ar"></div>
                            <div class="gauge-label en-only">Max Demand Coverage</div>
                            <div class="gauge-label ar-only">تغطية الحد الأقصى</div>
                        </div>
                    </div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">H2 Balance for Methanol</span>
                        <span class="ar-only">توازن الهيدروجين للميثانول</span>
                    </div>
                    <div id="chart-h2-en"></div>
                    <div id="chart-h2-ar"></div>
                </div>
            </div>

            <div class="chart-grid">
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">Stream Component Distribution</span>
                        <span class="ar-only">توزيع مكونات التيارات</span>
                    </div>
                    <div id="chart-heatmap-en"></div>
                    <div id="chart-heatmap-ar"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">Methanol Allocation</span>
                        <span class="ar-only">توزيع الميثانول</span>
                    </div>
                    <div id="chart-methanol-en"></div>
                    <div id="chart-methanol-ar"></div>
                </div>
            </div>
        </div>

        <!-- DETAILED TAB -->
        <div id="detailed" class="tab-content">
            <div class="chart-title" style="margin-bottom: 20px; font-size: 1.3rem;">
                <span class="en-only">Stream Details</span>
                <span class="ar-only">تفاصيل التيارات</span>
            </div>

            <div class="data-grid">
                {stream_cards_html}
            </div>

            <div class="table-container" style="margin-top: 30px;">
                <div class="chart-title">
                    <span class="en-only">Product Prices</span>
                    <span class="ar-only">أسعار المنتجات</span>
                </div>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th class="en-only">Product</th>
                            <th class="ar-only">المنتج</th>
                            <th class="en-only">Price ($/ton)</th>
                            <th class="ar-only">السعر ($/طن)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {prices_table_html}
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <footer class="footer">
        <span class="en-only">MIDOR-ETHYDCO Integration Analysis | Generated: {pd.Timestamp.now().strftime('%Y-%m-%d')}</span>
        <span class="ar-only">تحليل التكامل بين ميدور وإيثيدكو | تاريخ الإنشاء: {pd.Timestamp.now().strftime('%Y-%m-%d')}</span>
    </footer>

    <script>
        // Chart data
        var chartsEN = {{
            donut: {charts['en']['donut'].to_json()},
            products: {charts['en']['products'].to_json()},
            costbenefit: {charts['en']['cost_benefit'].to_json()},
            sankey: {charts['en']['sankey'].to_json()},
            gaugeMin: {charts['en']['gauge_min'].to_json()},
            gaugeMax: {charts['en']['gauge_max'].to_json()},
            h2: {charts['en']['h2_balance'].to_json()},
            heatmap: {charts['en']['heatmap'].to_json()},
            methanol: {charts['en']['methanol'].to_json()}
        }};

        var chartsAR = {{
            donut: {charts['ar']['donut'].to_json()},
            products: {charts['ar']['products'].to_json()},
            costbenefit: {charts['ar']['cost_benefit'].to_json()},
            sankey: {charts['ar']['sankey'].to_json()},
            gaugeMin: {charts['ar']['gauge_min'].to_json()},
            gaugeMax: {charts['ar']['gauge_max'].to_json()},
            h2: {charts['ar']['h2_balance'].to_json()},
            heatmap: {charts['ar']['heatmap'].to_json()},
            methanol: {charts['ar']['methanol'].to_json()}
        }};

        var config = {{responsive: true, displayModeBar: false}};
        var currentLang = 'en';

        function renderCharts(lang) {{
            var charts = lang === 'ar' ? chartsAR : chartsEN;
            var suffix = '-' + lang;
            var otherSuffix = lang === 'ar' ? '-en' : '-ar';

            // Hide other language charts
            document.querySelectorAll('[id$="' + otherSuffix + '"]').forEach(el => el.style.display = 'none');
            document.querySelectorAll('[id$="' + suffix + '"]').forEach(el => el.style.display = 'block');

            Plotly.newPlot('chart-donut' + suffix, charts.donut.data, charts.donut.layout, config);
            Plotly.newPlot('chart-products' + suffix, charts.products.data, charts.products.layout, config);
            Plotly.newPlot('chart-costbenefit' + suffix, charts.costbenefit.data, charts.costbenefit.layout, config);
            Plotly.newPlot('chart-sankey' + suffix, charts.sankey.data, charts.sankey.layout, config);
            Plotly.newPlot('chart-gauge-min' + suffix, charts.gaugeMin.data, charts.gaugeMin.layout, config);
            Plotly.newPlot('chart-gauge-max' + suffix, charts.gaugeMax.data, charts.gaugeMax.layout, config);
            Plotly.newPlot('chart-h2' + suffix, charts.h2.data, charts.h2.layout, config);
            Plotly.newPlot('chart-heatmap' + suffix, charts.heatmap.data, charts.heatmap.layout, config);
            Plotly.newPlot('chart-methanol' + suffix, charts.methanol.data, charts.methanol.layout, config);
        }}

        function setLanguage(lang) {{
            currentLang = lang;
            document.body.classList.toggle('rtl', lang === 'ar');

            // Update toggle buttons
            document.querySelectorAll('.lang-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.textContent.includes(lang === 'ar' ? 'العربية' : 'English'));
            }});

            renderCharts(lang);
            window.dispatchEvent(new Event('resize'));
        }}

        function showTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));

            document.getElementById(tabId).classList.add('active');
            event.target.closest('.nav-btn').classList.add('active');

            setTimeout(() => window.dispatchEvent(new Event('resize')), 100);
        }}

        // Initial render
        renderCharts('en');
    </script>
</body>
</html>
'''

    return html

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("Loading metrics...")
    metrics = load_metrics()

    print("Generating modern dashboard...")
    html = generate_html(metrics)

    print("Writing HTML file...")
    with open('integration_dashboard_v2.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("\n" + "="*60)
    print("Dashboard V2 generated successfully!")
    print("="*60)
    print("\nOutput: integration_dashboard_v2.html")
    print("\nFeatures:")
    print("  - Modern dark glassmorphism design")
    print("  - Language toggle (English/Arabic)")
    print("  - Animated background")
    print("  - Responsive layout")
    print("  - Clean, readable charts")

if __name__ == '__main__':
    main()
