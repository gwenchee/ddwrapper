"""
This script contains functions to edit various variables in a Dymond6
input excel notebook.

***
- An error will be thrown if you don't enable editing on the excel workbook
- Workbook must NOT be open when running these functions.
- The workbook cell locations are hardcoded into this script. If the variables
  in the input file are ever moved around, this script must be updated.
"""

# Dependencies
import openpyxl as op
import win32com.client as win32
from win32com.client import Dispatch

### FUNCTIONS ### (alphabetical order of function name)


# Scenario Name 
def scenario_name(name,workbook):
    """ This function changes the name of the scenario. 
    INPUT 
    name: scenario name (str)
    workbook: excel workbook (str)
    """

    excel = win32.DispatchEx('Excel.Application')
    wb = excel.Workbooks.Open(workbook) 
    ws = wb.Worksheets("Main")
    ws.Range("E15").Value = name
    wb.Save()
    excel.Application.Quit()
    return 


# Burnup
def equilibrium_burnup(burnup,reactors,workbook):
    """ This function updates the reactor equilibrium burnup for 
    selected reactors in the excel workbook 
    INPUT 
    power: reactor burnup, units in GWd/t (double)
    reactors: list of reactor numbers to update (string of int)
              EG: [1,2,3]
    workbook: excel workbook (str)
    """

    excel = win32.DispatchEx('Excel.Application')
    wb = excel.Workbooks.Open(workbook) 
    ws = wb.Worksheets('Reactors')
    reactor_list = {1:'F11', 2:'F12', 3:'F13', 4:'F14',5:'F15'}
    for x in range(len(reactors)): 
        ws.Range(reactor_list[reactors[x]]).Value = burnup
    wb.Save()
    excel.Application.Quit()
    return


# Used Fuel Cooling Time
def cooling_time(time,cooling_list,workbook):
    """ This function updates the used fuel cooling time for selected 
    reactor in the excel workbook 
    INPUT 
    time: length of time (years) to cool the UNF for (double)
    cooling_list: list of reactor numbers to update (list of int)
                  EG: [1,2,3]
    workbook: excel workbook (str)
    """

    excel = win32.DispatchEx('Excel.Application')
    wb = excel.Workbooks.Open(workbook) 
    ws = wb.Worksheets("Fuel cycle")
    reactor_list = {1:'C9', 2:'D9', 3:'E9', 4:'F9',5:'G10'}
    for x in range(len(cooling_list)): 
        ws.Range(reactor_list[cooling_list[x]]).Value = time
    wb.Save()
    excel.Application.Quit()
    return 


def fleetshare_introdate_reactor(first_year,start_year,start_share,transition_year,transition_share,workbook): 
    """ This function updates the fleetshare of reactors. 
    From first_year to start_year, fleet share is 100% first reactor. 
    From start_year to transition_year, fleet share is start_share values. 
    From transition_year to 300 years after first_year, fleet share is transition_share values.
    INPUT 
    first_year: first year of simulation (int)
    start_year: start year of simulation (can be same as first_year) (int)
    start_share:list of fleet share percentages for each reactor. 
                For example: [0,11,89] would be a fleet share of 
                0% of reactor 1, 11% of reactor 2 and 89% of 
                reactor 3 (list) 
    transition_year: year that new reactor technology is introduced. (int)
                The range of years is 1 to 300. So, if you have a 
                starting date of 2000 for your simulation and you 
                want the introduction to start at 2010, you must 
                enter the year 10. 
    transition_share:list of fleet share percentages for each reactor. 
                     For example: [0,11,89] would be a fleet share of 
                     0% of reactor 1, 11% of reactor 2 and 89% of 
                     reactor 3 (list) 
    workbook: excel workbook (str)
    """

    excel = win32.DispatchEx('Excel.Application')
    wb = excel.Workbooks.Open(workbook) 
    ws = wb.Worksheets('Reactors')
    N = start_year - first_year
    for x in range(1,N+1): 
        for y in range(len(start_share)): 
            col = chr(97+12+y).upper()
            row = str(x + 24) 
            if y == 0:
                ws.Range(col+row).Value = 100
            else:
                ws.Range(col+row).Value = 0   
    M = transition_year-first_year
    for x in range(N+1,M+1):
        for y in range(len(start_share)): 
            col = chr(97+12+y).upper()
            row = str(x + 24) 
            ws.Range(col+row).Value = start_share[y]
    for x in range(M+1,301): 
        for y in range(len(transition_share)): 
            col = chr(97+12+y).upper()
            row = str(x + 24) 
            ws.Range(col+row).Value = transition_share[y]
    wb.Save()
    excel.Application.Quit()
    return 


# Natural Enrichment 
def natural_enrichment(enrichment,workbook):
    """ This function updates the natural enrichment for all
    reactors in the excel workbook 
    INPUT 
    enrichment: natural enrichment for all reactors, units: wt% (double)
    workbook: excel workbook (str)
    """    
    excel = win32.DispatchEx('Excel.Application')
    wb = excel.Workbooks.Open(workbook) 
    ws = wb.Worksheets('Fuel Composition')
    ws.Range("E6").Value = enrichment
    wb.Save()
    excel.Application.Quit()
    return

# Reactor Power 
def reactor_power(power,reactors,workbook):
    """ This function updates the reactor power for selected 
    reactors in the excel workbook 
    INPUT 
    power: reactor power, units: MW (double)
    reactors: list of reactor numbers to update (string of int)
              EG: [1,2,3]
    workbook: excel workbook (str)
    """

    excel = win32.DispatchEx('Excel.Application')
    wb = excel.Workbooks.Open(workbook) 
    ws = wb.Worksheets('Reactors')
    reactor_list = {1:'C11', 2:'C12', 3:'C13', 4:'C14',5:'C15'}
    for x in range(len(reactors)): 
        ws.Range(reactor_list[reactors[x]]).Value = power
    wb.Save()
    wb.Close()
    excel.Application.Quit()
    return

reactor_power(1100,[1],'C:/Users/gchee/Documents/Dymond6/DYMOND-6-User-Dakota/Input.xlsx')

# Reprocessing Plant Capacity 
def reprocessing_capacity(capacity,reprocessing_plants,workbook):
    """ This function updates the reprocessing plant capacity 
    for selected reprocessing plants in the excel workbook 
    INPUT 
    capacity: reprocessing plant capacity, units: t/year (double)
    reprocessing_plants: list of reprocessing plant numbers to update (string of int)
                        EG: [1,2,3]
    workbook: excel workbook (str)
    """

    excel = win32.DispatchEx('Excel.Application')
    wb = excel.Workbooks.Open(workbook) 
    ws = wb.Worksheets('Fuel cycle')
    reprocessing_plant_list = {1:'C27', 2:'D27', 3:'E27'}
    for x in range(len(reprocessing_plants)): 
        ws.Range(reprocessing_plant_list[reprocessing_plants[x]]).Value = capacity
    wb.Save()
    excel.Application.Quit()
    return
