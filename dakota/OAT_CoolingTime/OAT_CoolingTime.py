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
scenario_name = 'CT' + str(round(params['CT']))
dymond6_input = os.path.normpath(os.getcwd()+os.sep+os.pardir+os.sep+os.pardir) + '\dymond6\Input.xlsx'
inp.scenario_name(name=scenario_name, workbook=dymond6_input)
inp.cooling_time(time=params['CT'], cooling_list=[1,2,3], workbook=dymond6_input)

# Run Dymond6 with edited input file 
dymond_run = os.path.normpath(os.getcwd()+os.sep+os.pardir+os.sep+os.pardir) + '\dymond6\DYMOND-6_windows.bat'
subprocess.call([dymond_run])

# ----------------------------
# Return the results to Dakota
# ----------------------------
for i, r in enumerate(results.responses()):
    if r.asv.function:
        r.function = 0
results.write()
