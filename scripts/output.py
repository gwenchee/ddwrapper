"""
This script contains functions to get various output variable values
from Dymond6 output database excel workbook.

***
- Workbook must NOT be open when running these functions.
"""

# Dependencies
import pandas as pd
import numpy as np

### FUNCTIONS ### (alphabetical order of function name)
# 4 types of output indicators (cumulated, maximum,minimum, final)
# Function to easily query various informations from the table


def fun_indicator(dataframe, indicator, final_year, slope_points=10):
    """ This function returns the final, maximum, minimum, cumulative or end slope
    value from the pandas dataframe it is given.
    INPUT
    dataframe: pandas dataframe
    indicator: the type of result to return -> final, max, min, sum or slope (str)
    slope_points: How many points to calculate end slope with
    OUTPUT
    val: the final, max, min or cumulative value based on the user chosen indicator (double)
    when: the year when the val occurred
          NOT relevant for the sum & slope indicator, it will just return final year
    """
    if indicator == 'final':
        when = final_year
        if dataframe['Value'].tail(1).index[0] == final_year:
            val = dataframe['Value'].tail(1).values[0]
        elif dataframe.empty:
            val = 0
        else:
            val = 0
    elif indicator == 'max': 
        val = dataframe['Value'].max()
        when = dataframe['Value'].idxmax()
    elif indicator == 'min': 
        val = dataframe['Value'].min()
        when = dataframe['Value'].idxmin()
    elif indicator == 'sum': 
        val = dataframe['Value'].sum()
        when = final_year
    elif indicator == 'slope': 
        dataframe2 = dataframe.copy()
        for x in range(len(dataframe.index)):
            if dataframe.index[x] <= (final_year-slope_points):
                dataframe2 = dataframe2.drop(dataframe.index[x])
        val = dataframe2.apply(lambda x: np.polyfit(dataframe2.index, x, 1)[0])[0]
        when = final_year
    else:
        raise Exception('The only available indicators are final, max, min, sum, or slope')
    return val, when


def get_dataframe(output_database):
    """This function takes a excel file and puts it into a pandas dataframe
    INPUT
    output_database: excel workbook path (str)
    OUTPUT
    pandas_excel: pandas dataframe containing excel workbook
    """
    pandas_excel = pd.ExcelFile(output_database)
    return pandas_excel


def get_transition_dataframe(whole_df, start, end):
    N = len(whole_df.index)
    whole_df2 = whole_df.copy()
    for x in range(N):
        if whole_df.index[x] < start:
            whole_df2 = whole_df2.drop(whole_df.index[x])
        elif whole_df.index[x] > end:
            whole_df2 = whole_df2.drop(whole_df.index[x])
    transition_df = whole_df2.copy()
    return transition_df


def grep_database(output_database,
                  scenario_name,
                  data_type,
                  output_variable,
                  indicator,
                  reactor_all=False,
                  reactor_list=[1,2,3,4,5], 
                  transition=False):
    """ This function generalizes the search for a specific output variable
    in a defined Dymomd6 output database.
    INPUT
    output_database: excel workbook dataframe (output from get_dataframe)
                     OR excel workbook path (str)
    scenario_name: scenario name (str)
    data_type: sheet in the output_database that the output_variable resides
               3 Options: Reactors, Stocks, or Flows. (str)
    output_variable: Data type of interest in output_database (str)
    indicator: the type of result to return (str)
               3 Options: final, max, min or sum.
    reactor_all: boolean to state whether output_variable is an " All types"
                 Reactor Type in the output database file (boolean)
    reactor_list: if reactor_all is False list of reactor numbers of interest
                  (list of int)
    transition: boolean to choose between evaluation of the whole simulation (False)
                or just the transition (True).
    OUTPUT
    val: the final, max or cumulative value based on the user chosen indicator (double)
    """
    datatypes = ['Reactors', 'Stocks', 'Flows']
    if data_type not in datatypes:
        raise Exception('Only 3 datatypes are accepted: Reactors, Stocks and Flows. Check that you capitalized the first letter')
    sheet = data_type + ' data'
    df = pd.read_excel(output_database, sheet_name=sheet)
    df = df[df['Scenario name'] == scenario_name]
    df = df[df['Data type'] == output_variable]
    start_year = df['Date'].head(1).values[0]
    final_year = df['Date'].tail(1).values[0]
    if reactor_all:
        df = df[df['Reactor type'] == 'All types']
    else: 
        if len(reactor_list) > 5: 
            raise Exception('There is a maximum of 5 reactors')
        else: 
            reactorlist = []
            for x in range(len(reactor_list)): 
                reactorlist.append('Reactor type '+ str(reactor_list[x]))
            df = df[df['Reactor type'].isin(reactorlist)]
    df = df.groupby('Date').sum()
    if df.empty:
        raise Exception('Dataframe is empty. Possible Causes: your scenario_name/data_type/output_variable is not defined correctly, what you are looking for doesnt exist in the database')
    if transition:
        try:
            start, end = transition_start_end(output_database, scenario_name)
        except:
            start = start_year
            end = final_year
        df = get_transition_dataframe(df, start, end)
        val, when_val = fun_indicator(df, indicator, end)
    else:
        val, when_val = fun_indicator(df, indicator, final_year)
    return val, when_val


def grep_isotopics(output_database,
                   scenario_name,
                   isotopes,
                   output_variable,
                   indicator, 
                   transition=False):
    """ This function generalizes the search of isotopics for a specific output variable 
    in a defined Dymomd6 output database. And so you can get the absolute mass of selected 
    isotopes (ie. Pu) in a type of stock (ie. HLW). 
    INPUT 
    output_database: excel workbook dataframe (output from get_dataframe)
                     OR excel workbook path (str)
    scenario_name: scenario name (str)
    isotopes: list of isotopes (Can input element or isotope name) 
             Element name, must be written in this format eg: U, Am (str)
             Isotope name, must be written in this format eg: U-235, Am-242m (str)
             EG: ['Pu','Am-241','U-235']
    output_variable: Data type of interest in output_database (str)
    indicator: the type of result to return (str)
               3 Options: final, max, min or sum. 
    transition: boolean to choose between evaluation of the whole simulation (False)
                or just the transition (True).
    OUTPUT 
    val: the final, max or cumulative value based on the user chosen indicator (double)
    """
    df = pd.read_excel(output_database,sheet_name = 'Isotopic compositions')
    dfs = pd.read_excel(output_database,sheet_name = 'Stocks data')
    df = df[df['Scenario name']==scenario_name] 
    dfs = dfs[dfs['Scenario name']==scenario_name] 
    df = df[df['Stock type']==output_variable]
    dfs = dfs[dfs['Data type']==output_variable]
    start_year = df['Date'].head(1).values[0]
    final_year = df['Date'].tail(1).values[0]
    if df.empty: 
        raise Exception('Dataframe is empty. Possible Causes: your scenario_name/data_type/output_variable is not defined correctly, what you are looking for doesnt exist in the database')
    pattern = '|'.join(isotopes)
    df = df[df['Isotope'].str.contains(pattern)]
    df = df[df['Reactor type']=='All types']
    dfs = dfs[dfs['Reactor type']=='All types']
    df = df.groupby('Date').sum()
    dfs = dfs.groupby('Date').sum()
    df_final = df*dfs
    if transition:
        try:
            start, end = transition_start_end(output_database, scenario_name)
        except:
            start = start_year
            end = final_year
        df_final = get_transition_dataframe(df_final, start, end)
        val, when_val = fun_indicator(df_final, indicator, end)
    else:
        val, when_val = fun_indicator(df_final, indicator, final_year)
    return val, when_val


def pu_quality():
    return


def transition_start_end(output_database, scenario_name):
    """ This function returns the start and end year of transition of a scenario
    selected by user.
    The start year of transition is defined as the first year where a
    reactor that is not reactor 1 begins construction.
    The end year of transition is defined as the final year where there is 
    idle capacity.
    INPUT
    output_database: excel workbook dataframe (output from get_dataframe)
                     OR excel workbook path (str)
    scenario_name: scenario name (str)
    OUTPUT
    transition_start_date: the start date of transition in scenario (int)
    transition_end_date: the end date of transition in scenario (int)
    """
    r_df = pd.read_excel(output_database, 'Reactors data')
    r_df = r_df[r_df['Scenario name'] == scenario_name]
    start_df = r_df[r_df['Data type'] == 'Under construction'] 
    end_df = r_df[r_df['Data type'] == 'Idle capacity']
    reactorlist = ['Reactor type 2', 'Reactor type 3', 'Reactor type 4', 'Reactor type 5']
    start_df = start_df[start_df['Reactor type'].isin(reactorlist)]
    transition_start_date = start_df['Date'].head(1).values[0]
    transition_end_date = end_df['Date'].tail(1).values[0]
    return transition_start_date, transition_end_date
