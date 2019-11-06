# Dakota Python Driving Script

# necessary python modules
import dakota.interfacing as di
import subprocess
import sys
import os 
sys.path.append('../../scripts')
import input as inp
import output as oup

# ----------------------------
# Parse Dakota parameters file
# ----------------------------
params, results = di.read_parameters_file()

# -------------------------------
# Convert and send to Dymond
# -------------------------------
# Edit Dymond6 input file
scenario_name = 'RP' + str(round(params['x1']))
dymond6_input = os.path.normpath(os.getcwd()+os.sep+os.pardir+os.sep+os.pardir) + '\dymond6\Input.xlsx'
inp.scenario_name(name=scenario_name, workbook=dymond6_input)
inp.reactor_power(power=params['x1'], workbook=dymond6_input, reactors=[1])

# Run Dymond6 with edited input file 
dymond_run = os.path.normpath(os.getcwd()+os.sep+os.pardir+os.sep+os.pardir) + '\dymond6\DYMOND-6_windows.bat'
subprocess.call([dymond_run])

# ----------------------------
# Return the results to Dakota
# ----------------------------
dymond6_output = oup.get_dataframe(os.path.normpath(os.getcwd()+os.sep+os.pardir+os.sep+os.pardir) + '\dymond6\Output database.xlsx')
for i, r in enumerate(results.responses()):
    if r.asv.function:
        r.function, val  = oup.grep_database(dymond6_output, 
                                        scenario_name,
                                        'Reactors',
                                        'Installed capacity',
                                        'final',
                                        reactor_all=False,
                                        reactor_list=[1])
results.write()
