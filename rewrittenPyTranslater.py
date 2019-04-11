from os import sys,system,remove,replace
import getopt
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
        self.msgs  = {}
        
        self.GUI = GUI
        Tk.__init__(self)
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
        self.filemenu.add_command(label="Save",command=NotImplementedError,accelerator="Ctrl+S",state=DISABLED)
        self.filemenu.add_command(label="Save as",command=NotImplementedError,accelerator="Shift+Ctrl+S",state=DISABLED)
        self.filemenu.add_command(label="Export",command=NotImplementedError,accelerator="Ctrl+E",state=DISABLED)
        self.filemenu.add_command(label="Close",command=self.destroy,accelerator="Ctrl+Q",state=DISABLED)
        self.bind("<Control-n>",NotImplementedError)
        self.bind("<Control-o>",NotImplementedError)
        self.bind("<Control-s>",NotImplementedError)
        self.bind("<Control-S>",NotImplementedError)
        self.bind("<Control-e>",NotImplementedError)
        self.bind("<Control-q>",self.destroy)

        self.menu.add_cascade(label="File",menu=self.filemenu)
        self.configure(menu=self.menu)

        self.lstmsgpan = Panedwindow(self,orient=HORIZONTAL)
        self.lstmsgpan.grid(row=0,column=0,sticky=N+W+E+S,columnspan=2)
        self.lstMsgId = Listbox(self.lstmsgpan)
        self.lstmsgpan.add(self.lstMsgId)#self.lstMsgId.grid(row=0,column=0,sticky=N+W+E+S)

        self.lstMsgContent = Listbox(self.lstmsgpan)
        self.lstMsgContent.bind("<Double-Button-1>",self.__editMsgContent__)
        self.lstmsgpan.add(self.lstMsgContent)#.grid(row=0,column=1,sticky=N+E+S+W)
    
    def createTemplate(self,pyfile,potfile):
        "Create a POT File from a Python Script with gettext Strings"
        system('pygettext.exe --no-location -d {} "{}"'.format(potfile.replace(".pot",""),pyfile))

    def __createTemplate__(self,*event):
        pyFilePH = filedialog.askopenfilename(title="Python File",filetypes=(("Py-File","*.py *.pyw"),))
        if pyFilePH:
            potFilePH = filedialog.asksaveasfilename(title="Save POT",filetypes=(("POT File","*.pot"),),defaultextension=".pot")
            if potFilePH:
                self.createTemplate(pyFilePH,potFilePH)
                if askyesno(title="Open POT File",message="Do you want to open the created POT file?"):
                    self.openFile(potFilePH)
                    self.__refresh__()
        "For IDE, cause VS is stupid"

    def openFile(self,filepath):
        self.msgs.clear()
        with open(filepath,"r") as file:
            self.oheader = "".join(next(file) for x in range(15))
            for line in file:
                
                if "msgid" in line:
                    nline = next(file)
                    id = line.split('"')[1]
                    if id != "":
                        content = nline.split('"')[1]
                        self.msgs[id] = content
            file.close()

        if self.oheader.strip() == "":
            warning(title="Corrupted File!",message="The file cannot be opened because it has a corrupted header.")
        else:
            self.ofile = filepath
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


    def save(self,file):
        with open(file,"r") as file:
            header = "".join(next(file) for x in range(15))
            file.close()
        with open(file,"w") as file:
            file.write(header)
            content = ""
            for k,v in self.msgs.items():
                file.write("""
msgid "{}"
msgstr "{}"
""".format(k,v))
            file.close()

    def __save__(self,*event):
        if not self.saved:
            self.save(self.ofile)
    def __saveAs__(self,*event):
        if not self.saved:
            pass
    def export(self,file):
        pass

    def __export__(self,*event):
        pass

    def editContent(self,msgid,msg):
        self.saved = False
        self.msgs[msgid] = msg
        print("changed",msgid,"to",msg)
          
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
            self.field.grid(sticky=N+E+S+W)

            self.ok = Button(self,text="Okay",command=self.__okay__)
            self.ok.grid(sticky=E+S)
            self.mainloop()

        def __okay__(self):
            self.edit(self.id,self.field.get(0.0,END)[:-1])
            self.master.__refresh__()
            self.destroy()

    

    def __editMsgContent__(self,*event):
        contid  = self.lstMsgContent.curselection()
        msgid   = self.lstMsgId.get(contid)
        
        self.ContetEdit(self,msgid,self.msgs[msgid],self.editContent)
        

    def __refresh__(self,*event):
        self.lstMsgId.delete(0,END)
        self.lstMsgContent.delete(0,END)
        for msgid in self.msgs.keys():
            self.lstMsgId.insert(END,msgid)
            self.lstMsgContent.insert(END,repr(self.msgs[msgid]))

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