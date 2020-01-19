from os import system,remove,replace,path,chdir
import sys
import getopt
import polib
import base64
from shutil import copyfile
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter.ttk import *
import tempfile

localdir = path.dirname(sys.argv[0]).replace("\\","/")
chdir(localdir)

args = sys.argv[1:]
print(localdir,args)
class PyTranslate(Tk):

    def __init__(self,file=None,GUI=True):
        self.oheader = None
        self.ofile = None
        self.saved = True
        self.msgs  = polib.POFile()

        self.GUI = GUI
        Tk.__init__(self)
        self.title("PyTranslate")
        self.__center__(800,500)
        try:
            self.iconbitmap("./PyTranslate.ico")
        except Exception as err:
            pass
        self.protocol("WM_DELETE_WINDOW",self.__onClose__)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.__createGUIContent__()
        
        if file:
                self.openFile(file)
                self.__refresh__()
        if GUI:
            self.mainloop()
        "For IDE, cause VS is stupid"
        
    def __center__(self,width=None,height=None):
        """Centering the Window"""
        windowWidth = width or self.winfo_reqwidth()
        windowHeight = height or self.winfo_reqheight()

        positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/2 - windowHeight/2)

        self.geometry("{}x{}+{}+{}".format(windowWidth,windowHeight,positionRight, positionDown))

    def __createGUIContent__(self):
        self.menu = Menu(tearoff=0)

        self.filemenu = Menu(tearoff=0)
        self.filemenu.add_command(label="Create new POT File",command=self.__createTemplate__,accelerator="Ctrl+N")
        self.filemenu.add_command(label="Open",command=self.__openFile__,accelerator="Ctrl+O")
        self.filemenu.add_command(label="Save",command=self.__save__,accelerator="Ctrl+S",state=DISABLED)
        self.filemenu.add_command(label="Save as",command=self.__saveAs__,accelerator="Shift+Ctrl+S",state=DISABLED)
        self.filemenu.add_command(label="Export",command=self.__export__,accelerator="Ctrl+E",state=DISABLED)
        self.filemenu.add_command(label="Quit",command=self.destroy,accelerator="Ctrl+Q",state=DISABLED)

        self.editmenu = Menu(tearoff=0)
        self.editmenu.add_command(label="Add Entrys from other Script",command=self.__addViaImport__,accelerator="Ctrl+I")

        self.bind("<Control-n>",self.__createTemplate__)
        self.bind("<Control-o>",self.__openFile__)
        self.bind("<Control-s>",self.__save__)
        self.bind("<Control-S>",self.__saveAs__)
        self.bind("<Control-e>",self.__export__)
        self.bind("<Control-q>",self.destroy)
        self.bind("<Control-i>",self.__addViaImport__)

        self.menu.add_cascade(label="File",menu=self.filemenu)
        self.menu.add_cascade(label="Edit",menu=self.editmenu)
        self.configure(menu=self.menu)

        self.lstmsgpan = Panedwindow(self,orient=HORIZONTAL)
        self.lstmsgpan.grid(row=0,column=0,sticky=N+W+E+S,columnspan=2)

        self.lstMsgId = Listbox(self.lstmsgpan,width=62)
        self.lstMsgId.bind("<Double-Button-1>",self.__editMsgID__)
        self.lstMsgId.bind("<MouseWheel>",self.__OnMouseWheel__)
        self.lstMsgId.bind("<Return>",self.__editMsgID__)
        self.lstMsgId.bind("<Delete>",self.__deleteMsgByID__)
        
        self.lstmsgpan.add(self.lstMsgId)#self.lstMsgId.grid(row=0,column=0,sticky=N+W+E+S)

        self.lstMsgContent = Listbox(self.lstmsgpan,width=65)
        self.lstMsgContent.bind("<Double-Button-1>",self.__editMsgContent__)
        self.lstMsgContent.bind("<MouseWheel>",self.__OnMouseWheel__)
        self.lstMsgContent.bind("<Return>",self.__editMsgContent__)
        self.lstMsgContent.bind("<Delete>",self.__deleteMsgByContent__)
        self.lstmsgpan.add(self.lstMsgContent)#.grid(row=0,column=1,sticky=N+E+S+W)

        
    
    def createTemplate(self,pyfile,potfile):
        "Create a POT File from a Python Script with gettext Strings"
        #TODO Exception Handling for Syntax Problems
        cmd = 'pygettext.exe --no-location -d {} "{}"'.format(potfile.replace(".pot",""),pyfile)
        system(cmd)

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

    def __addViaImport__(self,*event):
        pyFilePH = filedialog.askopenfilename(title="Python File",filetypes=(("Py-File","*.py *.pyw"),("All-Files","*.*")))
        if pyFilePH:
            potFilePH = path.join(tempfile.gettempdir(),"TmpPyInstall.pot")
            self.createTemplate(pyFilePH,potFilePH)
            try:
                for entry in polib.pofile(potFilePH):
                    if not self.msgs.find(entry.msgid):
                        self.msgs.append(entry)
                self.saved = False
            except:
                showerror(title="Failed to Import",message="The Syntax of the File is wrong or there is nothing to import.")
            remove(potFilePH)
            self.__refresh__()

    def __OnMouseWheel__(self,event):
        self.lstMsgId.yview("scroll", -int(event.delta/120),"units")
        self.lstMsgContent.yview("scroll",-int(event.delta/120),"units")
        return "break"


    def __createTemplate__(self,*event):
        
        pyFilePH = filedialog.askopenfilename(title="Python File",filetypes=(("Py-File","*.py *.pyw"),("All-Files","*.*")))
        if pyFilePH:
            potFilePH = filedialog.asksaveasfilename(title="Save POT",filetypes=(("POT File","*.pot"),),defaultextension=".pot")
            if potFilePH:
                self.createTemplate(pyFilePH,potFilePH)
                if askyesno(title="Open POT File",message="Do you want to open the created POT file?"):
                    self.openFile(potFilePH)
                    self.__refresh__()
  
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
            self.field.bind("<Shift-Return>",self.__okay__)
            self.field.bind("<Escape>",lambda x:self.destroy())
            self.field.bind("<Shift-Delete>",self.__delete__)
            self.field.insert(END,content)
            self.field.grid(columnspan=2,sticky=N+E+S+W)
            
            self.delete = Button(self,text="Delete",command=self.__delete__,state=NORMAL if id != "" else DISABLED)
            self.delete.grid(row=1,column=0,sticky=W+S)

            self.ok = Button(self,text="Okay",command=self.__okay__)
            self.ok.grid(row=1,column=1,sticky=E+S)
            self.after(1,lambda:self.field.focus_force())
            self.mainloop()


        def __okay__(self,*event):
            content = self.field.get(0.0,END)[:-1]
            if content != "":
                self.edit(self.id,content)
                self.master.__refresh__()
                self.destroy()

        def __delete__(self,*event):
            self.master.deleteItem(self.id)
            self.master.__refresh__()
            self.destroy()
    
    def __deleteMsgByContent__(self,*event):
        contid  = self.lstMsgContent.curselection()
        msgid   = self.lstMsgId.get(contid)
        self.deleteItem(msgid)
        self.saved = False
        self.__refresh__()

    def __deleteMsgByID__(self,*event):
        id   = self.lstMsgId.curselection()
        msgid   = self.lstMsgId.get(id)
        msgid = msgid if msgid != self.lstMsgId.get(END) else ""
        self.deleteItem(msgid)
        self.saved = False
        self.__refresh__()

    def __editMsgContent__(self,*event):
        contid  = self.lstMsgContent.curselection()
        msgid   = self.lstMsgId.get(contid)
        if msgid == self.lstMsgId.get(END):
            return
        self.ContetEdit(self,msgid,self.msgs.find(msgid).msgstr,self.editContent)
        
    def __editMsgID__(self,*event):
        id   = self.lstMsgId.curselection()
        msgid   = self.lstMsgId.get(id)
        msgid = msgid if msgid != self.lstMsgId.get(END) else ""
        self.ContetEdit(self,msgid,msgid,self.editID)


    def __refresh__(self,event=None,focus=True):
        self.filemenu.entryconfig(2,state=DISABLED if self.saved else NORMAL)
        self.filemenu.entryconfig(3,state=DISABLED if self.saved else NORMAL)
        self.filemenu.entryconfig(4,state=NORMAL if self.saved else DISABLED)
        
        oldidselect   = self.lstMsgId.curselection() or 0
        oldcontselect = self.lstMsgContent.curselection() or 0
        oldyview      = self.lstMsgId.yview()[0]

        self.lstMsgId.delete(0,END)
        self.lstMsgContent.delete(0,END)
        for msg in self.msgs:
            self.lstMsgId.insert(END,msg.msgid)
            self.lstMsgContent.insert(END,repr(msg.msgstr))
        self.lstMsgId.insert(END,"+".center(10))
        self.lstMsgContent.insert(END,"")

        self.lstMsgId.yview("moveto",oldyview)
        self.lstMsgContent.yview("moveto",oldyview)

        self.lstMsgId.select_set(oldidselect) if oldidselect else None
        self.lstMsgContent.select_set(oldcontselect) if oldcontselect else None

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


PyTranslate(args[0] if len(args) else None)
