"""
Color palette and Plotly styling helpers for the Streamlit dashboard (dark theme).
Kept separate from chart_style.py (used by the notebooks, light theme).
"""

# Brighter/lighter steps than a light-theme palette would use, for contrast
# against the dark surface.
PRIMARY = '#818CF8'   # indigo
CYAN = '#22D3EE'
AMBER = '#FBBF24'
ROSE = '#FB7185'
EMERALD = '#34D399'
VIOLET = '#A78BFA'
PINK = '#F472B6'
LIME = '#A3E635'

CATEGORICAL = [PRIMARY, CYAN, AMBER, ROSE, EMERALD, VIOLET, PINK, LIME]

REGION_COLORS = {
    'Central': PRIMARY,
    'East': CYAN,
    'South': EMERALD,
    'West': AMBER,
}

CATEGORY_COLORS = {
    'Furniture': PRIMARY,
    'Office Supplies': CYAN,
    'Technology': AMBER,
}

# Dark surfaces
BG = '#0F172A'          # page background (slate-900)
CARD_BG = '#1E293B'      # card background (slate-800)
TEXT_PRIMARY = '#F1F5F9'  # slate-100
TEXT_SECONDARY = '#94A3B8'  # slate-400
GRID = '#334155'        # slate-700
BORDER = 'rgba(255,255,255,0.08)'

# Dark-surface gradient, for "ranked magnitude" bar charts (dim -> bright indigo).
GRADIENT_INDIGO = [[0, '#312E81'], [1, PRIMARY]]


def style_fig(fig, height=380, showlegend=False):
    """Apply consistent, modern dark-theme styling to a Plotly figure."""
    fig.update_layout(
        template='plotly_dark',
        font=dict(family='Inter, sans-serif', color=TEXT_PRIMARY, size=13),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        height=height,
        showlegend=showlegend,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                     font=dict(color=TEXT_PRIMARY)),
        hoverlabel=dict(bgcolor=CARD_BG, font_size=13, font_family='Inter',
                          font_color=TEXT_PRIMARY, bordercolor=GRID),
        hovermode='x unified',
    )
    fig.update_xaxes(showgrid=False, showline=True, linecolor=GRID, ticks='',
                      color=TEXT_SECONDARY)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, ticks='',
                      color=TEXT_SECONDARY)
    return fig
