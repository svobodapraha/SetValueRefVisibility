import wx
import pcbnew

debugFile = r"e:\vlada_data\KICAD_TEST_PY\PY\debug.txt"

class SimpleGui(wx.Dialog):
    def __init__(self, parent, board):
        self.currentBoard = board
        wx.Dialog.__init__(self, parent, title="SET VALUE VISIBILITY")
        self.panel = wx.Panel(self)
        self.label = wx.StaticText(self.panel, label = "Hello World1")
        self.label.SetLabel("new Value")
        buttonShowValues = wx.Button(self.panel, label="Show Values", id=1)
        buttonHideValues = wx.Button(self.panel, label="Hide Values", id=2)
        buttonShowRef   = wx.Button(self.panel,  label="Show Ref",    id=3)
        buttonHideRef   = wx.Button(self.panel,  label="Hide Ref",    id=4)
        self.cbSelectedOnly   = wx.CheckBox(self.panel, label = "Selected Only")
        nets = board.GetNetsByName()
        self.netnames = []
        for netname, net in nets.items():
            if (str(netname) == ""):
                continue
            self.netnames.append(str(netname))
        netcb = wx.ComboBox(self.panel, choices=self.netnames)
        netcb.SetSelection(0)
        netsbox = wx.BoxSizer(wx.HORIZONTAL)
        netsbox.Add(wx.StaticText(self.panel, label="Nets:"))
        netsbox.Add(netcb, proportion=1)
        self.modules = board.GetModules()
        self.modulenames = []
        for mod in self.modules:
            self.modulenames.append("{}({})".format(mod.GetReference(), mod.GetValue()))
        modcb = wx.ComboBox(self.panel, choices=self.modulenames)
        modcb.SetSelection(0)
        modsbox = wx.BoxSizer(wx.HORIZONTAL)
        modsbox.Add(wx.StaticText(self.panel, label="Modules:"))
        modsbox.Add(modcb, proportion=1)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.label,   proportion=0)
        box.Add(buttonShowValues,    proportion=0)
        box.Add(buttonHideValues,    proportion=0)
        box.Add(buttonShowRef,       proportion=0)
        box.Add(buttonHideRef,       proportion=0)
        box.Add(self.cbSelectedOnly, proportion=0)
        box.Add(netsbox,             proportion=0)
        box.Add(modsbox,             proportion=0)
        self.panel.SetSizer(box)
        self.Bind(wx.EVT_BUTTON, self.OnPressShowValue, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnPressHideValue, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnPressShowRef,   id=3)
        self.Bind(wx.EVT_BUTTON, self.OnPressHideRef,   id=4)
        self.Bind(wx.EVT_COMBOBOX, self.OnSelectNet, id=netcb.GetId())
        self.Bind(wx.EVT_COMBOBOX, self.OnSelectMod, id=modcb.GetId())
        with open(debugFile, 'a') as f:
          f.write("new exec")
          f.write("\n")

    def OnPressShowValue(self, event):
        onlySelected = self.cbSelectedOnly.GetValue()
        print("in OnPressShowValue")
        self.label.SetLabel("in OnPressShowValue" + " " + str(onlySelected))
        with open(debugFile, 'a') as f:
          f.write("in OnPressShowValue")
          f.write("\n")
        for module in self.modules:
          if(module.IsSelected() or (not onlySelected)):
            module.Value().SetVisible(True)
        self.currentBoardRefresh()
        
          
    def OnPressHideValue(self, event):
        onlySelected = self.cbSelectedOnly.GetValue()
        print("in OnPressHideValue")
        self.label.SetLabel("in OnPressHideValue"  + " " + str(onlySelected))
        with open(debugFile, 'a') as f:
          f.write("in OnPressHideValue")
          f.write("\n")
        for module in self.modules:
          if(module.IsSelected() or (not onlySelected)):
            module.Value().SetVisible(False)
        self.currentBoardRefresh()
    
    def OnPressShowRef(self, event):
        onlySelected = self.cbSelectedOnly.GetValue()
        print("in OnPressShowRef")
        self.label.SetLabel("in OnPressShowRef" + " " + str(onlySelected))
        with open(debugFile, 'a') as f:
          f.write("in OnPressShowRef")
          f.write("\n")
        for module in self.modules:
          if(module.IsSelected() or (not onlySelected)):
            module.Reference().SetVisible(True)
        self.currentBoardRefresh()
  
    def OnPressHideRef(self, event):
        onlySelected = self.cbSelectedOnly.GetValue()
        print("in OnPressHideRef")
        self.label.SetLabel("in OnPressHideRef"  + " " + str(onlySelected))
        with open(debugFile, 'a') as f:
          f.write("in OnPressHideRef")
          f.write("\n")
        for module in self.modules:
          if(module.IsSelected() or (not onlySelected)):
            module.Reference().SetVisible(False)
        self.currentBoardRefresh()
                  
    def OnSelectNet(self, event):
        item = event.GetSelection()
        print("Net {} was selected".format(self.netnames[item]))
        self.label.SetLabel("Net {} was selected".format(self.netnames[item]))
        with open(debugFile, 'a') as f:
          f.write("Net {} was selected".format(self.netnames[item]))
          f.write("\n")
          
    def OnSelectMod(self, event):
        item = event.GetSelection()
        print("Module {} was selected".format(self.modulenames[item]))
        self.label.SetLabel("Module {} was selected".format(self.modulenames[item]))
        with open(debugFile, 'a') as f:
          f.write("Module {} was selected".format(self.modulenames[item]))
          f.write("\n")
        



#run from menu - action plugin
class SetValueRefVisibility(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Set Value and Ref Visibility V7"
        self.category = "Modify PCB"
        self.description = "Set value and reference visibility globaly"
        
    def Run(self):

        sg = SimpleGui(None, pcbnew.GetBoard())
        sg.ShowModal()
 

 #register in Kicad
SetValueRefVisibility().register()
        


#http://www.wxformbuilder.org/
#execute from interpreter:
#exec(open(r"e:\vlada_data\KICAD_TEST_PY\PY\myTestGUI.py").read()) 



        
        