# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 21:06:48 2022

@author: jacob

Dash app for mantarray data handling v0.0.2

colours : #00263e - Blue, #19ac8a - Green
"""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, ctx, dash_table
from scipy import stats

import pandas as pd
import os
import plotly.express as px
import pingouin as pg

### ------------------ styles and required definitions ---------------------###
wells = [f'{row}{column}' for column in (1,2,3,4,5,6) for row in ('A','B','C','D')]

app = Dash(__name__)

tabs_styles = {
    'height': '5px'
}
tab_style = {
    'padding': '10px',
    'fontWeight': 'bold',
}

tab_selected_style = {
    'borderTop': '5px solid #19ac8a',
    'backgroundColor': '#00263e',
    'color': 'white',
    'fontWeight': 'bold',
    'padding': '10px'
}

# add left panel, main panel, button, input and dropdown styles here for consistency


###-------------------------------DASH APP----------------------------------###

app.layout = html.Div([
    # header 
    html.Div([
        html.H1(children='Mantarry Analysis Tools', 
                style = {'padding' : 10,})
        ],style = {'backgroundColor' : '#00263e', 
                   'color' : 'white',
                   'borderTop': '5px solid #19ac8a'}),
    
    # Data import tab ---------------------------------------------------------
    dcc.Tabs([
        dcc.Tab(label='Data import', children = [
            # main body
            html.Div(children=[
                # left panel
                html.Div([
                    html.H1(children='Group Definitions'),
                     
                    html.Label('Input directory'),
                    dcc.Input(value='"G:\My Drive\Software\R scripts\Shiny\Data handling\Data_handling - v2.1"',
                              type='text',
                              style = {'width' : '93%',  'padding' : 10},
                              id='Input-files'),
                    
                    html.Br(),
                    html.Label('Choose descriptor'),
                    dcc.Dropdown(['Mean', 'Min', 'Max'], 
                                 'Mean',
                                 style={'color':'black'},
                                 id='Choose-descriptor'),
                    
                    html.Br(),
                    html.Label('Group 1'),
                    dcc.Dropdown(wells,
                                 ['A1','A2','A3','A4','A5'], # these are defaults simply for testing purposes
                                 multi=True,
                                 id='Grp1',
                                 style={'color' : 'black'}),
                    html.Br(),
                    html.Label('Group 2'),
                    dcc.Dropdown(wells,
                                 ['B1','B2','B3','B4','B5'], # these are defaults simply for testing purposes
                                 multi=True,
                                 id='Grp2',
                                 style={'color' : 'black'}),
                    html.Br(),
                    html.Label('Group 3'),
                    dcc.Dropdown(wells,
                                 multi=True,
                                 id='Grp3',
                                 style={'color' : 'black'}), 
                    html.Br(),
                    html.Label('Group 4'),
                    dcc.Dropdown(wells,
                                 multi=True,
                                 id='Grp4',
                                 style={'color' : 'black'}), 
                    html.Br(),
                    html.Label('Group 5'),
                    dcc.Dropdown(wells,
                                 multi=True,
                                 id='Grp5',
                                 style={'color' : 'black'}), 
                    html.Br(),
                    html.Label('Group 6'),
                    dcc.Dropdown(wells,
                                 multi=True,
                                 id='Grp6',
                                 style={'color' : 'black'}),
                    
                    html.Br(),
                    html.Label('Define group names'),
                    html.Br(),
                    dcc.Input(value='Electrical Stim,Control', 
                              type='text',
                              id='Group-names',
                              style = {'width' : '93%', 'padding' : 10}),
                    
                    html.Br(),
                    html.Label('Timepoints - Enter numbers only'),
                    html.Br(),
                    dcc.Input(value='21,24,28,33,35,40', 
                              type='text', 
                              id='Timepoints',
                              style = {'width' : '93%',  'padding' : 10}
                              ),
                    
                    html.Br(),
                    html.Button('Compute',
                                n_clicks=0,
                                id='Compute-button',
                                style={'width' : '100%',
                                       'padding' : 10,
                                       'margin-top' : '30px',
                                       'borderRadius' : '10px',
                                       'textAlign': 'center',
                                       'font-weight' : 'bold'}
                                ),
                    html.Br(),
                    html.Button('Download Raw Data',
                                id='raw-data-download-button',
                                style={'width' : '48%',
                                       'height' : '50px',
                                       'padding' : 10,
                                       'margin-top' : '30px',
                                       'margin-right' : '4%',
                                       'borderRadius' : '10px',
                                       'textAlign': 'center',
                                       'font-weight' : 'bold'}
                                ),
                    dcc.Download(id='raw-data-download'),
                    
                    html.Button('Download Summary Data',
                                id='summary-data-download-button',
                                style={'width' : '48%',
                                       'height' : '50px',
                                       'padding' : 10,
                                       'margin-top' : '30px',
                                       'borderRadius' : '10px',
                                       'textAlign': 'center',
                                       'font-weight' : 'bold'}
                                ),                 
                    dcc.Download(id='summary-data-download'),

                ], style = {'flex' : .2, 
                            'height' : '100vh',
                            'padding' : 10, 
                            'backgroundColor' : '#00263e', 
                            'color' : 'white'}),
                
                # data panel
                html.Div([
                    html.H1(children='Imported data'),
                    
                    html.Br(),
                    dcc.Dropdown(['Raw', 'Summary'], 
                                 value = 'Raw', style = {'width' : '40%'},
                                 id='data-display-choice'),
                    
                    dcc.Store(id='data-store'),
                    
                    html.Div(children='No values entered',
                             id='data-panel',
                             style={'width':'80vw',
                                    'heigh':'50vh'} #1800}
                        )
                    
                ], style = {'flex' : 1,
                            'height' : '100vh',
                            'padding' : 10, 
                            'backgroundColor' : 'white'})
                
              ], style = {'display' : 'flex', 'flex-direction' : 'row'})
            
            ], style = tab_style, selected_style = tab_selected_style),
        
                            
        # Graphs tab ---------------------------------------------------------
        dcc.Tab(label='Graphs', children = [
            # main body
            html.Div(children=[
                # left panel
                html.Div([
                    
                    html.H1(children='Graph Options'),
                    
                    html.Br(),
                    html.Label('Choose Variable'),
                    dcc.Dropdown([],
                                 id='variable-choice-graph',
                                 style={'color' : 'black'})
                    
                    ], style = {'flex' : .2,
                                'height' : '100vh',
                                'padding' : 10, 
                                'backgroundColor' : '#00263e', 
                                'color' : 'white'}),
                # graph panel
                html.Div([
                    
                    dcc.Graph(id='line-graph',
                              style={
                                "width": "80%",
                                "height": "80%",
                            })
                    
                    ], style = {'flex' : 1, 
                                'height' : '100vh',
                                'padding' : 10, 
                                'backgroundColor' : 'white'
                                })
                    
                ], style = {'display' : 'flex', 
                            'flex-direction' : 'row'})
            ], style = tab_style, selected_style = tab_selected_style),
        
        # Stats tab -----------------------------------------------------------
        dcc.Tab(label='Statistics', children = [
            # main body
            html.Div(children=[
                # left panel
                html.Div([
                    
                    html.H1(children='Graph Options'),
                    
                    html.Br(),
                    html.Label('Choose Variable'),
                    dcc.Dropdown([],
                                 id='variable-choice-stats',
                                 style={'color' : 'black'})
                    
                    ], style = {'flex' : .2,
                                'height' : '100vh',
                                'padding' : 10, 
                                'backgroundColor' : '#00263e', 
                                'color' : 'white'}),
                # stats panel
                html.Div([
                    html.H2(children='Model Output'),
                    html.Div(children='',
                             id='stats-aov-output',
                             style={'width':'40vw',
                                    'heigh':'10vh'}
                        ),
                    
                    html.H2(children='Pariwise Comparisons'),
                    html.Div(children='',
                             id='stats-pwc-output',
                             style={'width':'70vw',
                                    'heigh':'90vh'}
                        )
                    
                    ], style = {'flex' : 1, 
                                'height' : '100vh',
                                'padding' : 10, 
                                'backgroundColor' : 'white'})
                                
                ], style = {'display' : 'flex', 
                            'flex-direction' : 'row'})        
            
            ], style = tab_style, selected_style = tab_selected_style),        
        ])
        
    ], style = {'backgroundColor' : '#00263e',
                'height' : '100vh'})

## ---------------------------- Callbacks -----------------------------------##

# callback generates json serialised data frame and saves for later access
@app.callback(
    Output('data-store', 'data'),
    Input('Input-files', 'value'),
    Input('Choose-descriptor', 'value'),
    Input('Grp1', 'value'),
    Input('Grp2', 'value'),
    Input('Grp3', 'value'),
    Input('Grp4', 'value'),
    Input('Grp5', 'value'),
    Input('Grp6', 'value'),
    Input('Group-names', 'value'),
    Input('Timepoints', 'value'),
    Input('Compute-button', 'n_clicks'),
    )
def update_output(files,
                  descriptor,
                  group1, group2, group3, group4, group5, group6,
                  group_names,
                  timepoints,
                  button):
    
    # placeholder dataframe
    data = pd.DataFrame({'Placeholder':['Enter definitions and press compute']})
    json_data = data.to_json(orient='split')
    
    # generate group dictionary from user input
    group_definitions = dict(zip(group_names.split(","), [group1, group2, group3, group4, group5, group6]))
    
    timepoints = timepoints.split(",")
    timepoints = [int(time) for time in timepoints]
    
    if descriptor == 'Mean':
        des = 2
    elif descriptor == 'Min':
        des = 3
    elif descriptor == 'Max':
        des = 1
    
    # import dir as sting and replace the "" introduced by windows when copying paths
    input_dir = r'{}'.format(files)
    input_dir = input_dir[1:-1]
    
    # generate file list  
    file_list = os.listdir(input_dir)
    file_list = [f'{input_dir}\\{f}' for f in file_list if f.endswith('xlsx')]
    file_list = sorted(file_list)

   
    # when compute button is pressed
    if 'Compute-button' == ctx.triggered_id:
        
        # generate ratio of time points to number of files
        time_ratio = int(24*len(file_list)/len(timepoints))
        
        # generate assignments dictionary
        assignments = {'file': [file for file in file_list for i in enumerate(wells)],
                       'well': [well for file in file_list for well in wells],
                       'timepoint': [time for time in timepoints for well in range(time_ratio)] 
        }
        
        
        # generate dictionary of group names associated with index of associated wells
        group_index = {}
        
        for key in group_definitions:
            group_index[key] = [index for index, value in enumerate(assignments['well']) for well in group_definitions[key]\
                                if value == well]
           
        # apply group names to group list in assignments dictionary
        groups = ['NA' for line in range(len(assignments['file']))]
        
        for key in group_definitions:
            for index in group_index[key]:
                groups[index] = key
                
        assignments['group'] = groups     
        
        # load first excel file only to extract variable names
        f = pd.read_excel(file_list[0], sheet_name='aggregate-metrics')
        
        # find unique variable names within file - ignore empty lines
        variable_list = [variable for variable in pd.unique(f['Unnamed: 0']) if str(variable) != 'nan']
        
        # generate line index for each variable
        variable_index = {}
        
        for key in variable_list:
            variable_index[key] = [index+des for index, value in enumerate(f['Unnamed: 0']) if value == key] # to adjust relative position of mean, min or mean add 'des' to index here
            
        # read in data from each file into dictionary, key is the variable name
        data_dict = {variable:[] for variable in variable_list}
        
        # open each excel sequentially from file lies and extract from aggregate metric sheets the rows defined in the variable index dictionary
        for file in file_list:
            f = pd.read_excel(file, sheet_name = 'aggregate-metrics')
            for variable in variable_list:
                data_dict[variable].extend(f.loc[variable_index[variable][0], wells].tolist())    
        
        # combine data and assignments dictionaries
        data = dict(assignments, **data_dict)
        
        # convert to dataframe
        data = pd.DataFrame.from_dict(data)
        
        # clean data of any rows not associated with a user defined group
        data = data[data.group != 'NA']
        

        # convert to json format
        json_data = data.to_json(orient='split')
    
    return json_data

# callback reads json data and creates dataframes for display
@app.callback(
    Output('data-panel', 'children'),
    Input('data-store', 'data'),
    Input('data-display-choice', 'value')
    )
def summary_output(data,
                   data_choice):
    
    # read data from json store
    df = pd.read_json(data, orient='split')

    # create data table to display raw data
    tbl = dash_table.DataTable(df.to_dict('records'),
                               style_table={'overflowX' : 'scroll'},
                               style_cell={'textAlign':'left'})
    
    # if user chooses summary calculate summary values and display this table
    if data_choice == 'Summary':
        # flatten column names as dash cannot display multi index tables
        summary_df = df.groupby(['group', 'timepoint']).describe().loc[:,(slice(None),['count','mean', 'std'])].reset_index()
        summary_df.columns = [" - ".join(i) for i in summary_df.columns] 
        
        tbl = dash_table.DataTable(summary_df.to_dict('records'),
                                   style_table={'overflowX' : 'scroll'},
                                   style_cell={'textAlign':'left'})
        

    return tbl
     
# pass variables imported from spreadheets to dropdown menu in graph tab
@app.callback(
    Output('variable-choice-graph', 'options'),
    Output('variable-choice-graph', 'value'),
    Output('variable-choice-stats', 'options'),
    Output('variable-choice-stats', 'value'),
    Input('data-store', 'data')
    )
def dropdown_update(data):
    df = pd.read_json(data, orient='split')
    variable_list = [column for column in df.columns if column not in ['file', 'well', 'timepoint', 'group']]
    
    return variable_list, variable_list[0], variable_list, variable_list[0]

    
# plot summary data - this needs to be changed to only run after the data has been imported, error thrown due to lack of 'group' in placeholder dataframe
@app.callback(
    Output('line-graph', 'figure'),
    Input('data-store', 'data'),
    Input('variable-choice-graph', 'value')
    ) # straightforward to add labels and axis limit options for users with extra inputs
def plotting(data,
             variable):
    
    df = pd.read_json(data, orient='split')
    
    summary_df = df.groupby(['group', 'timepoint']).describe().loc[:,(slice(None),['count','mean', 'std'])].reset_index()
       
    # generate plotting dataframe - this could be more elegant
    plot_data = pd.DataFrame(summary_df[variable])
    plot_data['group'] = summary_df['group']
    plot_data['timepoint'] = summary_df['timepoint']
    
    # generate plotly figure object
    fig = px.line(plot_data,
                  x='timepoint', 
                  y='mean', 
                  color='group',
                  error_y='std',
                  markers= True,
                  template='simple_white',
                  labels={'mean' : variable,
                          'timepoint' : 'Days',
                          'group' : 'Group:'})
    
    fig.update_layout(title= {'text' : variable,
                              'x' : 0.5,
                              'xanchor' : 'center'},
                      font_family = 'Arial Black',
                      legend = {'orientation' : 'h',
                                'x' : 0.5,
                                'xanchor' : 'center'},
                      font = {'size' : 16})
    
    fig.update_yaxes(linewidth = 2)
    fig.update_xaxes(linewidth = 2)
               
    # return figure
    return fig

# calculate statistics     
@app.callback(
    Output('stats-aov-output', 'children'),
    Output('stats-pwc-output', 'children'),
    Input('data-store', 'data'),
    Input('variable-choice-stats', 'value')
    )
def statistics_processing(data,
                          variable):
    df_raw = pd.read_json(data, orient='split')
    
    # import data, groups and wells rename variable to remove characters not supported by stats packages
    df = df_raw[['well','group','timepoint',variable]].rename(columns = {variable:'variable'})
    df['group*timepoint'] = df['group'].astype('str') +"*"+ df["timepoint"].astype('str')
    
    # empty dictionaries for statistical tests
    shapiro_p_values = {}
    levene_arrays = {}
    
    if len(df['group'].unique())>1:
        # run shapiro tests on each group and collect arrays for levenes
        for grp in df_raw['group'].unique():
            df_filter = df[df.group == grp]
            
            shapiro_p_values[f'Group - {grp}'] = stats.shapiro(df_filter['variable']).pvalue
            
            if 'Groups' in levene_arrays.keys():
                levene_arrays['Groups'] += [df_filter['variable'].tolist()]
            else:
                levene_arrays['Groups'] = [df_filter['variable'].tolist()]
                
        # run shapiro tests on each timepoint and collect arrays for levenes    
        for time in df_raw['timepoint'].unique():
            df_filter = df[df.timepoint == time]
            
            shapiro_p_values[f'Timepoint - {time}'] = stats.shapiro(df_filter['variable']).pvalue
        
            if 'Timepoints' in levene_arrays.keys():
                levene_arrays['Timepoints'] += [df_filter['variable'].tolist()]
            else:
                levene_arrays['Timepoints'] = [df_filter['variable'].tolist()]
         
        # run shapiro tests on each group:timepoint interaction and collect arrays for levenes
        for grp in df_raw['group'].unique():
            for time in df_raw['timepoint'].unique():
                df_filter = df[df.timepoint == time]
                
                shapiro_p_values[f'Group {grp} x Timepoint - {time}'] = stats.shapiro(df_filter['variable']).pvalue
                
                if 'Group-Timepoints' in levene_arrays.keys():
                    levene_arrays['Group-Timepoints'] += [df_filter['variable'].tolist()]
                else:
                    levene_arrays['Group-Timepoints'] = [df_filter['variable'].tolist()]
        
        # make shapiro outputs into data frame
        shapiro_df = pd.DataFrame.from_dict(shapiro_p_values, 
                                            orient = 'index',
                                            columns = ['Shapiro p_value'])
        
        # collect levenes arrays and peform tests
        stat, groups_p = stats.levene(*levene_arrays['Groups'])
        stat, timpoints_p = stats.levene(*levene_arrays['Timepoints'])
        stat, groupsbytimepoints_p = stats.levene(*levene_arrays['Group-Timepoints'])
        
        # format levene p values into dictionary then convert to dataframe for display
        levenes_tests = {'Groups':groups_p,
                         'Timepoints':timpoints_p,
                         'Groups by Timepoints':groupsbytimepoints_p}
        
        levenes_df = pd.DataFrame.from_dict(levenes_tests, 
                                            orient = 'index',
                                            columns = ['Levene p_value'])
        
        # test assumptions with shapiro and levenes tests, returns false if assumptions violoated
        if shapiro_df['Shapiro p_value'].min() <= 0.05 or levenes_df['Levene p_value'].min() <= 0.05:
            para_bool = False
        else:
            para_bool = True
         
        # run parametric or non-parametric model analysis of variance - anova or kruscal wallis
        if para_bool == True:
            aov = pg.anova(dv='variable', 
                           between=['group','timepoint'], 
                           data=df,
                           detailed=True)
        else:
            krs_grp=pg.kruskal(dv='variable', 
                            between='group', 
                            data=df)
            
            krs_tmp=pg.kruskal(dv='variable', 
                                between='timepoint', 
                                data=df)
            
            krs_gbt=pg.kruskal(dv='variable', 
                                between='group*timepoint', 
                                data=df)
            
            aov = pd.concat([krs_grp, krs_tmp, krs_gbt]).reset_index().drop(['index'], axis=1)
            
        # create significance mark column and populate with astrix if p value less than .05
        aov['Significance'] = ''
        
        for index, row in aov.iterrows():
            if aov['p-unc'].iloc[index] <= 0.05:
                aov.loc[index,'Significance'] = '*'
        
        # make pairwise comprisons of all possible pairs, not this requires two tests to be run
        pairwise_first = pg.pairwise_tests(dv='variable', 
                                           between=['group','timepoint'],
                                           data=df,
                                           padjust='fdr_bh',
                                           parametric=para_bool)
        pairwise_second = pg.pairwise_tests(dv='variable', 
                                           between=['timepoint','group'],
                                           data=df,
                                           padjust='fdr_bh',
                                           parametric=para_bool)
        
        # merge frames and remove duplicate tests
        if para_bool == False:
            pairwise_output = pd.concat([pairwise_first, pairwise_second])\
                              .drop_duplicates(subset=['Contrast','A','B','p-unc']).reset_index()\
                              .drop(['index','alternative','hedges','U-val'], axis = 1)
        else:
            pairwise_output = pd.concat([pairwise_first, pairwise_second])\
                              .drop_duplicates(subset=['Contrast','A','B','p-unc']).reset_index()\
                              .drop(['index','alternative','BF10','dof','hedges'], axis = 1)
           
        
        # reorder columns to bring timepoint to sensible position
        pairwise_output=pairwise_output[pairwise_output.columns[:-1].insert(2, pairwise_output.columns[-1])]
        
        # create significance mark column and populate with astrix if p value less than .05
        pairwise_output['Significance'] = ''
        
        for index, row in pairwise_output.iterrows():
            if pairwise_output['p-corr'].iloc[index] <= 0.05 and pairwise_output['p-corr'].iloc[index] != 'NaN':
                pairwise_output.loc[index,'Significance'] = '*'
            elif pairwise_output['p-unc'].iloc[index] <= 0.05:
                pairwise_output.loc[index,'Significance'] = '*'
    
    # if no group contrasts need to be made only make timepoint contrasts
    else:
        # run shapiro tests on each timepoint and collect arrays for levenes    
        for time in df_raw['timepoint'].unique():
            df_filter = df[df.timepoint == time]
            
            shapiro_p_values[f'Timepoint - {time}'] = stats.shapiro(df_filter['variable']).pvalue
        
            if 'Timepoints' in levene_arrays.keys():
                levene_arrays['Timepoints'] += [df_filter['variable'].tolist()]
            else:
                levene_arrays['Timepoints'] = [df_filter['variable'].tolist()]
     
        # make shapiro outputs into data frame
        shapiro_df = pd.DataFrame.from_dict(shapiro_p_values, 
                                            orient = 'index',
                                            columns = ['Shapiro p_value'])
        
        # collect levenes arrays and peform tests
        stat, timpoints_p = stats.levene(*levene_arrays['Timepoints'])
        
        # format levene p values into dictionary then convert to dataframe for display
        levenes_tests = {'Timepoints':timpoints_p}
                                 
        levenes_df = pd.DataFrame.from_dict(levenes_tests, 
                                            orient = 'index',
                                            columns = ['Levene p_value'])
        
        # test assumptions with shapiro and levenes tests, returns false if assumptions violoated
        if shapiro_df['Shapiro p_value'].min() <= 0.05 or levenes_df['Levene p_value'].min() <= 0.05:
            para_bool = False
        else:
            para_bool = True
        
        # test assumptions with shapiro and levenes tests, returns false if assumptions violoated
        if shapiro_df['Shapiro p_value'].min() <= 0.05 or levenes_df['Levene p_value'].min() <= 0.05:
            para_bool = False
         
        # run parametric or non-parametric model analysis of variance - anova or kruscal wallis
        if para_bool == True:
            aov = pg.anova(dv='variable', 
                           between=['timepoint'], 
                           data=df,
                           detailed=True)
        else:
            krs_tmp=pg.kruskal(dv='variable', 
                                between='timepoint', 
                                data=df)
            
            aov = krs_tmp.reset_index().drop(['index'], axis=1)
            
        # create significance mark column and populate with astrix if p value less than .05
        aov['Significance'] = ''
        
        for index, row in aov.iterrows():
            if aov['p-unc'].iloc[index] <= 0.05:
                aov.loc[index, 'Significance'] = '*'
        
        # make pairwise comprisons of all possible pairs, not this requires two tests to be run
        pairwise_first = pg.pairwise_tests(dv='variable', 
                                           between=['timepoint'],
                                           data=df,
                                           padjust='fdr_bh',
                                           parametric=para_bool)
                
        # merge frames and remove duplicate tests
        if para_bool == False:
            pairwise_output = pairwise_first\
                              .drop_duplicates(subset=['Contrast','A','B','p-unc']).reset_index()\
                              .drop(['index','alternative','hedges','U-val'], axis = 1)
        else:
            pairwise_output = pairwise_first\
                              .drop_duplicates(subset=['Contrast','A','B','p-unc']).reset_index()\
                              .drop(['index','alternative','BF10','dof','hedges'], axis = 1)
        
        # reorder columns to bring timepoint to sensible position
        pairwise_output=pairwise_output[pairwise_output.columns[:-1].insert(1, pairwise_output.columns[-1])]
        
        # create significance mark column and populate with astrix if p value less than .05
        pairwise_output['Significance'] = ''
        
        for index, row in pairwise_output.iterrows():
            if pairwise_output['p-corr'].iloc[index] <= 0.05 and pairwise_output['p-corr'].iloc[index] != 'NaN':
                pairwise_output.loc[index, 'Significance'] = '*'
            elif pairwise_output['p-unc'].iloc[index] <= 0.05:
                pairwise_output.loc[index, 'Significance'] = '*'
    
    aov = dash_table.DataTable(aov.to_dict('records'),
                               style_table={'overflowX' : 'scroll'},
                               style_cell={'textAlign':'left'})
    
    pairwise_output = dash_table.DataTable(pairwise_output.to_dict('records'),
                                           style_table={'overflowX' : 'scroll'},
                                           style_cell={'textAlign':'left'})
                
    # return outputs
    return aov, pairwise_output

# download callbacks
@app.callback(
    Output('raw-data-download', 'data'),
    Input('raw-data-download-button', 'n_clicks'),
    Input('data-store', 'data'),
    )
def raw_download(n_clicks, data):
    if 'raw-data-download-button' == ctx.triggered_id:
        df = pd.read_json(data, orient='split')
    
        return dcc.send_data_frame(df.to_excel, "Raw_data_download.xlsx", sheet_name="Raw Data")
    
@app.callback(
    Output('summary-data-download', 'data'),
    Input('summary-data-download-button', 'n_clicks'),
    Input('data-store', 'data'),
    )
def summary_download(n_clicks, data):
    if 'summary-data-download-button' == ctx.triggered_id:
        df = pd.read_json(data, orient='split')
        summary_df = df.groupby(['group', 'timepoint']).describe().loc[:,(slice(None),['count','mean', 'std'])].reset_index() 
    
        return dcc.send_data_frame(summary_df.to_excel, "Summary_data_download.xlsx", sheet_name="Summary Data")
    
                   
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)  