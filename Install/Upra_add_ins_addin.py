import os
import arcpy
import pythonaddins

class AptiTool(object):
    """Implementation for Upra_add_ins_addin.tool (Tool)"""
    def __init__(self):
        self.enabled = True
        self.varpath = r''
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
        self.x = 0
        self.y = 0
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
        elif os.path.exists(gdbpath + r'\1_VARIABLE.gdb'):
            varpath = r''+ gdbpath + r'\1_VARIABLE.gdb'
            arcpy.env.workspace = varpath
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
        else:
            pythonaddins.MessageBox("GDB for Variables don't exist", "Error GDB is not present")
        Listvars.refresh()
        for layer in dts:
            Listvars.items.append(layer)
        self.x = x
        self.y = y
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
        print tool.varpath,selection
        addLayer = arcpy.mapping.Layer(tool.varpath + selection)
        print addLayer
        pythonaddins.MessageBox("Cargando: %s"%(tool.varpath + selection), "Carga Layer")
        arcpy.mapping.AddLayer(df, addLayer, "TOP")
        layer = arcpy.CreateFeatureclass_management(r'{0}\Users\{1}\Documents\ArcGIS\Default.gdb'.format(os.environ['systemdrive'],os.environ['username']), "data", "POINT").getOutput(0)
        fcaux = r'{0}\Users\{1}\Documents\ArcGIS\Default.gdb\data'.format(os.environ['systemdrive'],os.environ['username'])
        ras = arcpy.mapping.ListLayers(mxd)
        ras = [ i for i in ras if i.isRasterLayer]
        names = [i.name for i in ras]
        [arcpy.AddField_management (fcaux, field_name=i.name, field_type="TEXT") for i in ras]
        vec = [ i for i in ras if not i.isRasterLayer and i.name != 'data']
        rdat = [arcpy.GetCellValue_management(i.name,"{} {}".format(tool.x,tool.y),"1").getOutput(0) for i in ras]
        print rdat
        fields = ["SHAPE@XY"]
        fields.extend(names)
        cursor = arcpy.da.InsertCursor(fcaux, fields)
        xy = (tool.x, tool.y)
        fields = [xy]
        fields.extend(rdat)
        cursor.insertRow(fields)
        extent = arcpy.Extent(tool.x-5000, tool.y-5000, tool.x+5000, tool.y+5000)
        #tool.deactivate()
        mxd = arcpy.mapping.MapDocument("CURRENT")
        lyr=arcpy.mapping.ListLayers(mxd)
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        lyr = arcpy.mapping.ListLayers(mxd, "data", df)[0]
        arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", ' "OBJECTID" = 1 ')
        #df.zoomToSelectedFeatures()
        df.extent = extent#lyr.getSelectedExtent()

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