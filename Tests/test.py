import SWconnect

#Connect to the SeisWare project list
project_list = SWconnect.sw_project_list()

#Print a list of all the projects
for i in project_list:
    print(i.Name())

#Connect to first project in the project list
any_project = SWconnect.sw_connect(project_list[0].Name())

print("The first project in the list is: %s" % (project_list[0].Name()))

#Connect to a specific project
project = SWconnect.sw_connect("SeisWare SDK Trial Data Set")

#Grab all the wells for the specified project
wells = SWconnect.get_all_wells(project)

for i in wells:
    print(i.UWI())

#Grab the UWI for a specific well in the well list
well = SWconnect.get_well(project,"Well 1")
print("Well UWI is %s" % (well.UWI()))

#Grab all the directional surveys for the selected well in the project
directional_survey_well = SWconnect.get_well(project, well.UWI())

directional_survey = SWconnect.get_srvy(project, directional_survey_well)

#Print the directional survey
print(directional_survey)

#Specify the UWI and Curve Name we want to grab
log_well = "Well 1"
log_name = "DT"

print(f"Log curve for well {log_well}")

#Get the well object
well = SWconnect.get_well(project,log_well)

#Get the specified log curve for the specified well object
log_curves = SWconnect.get_log_curve(project,well,log_name)

#Print the specified log curve's depth and value pairs
print(log_curves)

#Grab a specific horizon for the specified project
horizon = SWconnect.get_horizon(project,"3D", "p1000")
print(horizon)
