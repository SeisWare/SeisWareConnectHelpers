# -*- coding: utf-8 -*-
"""
This is a helper function for connecting to a SeisWare Project
"""
import SeisWare
import sys 
import pandas as pd

def handle_error(message, error):
    """
    Helper function to print out the error message to stderr and exit the program.
    """
    print(message, file=sys.stderr)
    print("Error: %s" % (error), file=sys.stderr)
    sys.exit(1)

def SWprojlist():
    connection = SeisWare.Connection()
    
    try:
        serverInfo = SeisWare.Connection.CreateServer()
        connection.Connect(serverInfo.Endpoint(), 5000)
    except RuntimeError as err:
        handle_error("Failed to connect to the server", err)

    project_list = SeisWare.ProjectList()
    
    connection.ProjectManager().GetAll(project_list)
    
    return project_list

def SWconnect(project_name):
    connection = SeisWare.Connection()
    
    try:
        serverInfo = SeisWare.Connection.CreateServer()
        connection.Connect(serverInfo.Endpoint(), 5000)
    except RuntimeError as err:
        handle_error("Failed to connect to the server", err)

    project_list = SeisWare.ProjectList()

    try:
        connection.ProjectManager().GetAll(project_list)
    except RuntimeError as err:
        handle_error("Failed to get the project list from the server", err)

    projects = [project for project in project_list if project.Name() == project_name]
    if not projects:
        print("No project was found", file=sys.stderr)
        sys.exit(1)
        
    login_instance = SeisWare.LoginInstance()
    try:
        login_instance.Open(connection, projects[0])
    except RuntimeError as err:
        handle_error("Failed to connect to the project", err)
        
    return login_instance

def getWell(uwi,login_instance):
    
    well_list = SeisWare.WellList()
    
    try:
        login_instance.WellManager().GetAll(well_list)
    except RuntimeError as err:
        handle_error("Failed to get all the wells from the project", err)
        
    wells = [well for well in well_list if well.UWI() == uwi]
    
    return wells[0]


def getAllWells(login_instance):
    
    well_list = SeisWare.WellList()
    
    try:
        login_instance.WellManager().GetAll(well_list)
    except RuntimeError as err:
        handle_error("Failed to get all the wells from the project", err)
        
    wells = [well for well in well_list]
    
    return wells

'''
def wellstoDF(wells):
 #Take a list of SeisWare Well Type objects and adds it to a dataframe   
    
    return welldf
'''

def plotLog(uwi,log_curve_name,login_instance):
 #Populate Log Curve List for given well
    log_curve_list = SeisWare.LogCurveList()
    
    well = getWell(uwi,login_instance)
    
    try:
        login_instance.LogCurveManager().GetAllForWell(well.ID(), log_curve_list)
    except RuntimeError as err:
        handle_error("Failed to get the log curves of well %s from the project" % (well.UWI()), err)
    
    log_curves = [log_curve for log_curve in log_curve_list if log_curve.Name() == log_curve_name]
    
    if not log_curves:
        print("No log curve was found", file=sys.stderr)
        sys.exit(1) 
    
    try:
        login_instance.LogCurveManager().PopulateValues(log_curves[0])
    except RuntimeError as err:
        handle_error("Failed to populate the values of log curve %s of well %s from the project" % (log_curve_name, well.UWI()), err)

    log_curve_values = SeisWare.DoublesList()
    log_curves[0].Values(log_curve_values)
    
    return log_curve_values

def get_grid(login_instance, grid_name):


    return grid_df


def getsrvy(login_instance, well):
    '''
    well: SeisWare well object


    Get the directional survey based on well, login_instance.
    Return directional survey as dataframe with 
    columns 
    UWI X Y TVDSS MD
    
    '''

    surfaceX = well.TopHole().x.Value(depth_unit)
    surfaceY = well.TopHole().y.Value(depth_unit)
    surfaceDatum = well.DatumElevation().Value(depth_unit)

    dirsrvylist = SeisWare.DirectionalSurveyList()

    login_instance.DirectionalSurveyManager().GetAllForWell(well.ID(),dirsrvylist)

    #Select the directional survey if it exists
    dirsrvy = [i for i in dirsrvylist if i.OffsetNorthType()>0]
    
    login_instance.DirectionalSurveyManager().PopulateValues(dirsrvy[0])
    
    srvypoints = SeisWare.DirectionalSurveyPointList()
    
    dirsrvy[0].Values(srvypoints)
    
    srvytable = []
    
    for i in srvypoints:
        srvytable.append((
            well.Name(),
            surfaceX + i.xOffset.Value(depth_unit),
            surfaceY + i.yOffset.Value(depth_unit),
            surfaceDatum - i.tvd.Value(depth_unit),
            i.md.Value(depth_unit)))

    return pd.DataFrame(srvytable, columns = ['UWI','X','Y','TVDSS','MD'])


def getlogcurve(login_instance,well,log_curve_name):
    '''

    Takes well object, log curve name, and login instance to return a dataframe containing
    
    columns
    MD curvevalue

    '''
    log_curve_list = SeisWare.LogCurveList()
    
    try:
        login_instance.LogCurveManager().GetAllForWell(well.ID(), log_curve_list)
    except RuntimeError as err:
        handle_error("Failed to get the log curves of well %s from the project" % (well.UWI()), err)
    
    log_curves = [log_curve for log_curve in log_curve_list if log_curve.Name() == log_curve_name]
    
    if not log_curves:
        
        return pd.DataFrame(data=None,columns = ['MD',log_curve_name])
        #print("No log curve was found", file=sys.stderr)
        #sys.exit(1) 
    
    try:
        login_instance.LogCurveManager().PopulateValues(log_curves[0])
    except RuntimeError as err:
        handle_error("Failed to populate the values of log curve %s of well %s from the project" % (log_curve_name, well.UWI()), err)

    log_curve_values = SeisWare.DoublesList()
    log_curves[0].Values(log_curve_values)
    
    log_table = []

    for i in range(len(log_curve_values)):
        log_table.append(((log_curves[0].TopDepth()+log_curves[0].DepthInc()*i).Value(depth_unit),log_curve_values[i]))


    return pd.DataFrame(log_table,columns = ['MD',log_curve_name])

