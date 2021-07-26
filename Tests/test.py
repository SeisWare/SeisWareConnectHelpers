import SWconnect

project_list = SWconnect.sw_project_list()

for i in project_list:
    print(i.Name())

proj = SWconnect.sw_connect(project_list[0].Name())

print(f"The project name is {project_list[0].Name()}")

wells = SWconnect.get_all_wells(proj)

for i in wells:
    print(i.UWI())

well = SWconnect.get_well(proj,wells[0].UWI())

print(f"Well UWI is 100012308424W600")

survey_well = SWconnect.get_well(proj,"100012308424W600")

survey = SWconnect.get_srvy(proj,survey_well)

print(survey)

log_well = "100013208721W600"
log_name = "DT"

print(f"Log curve for well {log_well}")

well = SWconnect.get_well(proj,log_well)

log_curves = SWconnect.get_log_curve(proj,well,log_name)

print(log_curves)