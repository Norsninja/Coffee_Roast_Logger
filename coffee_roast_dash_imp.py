import dash
from dash import dcc, html
import dash.dependencies as dd
import pandas as pd
import plotly.graph_objs as go
import os
import re

# Load and preprocess the data
folder_path = 'roasting_data'
all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

# Concatenate all roast data into a single DataFrame
roast_data_list = []
metadata_list = []
for file in all_files:
    with open(file, 'r') as f:
        lines = f.readlines()
        # Extract metadata from comment lines
        metadata = {}
        for line in lines:
            if line.startswith('#'):
                match = re.match(r'# (.*?): (.*)', line)
                if match:
                    key, value = match.groups()
                    metadata[key] = value
            else:
                break
        # Skip comment lines that start with '#'
        data_start_idx = next(i for i, line in enumerate(lines) if not line.startswith('#'))
        data = pd.read_csv(file, skiprows=data_start_idx)
    roast_name = os.path.splitext(os.path.basename(file))[0]
    data['Roast Name'] = roast_name
    metadata['Roast Name'] = roast_name
    roast_data_list.append(data)
    metadata_list.append(metadata)

roast_data = pd.concat(roast_data_list, ignore_index=True)
metadata_df = pd.DataFrame(metadata_list)

# Rename 'Minute' column to 'Time' for consistency
roast_data.rename(columns={'Minute': 'Time'}, inplace=True)

# Convert 'Time' column to numeric, dropping NaN values
roast_data['Time'] = pd.to_numeric(roast_data['Time'], errors='coerce').fillna(0).astype(int)

# Calculate Rate of Change for Bean Temperature and Exhaust Temperature
roast_data['RoC_Bt'] = roast_data['Bean Temperature (Bt)'].diff()
roast_data['RoC_Bt_Smoothed'] = roast_data['RoC_Bt'].rolling(window=3, min_periods=1).mean()  # Smoothing the RoR to reduce noise
roast_data['RoC_Et'] = roast_data['Exhaust Temperature (Et)'].diff()

# Calculate weight loss
metadata_df['Start Weight'] = pd.to_numeric(metadata_df['Start Weight'].str.replace('g', '').str.strip(), errors='coerce')
metadata_df['End Weight'] = pd.to_numeric(metadata_df['End Weight'].str.replace('g', '').str.strip(), errors='coerce')
metadata_df['Weight Loss (%)'] = ((metadata_df['Start Weight'] - metadata_df['End Weight']) / metadata_df['Start Weight']) * 100

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1('Artisan-Style Coffee Roast Dashboard', style={'textAlign': 'center', 'color': '#D8DEE9'}),
    
    html.Label('Select Roast(s):', style={'color': '#D8DEE9'}),
    dcc.Dropdown(
        id='roast-selector',
        options=[{'label': roast, 'value': roast} for roast in roast_data['Roast Name'].unique()],
        value=[roast_data['Roast Name'].unique()[0]],
        multi=True,
        style={'backgroundColor': '#2E3440', 'color': '#D8DEE9'}
    ),
    
    dcc.Graph(id='combined-graph', config={'displayModeBar': False}),
    html.Div(id='weight-loss-info', style={'color': '#D8DEE9', 'marginTop': '20px'}),
    html.Div(id='fan-heat-settings', style={'color': '#D8DEE9', 'marginTop': '20px'})
], style={'backgroundColor': '#2E3440', 'padding': '10px'})

# Callbacks for interactivity
@app.callback(
    [
        dd.Output('combined-graph', 'figure'),
        dd.Output('weight-loss-info', 'children'),
        dd.Output('fan-heat-settings', 'children')
    ],
    [dd.Input('roast-selector', 'value')]
)
def update_graphs(selected_roasts):
    # Define color palette for better differentiation
    color_palette = [
        ('#5E81AC', '#88C0D0'),  # Blue shades
        ('#BF616A', '#D08770'),  # Red-orange shades
        ('#A3BE8C', '#B48EAD'),  # Green and Purple shades
        ('#EBCB8B', '#D8DEE9'),  # Yellow and Light shades
        ('#81A1C1', '#8FBCBB')   # Blue-green shades
    ]
    
    # Filter data based on selected roasts
    filtered_data = roast_data[roast_data['Roast Name'].isin(selected_roasts)]
    filtered_metadata = metadata_df[metadata_df['Roast Name'].isin(selected_roasts)]
    
    # Combined Graph: Temperature and Rate of Change
    combined_traces = []
    markers = []
    for idx, roast in enumerate(selected_roasts):
        roast_data_filtered = filtered_data[filtered_data['Roast Name'] == roast]
        # Add initial data point for temperature starting at room temperature at minute 0
        room_temp = 68  # Assuming room temperature is 68°F
        roast_data_filtered = pd.concat([pd.DataFrame({'Time': [0], 'Bean Temperature (Bt)': [room_temp], 'Exhaust Temperature (Et)': [room_temp], 'Fan Power': [0], 'Heat Setting': [0], 'RoC_Bt': [0], 'RoC_Bt_Smoothed': [0], 'Roast Name': [roast]}), roast_data_filtered], ignore_index=True)
        color_bt, color_et = color_palette[idx % len(color_palette)]
        temp_trace_bt = go.Scatter(x=roast_data_filtered['Time'], y=roast_data_filtered['Bean Temperature (Bt)'], mode='lines', name=f'Bean Temperature (Bt) - {roast}', line=dict(color=color_bt))
        temp_trace_et = go.Scatter(x=roast_data_filtered['Time'], y=roast_data_filtered['Exhaust Temperature (Et)'], mode='lines', name=f'Exhaust Temperature (Et) - {roast}', line=dict(color=color_et, dash='dot'))
        roc_trace_bt = go.Scatter(x=roast_data_filtered['Time'], y=roast_data_filtered['RoC_Bt'], mode='lines', name=f'Rate of Change (Bt) - {roast}', line=dict(color=color_et))
        roc_trace_bt_smooth = go.Scatter(x=roast_data_filtered['Time'], y=roast_data_filtered['RoC_Bt_Smoothed'], mode='lines', name=f'Smoothed Rate of Change (Bt) - {roast}', line=dict(color=color_et, dash='dash'))
        combined_traces.extend([temp_trace_bt, temp_trace_et, roc_trace_bt, roc_trace_bt_smooth])

        # Add markers for First Crack and Cooling Start
        roast_metadata = filtered_metadata[filtered_metadata['Roast Name'] == roast].iloc[0]
        fc_start = roast_metadata.get('First Crack Start')
        fc_end = roast_metadata.get('First Crack End')
        cooling_start = roast_metadata.get('Cooling Start')
        
        if fc_start:
            markers.append(go.Scatter(
                x=[int(fc_start.split(':')[0])],
                y=[roast_data_filtered['Bean Temperature (Bt)'].max()],
                mode='markers',
                marker=dict(size=10, color=color_bt, symbol='circle'),
                name=f'First Crack Start - {roast}'
            ))
        if fc_end:
            markers.append(go.Scatter(
                x=[int(fc_end.split(':')[0])],
                y=[roast_data_filtered['Bean Temperature (Bt)'].max()],
                mode='markers',
                marker=dict(size=10, color=color_bt, symbol='triangle-up'),
                name=f'First Crack End - {roast}'
            ))
        if cooling_start:
            markers.append(go.Scatter(
                x=[int(cooling_start.split(':')[0])],
                y=[roast_data_filtered['Bean Temperature (Bt)'].max()],
                mode='markers',
                marker=dict(size=10, color=color_bt, symbol='square'),
                name=f'Cooling Start - {roast}'
            ))
    
    # Adding shaded roasting phases based on temperature ranges
    max_time = roast_data_filtered['Time'].max()
    shading_shapes = []
    for idx, roast in enumerate(selected_roasts):
        roast_data_filtered = filtered_data[filtered_data['Roast Name'] == roast]
        # Determine phase ranges based on temperature profiles
        drying_end_time = roast_data_filtered[roast_data_filtered['Bean Temperature (Bt)'] >= 375]['Time'].min()
        maillard_end_time = roast_data_filtered[roast_data_filtered['Bean Temperature (Bt)'] >= 395]['Time'].min()
        development_end_time = roast_data_filtered[roast_data_filtered['Bean Temperature (Bt)'] >= 400]['Time'].min()

        if not pd.isna(drying_end_time):
            shading_shapes.append(
                dict(
                    type='rect',
                    xref='x',
                    yref='paper',
                    x0=0,
                    y0=0,
                    x1=drying_end_time,
                    y1=1,
                    fillcolor='rgba(94, 129, 172, 0.2)',
                    layer='below',
                    line_width=0,
                    name='Drying Phase'
                )
            )
        if not pd.isna(maillard_end_time):
            shading_shapes.append(
                dict(
                    type='rect',
                    xref='x',
                    yref='paper',
                    x0=drying_end_time,
                    y0=0,
                    x1=maillard_end_time,
                    y1=1,
                    fillcolor='rgba(191, 97, 106, 0.2)',
                    layer='below',
                    line_width=0,
                    name='Maillard Reaction'
                )
            )
        if not pd.isna(development_end_time):
            shading_shapes.append(
                dict(
                    type='rect',
                    xref='x',
                    yref='paper',
                    x0=maillard_end_time,
                    y0=0,
                    x1=max_time,
                    y1=1,
                    fillcolor='rgba(163, 190, 140, 0.2)',
                    layer='below',
                    line_width=0,
                    name='Development Phase'
                )
            )
    
    combined_layout = go.Layout(
        title='Temperature and Rate of Change Over Time',
        xaxis={'title': 'Time (min)', 'color': '#D8DEE9'},
        yaxis={'title': 'Temperature (°F) / Rate of Change (°F/min)', 'color': '#D8DEE9'},
        plot_bgcolor='#3B4252',
        paper_bgcolor='#2E3440',
        font=dict(color='#D8DEE9'),
        shapes=shading_shapes
    )
    combined_figure = go.Figure(data=combined_traces + markers, layout=combined_layout)

    # Weight loss information
    weight_loss_info = []
    for idx, roast in enumerate(selected_roasts):
        roast_metadata = filtered_metadata[filtered_metadata['Roast Name'] == roast].iloc[0]
        weight_loss = roast_metadata.get('Weight Loss (%)')
        if weight_loss is not None:
            weight_loss_info.append(f"{roast}: Weight Loss = {weight_loss:.2f}%")

    # Fan and Heat Settings Information
    fan_heat_info = []
    for idx, roast in enumerate(selected_roasts):
        roast_data_filtered = filtered_data[filtered_data['Roast Name'] == roast]
        fan_settings = roast_data_filtered['Fan Power'].tolist()
        heat_settings = roast_data_filtered['Heat Setting'].tolist()
        fan_heat_info.append(html.Div([
            html.H4(f"{roast} Fan and Heat Settings", style={'marginBottom': '5px'}),
            html.Div([
                html.Div([
                    html.Div(f"Time {i+1} min: Fan = {fan}, Heat = {heat}", style={'marginBottom': '2px'})
                    for i, (fan, heat) in enumerate(zip(fan_settings, heat_settings))
                ])
            ], style={'marginBottom': '10px'})
        ]))

    return [combined_figure, html.Div(weight_loss_info), html.Div(fan_heat_info)]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)