import wx
import  wx.html as  html
import Mod_ProductData


class Frame_Main(wx.App):
    def OnInit(self):
        self.frame1 = MyFrame("cposs1 At your service", (0, 0), (1200, 800))
        self.frame1.Show()
        self.SetTopWindow(self.frame1)
        return True



class MyFrame(wx.Frame):
    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        iconFile = "plus1.ico"
        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)        
        menuFile = wx.Menu()
        menuFile.Append(1, "&About...")
        menuFile.AppendSeparator()
        menuFile.Append(2, "E&xit")
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&File")
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")

        sb = wx.StaticBox(self, -1, "Options")
        searchBtnOpt = wx.CheckBox(self, -1, "Search button")
        searchBtnOpt.SetValue(True)
        cancelBtnOpt = wx.CheckBox(self, -1, "Cancel button")
        menuBtnOpt   = wx.CheckBox(self, -1, "Search menu")

        self.search = wx.SearchCtrl(self, size=(200,-1), style=wx.TE_PROCESS_ENTER)

        self.TxtItemDetails={}
        

        # Setup the layout
        box = wx.StaticBoxSizer(sb, wx.VERTICAL)
        box.Add(searchBtnOpt, 0, wx.ALL, 5)
        box.Add(cancelBtnOpt, 0, wx.ALL, 5)
        box.Add(menuBtnOpt,   0, wx.ALL, 5)

        self.Receipt = HTMLBasket(self, -1)
        box.Add(self.Receipt, 0, wx.ALL, 5)
        GetBasket(2,self.Receipt)

        
        
        for ControlName in [ "Heading", "Description", "Detail1", "Detail2", "Price" ]:
            self.TxtItemDetails[ControlName]=wx.TextCtrl(self, -1, "%s" % ControlName, size=(125, -1))
            box.Add(self.TxtItemDetails[ControlName], 0, wx.ALL, 15)
        print(self.TxtItemDetails["Description"])
        print(self.TxtItemDetails["Detail1"])
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(box, 0, wx.ALL, 35)
        sizer.Add((15,15))
        sizer.Add(self.search, 0, wx.ALL, 15)

        self.SetSizer(sizer)

        # Set event bindings for search panel
        self.Bind(wx.EVT_CHECKBOX, self.OnToggleSearchButton, searchBtnOpt)
        self.Bind(wx.EVT_CHECKBOX, self.OnToggleCancelButton, cancelBtnOpt)
        self.Bind(wx.EVT_CHECKBOX, self.OnToggleSearchMenu,   menuBtnOpt)

        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearch, self.search)
        ##self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel, self.search)
        ##self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.search)
        ##self.Bind(wx.EVT_TEXT, self.OnDoSearch, self.search) 
        self.Bind(wx.EVT_MENU, self.OnAbout, id=1)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=2)

    def OnQuit(self, event):
        self.Close()
        
    def OnAbout(self, event):
        wx.MessageBox("This is a wxPython Hello world sample",
        "About Hello World", wx.OK | wx.ICON_INFORMATION, self)    

    def OnToggleSearchButton(self, evt):
        self.search.ShowSearchButton( evt.GetInt() )
            
    def OnToggleCancelButton(self, evt):
        self.search.ShowCancelButton( evt.GetInt() )
        
    def OnToggleSearchMenu(self, evt):
        if evt.GetInt():
            self.search.SetMenu( self.MakeMenu() )
        else:
            self.search.SetMenu(None)

    def OnSearch(self, evt):        
        ItemID=int(self.search.GetValue() or 0)
        ItemDetails=Mod_ProductData.ProductDictionary(ItemID) 
        for ControlName in [ "Heading", "Description", "Detail1", "Detail2", "Price" ]:
            self.TxtItemDetails[ControlName].SetValue(ItemDetails[ControlName])
        GetBasket(2,self.Receipt)
            
    def OnCancel(self, evt):
        print("OnCancel")

    def OnDoSearch(self, evt):
        print("OnDoSearch: " + self.search.GetValue())
        

    def MakeMenu(self):
        menu = wx.Menu()
        item = menu.Append(-1, "Recent Searches")
        item.Enable(False)
        for txt in [ "You can maintain",
                     "a list of old",
                     "search strings here",
                     "and bind EVT_MENU to",
                     "catch their selections" ]:
            menu.Append(-1, txt)
        return menu



class HTMLBasket(html.HtmlWindow):
    def __init__(self, parent, id):
        html.HtmlWindow.__init__(self, parent, id, style=wx.NO_FULL_REPAINT_ON_RESIZE,pos=(0,30), size=(602,310))
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()
       
    def OnLinkClicked(self, linkinfo):
        Req=linkinfo.GetHref().split(',')
        if Req[0]=='#Add':
            print "Add item %s" % Req[1]
            Mod_ProductData.AddToBasket(int(Req[1]),BasketID=2,Qty=1)
        elif Req[0]=='#Del':
            print "Del item %s" % Req[1]
            Mod_ProductData.AddToBasket(int(Req[1]),BasketID=2,Qty=-1)
        else:
            print('OnLinkClicked: %s\n' % linkinfo.GetHref())
        super(HTMLBasket, self).OnLinkClicked(linkinfo)
        GetBasket(2,self.Receipt)
        
def GetBasket(BasketID, UpdateObj):
    BasketDict=Mod_ProductData.ReturnBasket(BasketID)
    TempHTML=""
    for ItemDetail in BasketDict:
        TempHTML=TempHTML + "%s %s %s %s %s %s <a name='Add,%s' href='#Add,%s'>Add</a> <a name='Del,%s' href='#Del,%s'>Remove</a><br>" % (ItemDetail["ItemID"],ItemDetail["Heading"],
                                                       ItemDetail["Detail1"],ItemDetail["Detail2"],
                                                       ItemDetail["Price"],ItemDetail["Qty"],
                                                       ItemDetail["ItemID"], ItemDetail["ItemID"],
                                                        ItemDetail["ItemID"], ItemDetail["ItemID"])
    
    #print(Application.frame1.TxtItemDetails["Detail1"] or 'Not found')
    UpdateObj.SetPage(TempHTML)




if __name__ == '__main__':
    app = wx.App()
    MyFrame = Frame_Main(False)
    app.MainLoop()
    
