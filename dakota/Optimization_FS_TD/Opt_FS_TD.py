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
scenario_name = 'FS' + str(round(params['FS'])) + 'TY' + str(round(params['TY']))
dymond6_input = os.path.normpath(os.getcwd()+os.sep+os.pardir+os.sep+os.pardir) + '\dymond6\Input.xlsx'
inp.scenario_name(name=scenario_name, workbook=dymond6_input)
inp.fleetshare_introdate_reactor(first_year=70,
                                 start_year=77,
                                 start_share=[0,0,100],
                                 transition_year=int(params['TY']),
                                 transition_share=[0, params['FS'], 100-params['FS']],
                                 workbook=dymond6_input)

# Run Dymond6 with edited input file 
dymond_run = os.path.normpath(os.getcwd()+os.sep+os.pardir+os.sep+os.pardir) + '\dymond6\DYMOND-6_windows.bat'
subprocess.call([dymond_run])

# ----------------------------
# Return the results to Dakota
# ----------------------------
dymond6_output = oup.get_dataframe(os.path.normpath(os.getcwd()+os.sep+os.pardir+os.sep+os.pardir) + '\dymond6\Output database.xlsx')
commod_list = ['Spent fuel cooling','Primary feed', 'HLW in storage']
for i, r in enumerate(results.responses()):
    if r.asv.function:
        r.function, val = oup.grep_isotopics(output_database=dymond6_output,
                                        scenario_name=scenario_name,
                                        isotopes=['Pu'],
                                        output_variable=commod_list[i],
                                        indicator='max')
results.write()
