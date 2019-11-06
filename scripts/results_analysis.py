import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np
from math import pi
import output as oup


def format_dataframe(dat_file,column_names,index):
    """ This function formats a dakota output dat file into an easily readable format 
    INPUT 
    dat_file: path to dat file (str)
    column_names = list of names corresponding to what the user wants each column to be named
                   (list of str)
    index = list of input variable names to be index (list of str)
    OUTPUT 
    df: formatted pandas dataframe 
    """
    df = pd.read_csv(dat_file,sep='\s+',names=column_names)
    df = df.iloc[1:]
    df = df.drop(columns='id')
    df = df.set_index(index)
    return df 

def initialize_df(scenario_index,scenarios_nums):
    """This function creates a pandas dataframe with scenario_index 
    as index title and scenarios_nums as index values.
    This is used to initialize a dataframe to add subsequent columns to.
    INPUT 
    scenario_index: title of index
    scenario_nums: list of scenario numbers
    OUTPUT 
    df: initialized pandas dataframe 
    """
    df = pd.DataFrame(index=scenarios_nums)
    df.index.name = scenario_index
    return df 

def eval_criteria_everything(starter_string,scenario_nums,dymond6_output):
    scenarios = []
    for x in range(len(scenario_nums)): 
        scenarios.append(starter_string+scenario_nums[x])
    df = initialize_df(scenario_index=starter_string,
                       scenarios_nums=scenario_nums)
    
    df['Final HLW in storage'] = 0
    df['Final HLW in storage (Transition)'] = 0
    df['Final Depleted U'] = 0 
    df['Final Depleted U (Transition)'] = 0 
    df['Sum uranium ore'] = 0
    df['Sum uranium ore (Transition)'] = 0
    df['Sum total idle capacity'] = 0
    df['Last date idle capacity'] = 0
    df['Duration of transition'] = 0

    for x in range(len(scenario_nums)): 
        df.loc[scenario_nums[x],'Final HLW in storage'], val = oup.grep_database(output_database=dymond6_output,
                                                                                 scenario_name=scenarios[x],
                                                                                 data_type='Stocks',
                                                                                 output_variable='HLW in storage',
                                                                                 indicator='final',
                                                                                 reactor_all=True)
        df.loc[scenario_nums[x],'Final HLW in storage (Transition)'], val = oup.grep_database(output_database=dymond6_output,
                                                                                              scenario_name=scenarios[x],
                                                                                              data_type='Stocks',
                                                                                              output_variable='HLW in storage',
                                                                                              indicator='final',
                                                                                              reactor_all=True,
                                                                                              transition=True)
        df.loc[scenario_nums[x],'Final Depleted U'], val = oup.grep_database(output_database=dymond6_output,
                                                                             scenario_name=scenarios[x],
                                                                             data_type='Stocks',
                                                                             output_variable='Depleted U',
                                                                             indicator='final',
                                                                             reactor_all=True)
        df.loc[scenario_nums[x],'Final Depleted U (Transition)'], val = oup.grep_database(output_database=dymond6_output,
                                                                                          scenario_name=scenarios[x],
                                                                                          data_type='Stocks',
                                                                                          output_variable='Depleted U',
                                                                                          indicator='final',
                                                                                          reactor_all=True,
                                                                                          transition =True)
        df.loc[scenario_nums[x],'Sum uranium ore'], val =  oup.grep_database(output_database=dymond6_output,
                                                                              scenario_name=scenarios[x],
                                                                              data_type='Flows',
                                                                              output_variable='Mined ore',
                                                                              indicator='sum',
                                                                              reactor_all=True)
        df.loc[scenario_nums[x],'Sum uranium ore (Transition)'], val =  oup.grep_database(output_database=dymond6_output,
                                                                                          scenario_name=scenarios[x],
                                                                                          data_type='Flows',
                                                                                          output_variable='Mined ore',
                                                                                          indicator='sum',
                                                                                          reactor_all=True,
                                                                                          transition=True)
        df.loc[scenario_nums[x],'Sum total idle capacity'], val = oup.grep_database(output_database=dymond6_output,
                                                                                  scenario_name=scenarios[x],
                                                                                  data_type='Reactors',
                                                                                  output_variable='Idle capacity',
                                                                                  indicator='sum',
                                                                                  reactor_all=False,
                                                                                  reactor_list=[1,2,3])
        start, df.loc[scenario_nums[x],'Last date idle capacity'] = oup.transition_start_end(output_database=dymond6_output,
                                                                                             scenario_name=scenarios[x])
        df.loc[scenario_nums[x],'Duration of transition'] = df.loc[scenario_nums[x],'Last date idle capacity'] - start
    return df 

def eval_criteria_proliferation(starter_string,scenario_nums,commod,dymond6_output):
    scenarios = []
    for x in range(len(scenario_nums)): 
        scenarios.append(starter_string+scenario_nums[x])
    df_pu4 = initialize_df(scenario_index=starter_string,
                   scenarios_nums=scenario_nums)
    df_pu4['Max Pu '+commod] = 0
    df_pu4['Max Pu '+commod+' year'] = 0
    df_pu4['End Slope Pu '+commod] = 0
    df_pu4['Max Fissile Pu '+commod] = 0
    df_pu4['Max Fissile Pu '+commod+' year'] = 0
    df_pu4['End Slope Fissile Pu '+commod] = 0
    df_pu4['Max Pu '+commod+' year quality'] = 0

    for x in range(len(scenario_nums)):
        df_pu4.loc[scenario_nums[x],'Max Pu '+commod],df_pu4.loc[scenario_nums[x],'Max Pu '+commod+' year'] = oup.grep_isotopics(output_database=dymond6_output,
                                                                                                                                           scenario_name=scenarios[x],
                                                                                                                                           isotopes=['Pu'],
                                                                                                                                           output_variable=commod,
                                                                                                                                           indicator='max')   
        df_pu4.loc[scenario_nums[x],'End Slope Pu '+commod], val = oup.grep_isotopics(output_database=dymond6_output,
                                                                                           scenario_name=scenarios[x],
                                                                                           isotopes=['Pu'],
                                                                                           output_variable=commod,
                                                                                           indicator='slope')
        df_pu4.loc[scenario_nums[x],'Max Fissile Pu '+commod],df_pu4.loc[scenario_nums[x],'Max Fissile Pu '+commod+' year'] = oup.grep_isotopics(output_database=dymond6_output,
                                                                                                                                           scenario_name=scenarios[x],
                                                                                                                                           isotopes=['Pu-239','Pu-241'],
                                                                                                                                           output_variable=commod,
                                                                                                                                           indicator='max')
        df_pu4.loc[scenario_nums[x],'End Slope Fissile Pu '+commod], val = oup.grep_isotopics(output_database=dymond6_output,
                                                                                           scenario_name=scenarios[x],
                                                                                           isotopes=['Pu-239','Pu-241'],
                                                                                           output_variable=commod,
                                                                                           indicator='slope')
        df_pu4.loc[scenario_nums[x],'Max Pu '+commod+' year quality'] = df_pu4.loc[scenario_nums[x],'Max Fissile Pu '+commod]/df_pu4.loc[scenario_nums[x],'Max Pu '+commod]
    return df_pu4

def eval_criteria_plutonium(starter_string,scenario_nums,dymond6_output): 
    scenarios = []
    for x in range(len(scenario_nums)): 
        scenarios.append(starter_string+scenario_nums[x])
    df = initialize_df(scenario_index=starter_string,
                       scenarios_nums=scenario_nums)
    commod_list = ['Primary feed','Spent fuel waiting for RP','HLW in storage','Spent fuel in storage',
                   'Fuel in reactors','Spent fuel cooling','Spent fuel ready for disposal','HLW ready for disposal']
    for x in range(len(commod_list)): 
        df['Max Pu '+commod_list[x]] = 0
    for y in range(len(commod_list)):
        for x in range(len(scenario_nums)):
            df.loc[scenario_nums[x],'Max Pu '+commod_list[y]], val = oup.grep_isotopics(output_database=dymond6_output,
                                                                                       scenario_name=scenarios[x],
                                                                                       isotopes=['Pu'],
                                                                                       output_variable=commod_list[y],
                                                                                       indicator='max')
    return df

# sensitivity 
def sensitivity(base_case,init_df):
    """ This function takes a dataframe 
    """
    SA_df = init_df.copy()
    M = init_df.index.size
    categories=list(init_df)
    N = len(categories)
    row = 0
    for x in range(M): 
        if init_df.index[x] == base_case: 
            basecase_index = row
        row += 1
    for x in range(M): 
        if init_df.index[x] == base_case: 
            for y in range(N): 
                SA_df.iloc[x,y] = 0
        else: 
            for y in range(N): 
                if float(init_df.iloc[basecase_index,y]) == 0: 
                    SA_df.iloc[x,y] = np.nan
                else:
                    SA_df.iloc[x,y] = (init_df.iloc[x,y]-init_df.iloc[basecase_index,y])/init_df.iloc[basecase_index,y]*100  
    return SA_df


def threed_plot(df,commod):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # Data for a three-dimensional line
    x = [int(i) for i in list(df.index.get_level_values(0).values)]
    y = [int(i) for i in list(df.index.get_level_values(1).values)]
    z = [float(i) for i in list(df[commod].values)]
    for xi, yi, zi in zip(x, y, z):        
        line=art3d.Line3D(*zip((xi, yi, min(z)), (xi, yi, zi)), marker='o', markevery=(1, 1))
        ax.add_line(line) 
    ax.set_xlim3d(x[0], x[-1])
    ax.set_ylim3d(y[0], y[-1])
    ax.set_zlim3d(min(z), max(z))  
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.zaxis.set_major_locator(MaxNLocator(5))
    ax.set_title('3D plot of '+commod)
    ax.set_xlabel(df.index.names[0]+' [%]')
    ax.set_ylabel(df.index.names[1]+ ' [yr]')
    ax.set_zlabel(commod +' [kg]')
    ax.dist = 11
    fig.savefig(commod, bbox_inches='tight')
    return