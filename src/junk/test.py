import plotly
from plotly.graph_objs import Bar, Layout


trace1 = Bar(
    x=['giraffes', 'orangutans', 'monkeys'],
    y=[20, 14, 23],
    name='SF Zoo'
)
trace2 = Bar(
    x=['giraffes', 'orangutans', 'monkeys'],
    y=[12, 18, 29],
    name='LA Zoo'
)

data = [trace1, trace2]
layout = Layout(
    barmode='group'
)

plotly.offline.plot({
    "data": data,
    "layout": layout
}, auto_open=False, show_link=False, filename='visualize.html')