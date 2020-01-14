from os import sys,system,remove,replace
import getopt
import polib
import base64
from shutil import copyfile
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter.ttk import *

args = sys.argv[1:]

class PyTranslater(Tk):

    def __init__(self,file=None,GUI=True):
        self.oheader = None
        self.ofile = None
        self.saved = True
        self.msgs  = polib.POFile()

        
        self.GUI = GUI
        Tk.__init__(self)
        self.title("PyTranslater")
        try:
            self.iconbitmap("./PyTranslater.ico")
        except Exception as err:
            pass
        self.protocol("WM_DELETE_WINDOW",self.__onClose__)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.__createGUIContent__()
        if file:
                self.openFile(file)
        if GUI:
            self.mainloop()
        "For IDE, cause VS is stupid"
        
    def __createGUIContent__(self):
        self.menu = Menu(tearoff=0)

        self.filemenu = Menu(tearoff=0)
        self.filemenu.add_command(label="Create new POT File",command=self.__createTemplate__,accelerator="Ctrl+N")
        self.filemenu.add_command(label="Open",command=self.__openFile__,accelerator="Ctrl+O")
        self.filemenu.add_command(label="Save",command=self.__save__,accelerator="Ctrl+S",state=DISABLED)
        self.filemenu.add_command(label="Save as",command=self.__saveAs__,accelerator="Shift+Ctrl+S",state=DISABLED)
        self.filemenu.add_command(label="Export",command=self.__export__,accelerator="Ctrl+E",state=DISABLED)
        self.filemenu.add_command(label="Quit",command=self.destroy,accelerator="Ctrl+Q",state=DISABLED)
        self.bind("<Control-n>",self.__createTemplate__)
        self.bind("<Control-o>",self.__openFile__)
        self.bind("<Control-s>",self.__save__)
        self.bind("<Control-S>",self.__saveAs__)
        self.bind("<Control-e>",self.__export__)
        self.bind("<Control-q>",self.destroy)

        self.menu.add_cascade(label="File",menu=self.filemenu)
        self.configure(menu=self.menu)

        self.lstmsgpan = Panedwindow(self,orient=HORIZONTAL)
        self.lstmsgpan.grid(row=0,column=0,sticky=N+W+E+S,columnspan=2)
        self.lstMsgId = Listbox(self.lstmsgpan)
        self.lstMsgId.bind("<Double-Button-1>",self.__editMsgID__)
        self.lstmsgpan.add(self.lstMsgId)#self.lstMsgId.grid(row=0,column=0,sticky=N+W+E+S)

        self.lstMsgContent = Listbox(self.lstmsgpan)
        self.lstMsgContent.bind("<Double-Button-1>",self.__editMsgContent__)
        self.lstmsgpan.add(self.lstMsgContent)#.grid(row=0,column=1,sticky=N+E+S+W)
    
    def createTemplate(self,pyfile,potfile):
        "Create a POT File from a Python Script with gettext Strings"
        system('pygettext.exe --no-location -d {} "{}"'.format(potfile.replace(".pot",""),pyfile))

    class NewTemplate(Toplevel):

        def __init__(self,master):
            Toplevel.__init__(self,master)
            self.id = id
            self.edit = edit
            self.master = master

            Toplevel.__init__(self,master)
            self.title(self.id)
            self.columnconfigure(0,weight=1)
            self.rowconfigure(1,weight=1)
            self.attributes("-tool",1)

            self.field = Text(self)
            self.field.insert(END,content)
            self.field.grid(sticky=N+E+S+W)

            self.ok = Button(self,text="Okay",command=self.__okay__)
            self.ok.grid(sticky=E+S)
            self.mainloop()

    def __createTemplate__(self,*event):
        
        pyFilePH = filedialog.askopenfilename(title="Python File",filetypes=(("Py-File","*.py *.pyw"),("All-Files","*.*")))
        if pyFilePH:
            potFilePH = filedialog.asksaveasfilename(title="Save POT",filetypes=(("POT File","*.pot"),),defaultextension=".pot")
            if potFilePH:
                self.createTemplate(pyFilePH,potFilePH)
                if askyesno(title="Open POT File",message="Do you want to open the created POT file?"):
                    self.openFile(potFilePH)
                    self.__refresh__()
        "For IDE, cause VS is stupid"
  
    def openFile(self,filepath):
        self.msgs = polib.pofile(filepath)
        self.saved = True

    def __openFile__(self,*event):
        if not self.saved:
            if not self.__unsaved__():
                return 
        filepath = filedialog.askopenfilename(title="Open POT or PO File",filetypes=(("Translation Files","*.pot *.po"),))
        if filepath:
            self.openFile(filepath)
            self.__refresh__()
        "For IDE, cause VS is stupid"


    def save(self,filepath):
        self.msgs.save(filepath)
        self.saved = True

    def __save__(self,*event):
        if not self.saved:
            self.save(self.ofile)
            self.__refresh__()

    def __saveAs__(self,*event):
        if not self.saved:
            filepath = filedialog.asksaveasfilename(title="Save as PO",filetypes=(("Translation File","*.po"),),defaultextension=".po")
            if filepath:
                self.save(filepath)
                self.__refresh__()

    def export(self,file):
        self.msgs.save_as_mofile(file)

    def __export__(self,*event):
        filepath = filedialog.asksaveasfilename(title="Export as MO",filetypes=(("Compiled Translation File","*.mo"),),defaultextension=".mo")
        if filepath:
            self.export(filepath)
            self.__refresh__()

    def editContent(self,msgid,msg):
        self.saved = False
        print(msg)
        self.msgs.find(msgid).msgstr = msg
       
    def editID(self,oldmsgid,newmsgid):
        self.saved = False
        if oldmsgid != "":
            self.msgs.find(oldmsgid).msgid = newmsgid
        else:
            self.msgs.append(polib.POEntry(msgid=newmsgid,msgstr=""))
        
    def deleteItem(self,msgid):

        self.msgs.remove(self.msgs.find(msgid))

    class ContetEdit(Toplevel):
        def __init__(self,master,id,content,edit):
            "Window with Textfield"
            self.id = id
            self.edit = edit
            self.master = master

            Toplevel.__init__(self,master)
            self.title(self.id)
            self.columnconfigure(0,weight=1)
            self.rowconfigure(1,weight=1)
            self.attributes("-tool",1)

            self.field = Text(self)
            self.field.insert(END,content)
            self.field.grid(columnspan=2,sticky=N+E+S+W)
            
            self.delete = Button(self,text="Delete",command=self.__delete__,state=NORMAL if id != "" else DISABLED)
            self.delete.grid(row=1,column=0,sticky=W+S)

            self.ok = Button(self,text="Okay",command=self.__okay__)
            self.ok.grid(row=1,column=1,sticky=E+S)
            self.mainloop()

        def __okay__(self):
            content = self.field.get(0.0,END)[:-1]
            if content != "":
                self.edit(self.id,content)
                self.master.__refresh__()
                self.destroy()

        def __delete__(self):
            self.master.deleteItem(self.id)
            self.master.__refresh__()
            self.destroy()
    

    def __editMsgContent__(self,*event):
        contid  = self.lstMsgContent.curselection()
        msgid   = self.lstMsgId.get(contid)
        self.ContetEdit(self,msgid,self.msgs.find(msgid).msgstr,self.editContent)
        
    def __editMsgID__(self,*event):
        id   = self.lstMsgId.curselection()
        msgid   = self.lstMsgId.get(id)
        msgid = msgid if msgid != self.lstMsgId.get(END) else ""
        self.ContetEdit(self,msgid,msgid,self.editID)


    def __refresh__(self,*event):
        self.filemenu.entryconfig(2,state=DISABLED if self.saved else NORMAL)
        self.filemenu.entryconfig(3,state=DISABLED if self.saved else NORMAL)
        self.filemenu.entryconfig(4,state=NORMAL if self.saved else DISABLED)

        self.lstMsgId.delete(0,END)
        self.lstMsgContent.delete(0,END)
        for msg in self.msgs:
            self.lstMsgId.insert(END,msg.msgid)
            self.lstMsgContent.insert(END,repr(msg.msgstr))
        self.lstMsgId.insert(END,"+".center(10))

    def __unsaved__(self,*event):
        anwser = askyesnocancel(title="Save changes?",message="Do you want to save the file?")
        if anwser:
            self.save(self.ofile)
        elif anwser == None:
            return False
        return True
        
    def __onClose__(self,*event):
        if not self.saved:
            if not self.__unsaved__():
                return
        self.destroy()


PyTranslater()