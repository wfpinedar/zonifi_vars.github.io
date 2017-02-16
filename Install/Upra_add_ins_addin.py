import os
import arcpy
import pythonaddins

class AptiTool(object):
    """Implementation for Upra_add_ins_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.varpath = r''
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
    def get_geodatabase_path(self, input_table):
        '''Return the Geodatabase path from the input table or feature class.
        :param input_table: path to the input table or feature class
        '''
        #workspace = os.path.dirname(input_table)
        workspace = input_table
        if not [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
            return workspace
        else:
            return os.path.dirname(workspace)
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        Listvars.items = []
        a = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        gdbpath = self.get_geodatabase_path(a.workspacePath)
        message = "Your mouse clicked \n longitud: " + str(x) + ", \n Latitud: " + str(y) + "\n And your selected layer is: " + a.name + "\n Located in gdb: " + a.workspacePath + "\n And GDB PATH is: " + gdbpath
        #pythonaddins.MessageBox(message, "My Coordinates")
        varpath = gdbpath + r'\1_VARIABLES.gdb'
        listFC = []
        dts = []
        ft = []
        if os.path.exists(varpath):
            #pythonaddins.MessageBox(varpath, "GDB for Variables")
            arcpy.env.workspace = r''+varpath
            print arcpy.env.workspace
            #listFC = arcpy.ListFeatureClasses(wild_card="V_*")
            ras =  arcpy.ListRasters(wild_card="V_*")
            dt = arcpy.ListDatasets()
            for d in dt:
                ft = arcpy.ListFeatureClasses(wild_card="V*", feature_type = 'All', feature_dataset = d)
                dta= [d + '\\' + f for f in ft]
                dts.extend(dta)
                listFC.extend(ft)
            listFC.extend(ras)
            dts.extend(ras)
            #pythonaddins.MessageBox(listFC, "Variables")
            #pythonaddins.MessageBox(dts, "Variables")
        else:
            pythonaddins.MessageBox("GDB for Variables don't exist", "Error GDB is not present")
        Listvars.refresh()
        for layer in dts:
            Listvars.items.append(layer)
        tool.deactivate()
        pass
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        pass
    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        pass
    def onRectangle(self, rectangle_geometry):
        pass

class Listvars(object):
    """Implementation for Upra_add_ins_addin.Listvars (ComboBox)"""
    def __init__(self):
        self.items = []
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
        self.width = 'WWWWWWWWWWWWWWWWWWWWW'
    def onSelChange(self, selection):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        addLayer = arcpy.mapping.Layer(tool.varpath + selection)
        pythonaddins.MessageBox("Cargando: %s"%(tool.varpath + selection), "Carga Layer")
        arcpy.mapping.AddLayer(df, addLayer, "TOP")
        tool.deactivate()
        pass
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        self.items = []
        pass

class UpdateLayers(object):
    """Implementation for Upra_add_ins_addin.UpdateLayers (Extension)"""
    def __init__(self):
        # For performance considerations, please remove all unused methods in this class.
        self.enabled = True
    def itemAdded(self, new_item):
        pass
    def itemDeleted(self, deleted_item):
        pass