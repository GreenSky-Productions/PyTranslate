from os import sys,system,remove,replace
from tkinter import *
import getopt
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter.ttk import *
from shutil import copyfile

class PyFileImport(Tk):

    def __init__(self,file=None):
        Tk.__init__(self)
        self.title("PY Translater")
        self.geometry("1000x600")
        self.ofile = file
        self.msgid = 0
        self.msgs = {}
        self.content = []
        self.createContent()
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0,weight=1)
        self.openPot(file) if file else None
        
    def createPot(self,readfile,saveFile):
        system('pygettext.exe --no-location -d {} "{}"'.format(saveFile.replace(".pot",""),readfile))
        
    def openFile(self,file):
        self.msgs.clear()

        first = True
        with open(file,"r") as _file:
            for line in _file:
                if "msgid" in line:
                    if first:
                        first = False
                        continue
                    nline = next(_file)
                    id = line.split('"')[1]
                    content = nline.split('"')[1]
                    self.msgs[id] = content
            _file.close()

        self.ofile = file
        self.title("Py Tranlater '{}'".format(self.ofile))
        self.filemenu.entryconfig(2,state=NORMAL)
        self.filemenu.entryconfig(3,state=NORMAL)
        self.filemenu.entryconfig(4,state=NORMAL)
        self.load()

    def __openFile__(self,event=None):
        readFile = filedialog.askopenfilename(title="Open POT or PO File",filetypes=(("Translation Files","*.pot *.po"),))
        if readFile:
            self.openPot(readFile)
        self.load()


    def isClosed(self,event=None):
        askyesnocancel()

    def closeFile(self):
        self.ofile = None
        self.title("Py Tranlater".format(self.ofile))

    def __createPotFile__(self,event=None):
        readFile = filedialog.askopenfilename(title="Python File",filetypes=(("Py-File","*.py *.pyw"),))
        saveFile = filedialog.asksaveasfilename(title="Save POT",filetypes=(("POT File","*.pot"),))
        if readFile and saveFile:
            self.createPot(readFile,saveFile)
            if askyesno(title="Open POT File",message="Do you want to open the created POT file?"):
                self.openPot(saveFile)
            else:
                showinfo(title="Finished",message="The POT File is successfully created.")


        #C:\Users\p.seelk\Source\Repos\SPSettings\SPSettings

    def __saveAsPoFile__(self,event=None):
        filepath = filedialog.asksaveasfilename(title="Save Po",filetypes=(("Translation File","*.po"),),defaultextension=".po")
        if filepath:
            self.writeNewPo(filepath)
            self.title("Py Translate '{}'".format(self.ofile))

    def saveFile(self,event=None):
        if self.ofile:
            self.writeNewPo(self.ofile)
            self.title("Py Translate '{}'".format(self.ofile))

    def getNewMsgContent(self):
        content = self.window.field.get(0.0,END)[:-1]
        if content != self.msgs[self.msgid]:
            self.title("Py Translate *'{}'".format(self.ofile))
        self.msgs[self.msgid] = content
        self.window.destroy()
        print(content)
        self.load()

    def changeMsgContent(self,event=None):
        curind     = self.lstMsgContent.curselection()
        msgcont    = self.lstMsgContent.get(curind)[1:-1]
        self.msgid = self.lstMsgId.get(curind)

        self.window = Toplevel(self)
        self.window.title(self.msgid)
        self.window.columnconfigure(0,weight=1)
        self.window.rowconfigure(1,weight=1)
        self.window.attributes("-tool",1)
        self.window.field = Text(self.window)
        self.window.field.insert(END,msgcont)
        self.window.field.grid(sticky=N+E+S+W)
        self.window.ok = Button(self.window,text="Okay",command=self.getNewMsgContent)
        self.window.ok.grid(sticky=E+S)
        self.window.after(200,self.window.field.focus_set)
        self.window.mainloop()
      
    def poToMo(self,file):
        self.writeNewPo("tmp.po")
        system('msgfmt.exe tmp')
        replace("tmp.mo",filepath)
        remove("tmp.po")

    def readHeader(self):
        with open(self.ofile,"r") as file:
            header = "".join(next(file) for x in range(15))
            file.close()
        return header

    def writeNewPo(self,file):
        header = self.readHeader()
        with open(file,"w") as file:
            file.write(header)
            content = ""
            for k,v in self.msgs.items():
                file.write("""
msgid "{}"
msgstr "{}"
""".format(k,v))
            file.close()

    def export(self,event=None):
        filepath = filedialog.asksaveasfilename(title="Export as MO",filetypes=(("Compiled Translation File","*.mo"),),defaultextension=".mo")
        if filepath:
            self.poToMo(filepath)
            
    def createContent(self):
        self.menu = Menu(tearoff=0)
        self.filemenu = Menu(tearoff=0)

        self.filemenu.add_command(label="Create new POT File",command=self.newPotFile,accelerator="Ctrl+N")
        self.bind("<Control-n>",self.newPotFile)
        self.filemenu.add_command(label="Open",command=self.openPotFile,accelerator="Ctrl+O")
        self.bind("<Control-o>",self.openPotFile)
        self.filemenu.add_command(label="Save",command=self.savePoFile,accelerator="Ctrl+S",state=DISABLED)
        self.bind("<Control-s>",self.savePoFile)
        self.filemenu.add_command(label="Save as",command=self.saveAsPoFile,accelerator="Shift+Ctrl+S",state=DISABLED)
        self.bind("<Control-S>",self.saveAsPoFile)
        self.filemenu.add_command(label="Export",command=self.export,accelerator="Ctrl+E",state=DISABLED)
        self.bind("<Control-e>",self.export)
        self.filemenu.add_command(label="Close",command=self.destroy,accelerator="Ctrl+Q",state=DISABLED)
        self.bind("<Control-q>",self.destroy)
        self.menu.add_cascade(label="File",menu=self.filemenu)
        #filemenu.add_command(label="Open POT")

        self.configure(menu=self.menu)

        self.lstmsgpan = Panedwindow(self,orient=HORIZONTAL)
        self.lstmsgpan.grid(row=0,column=0,sticky=N+W+E+S,columnspan=2)
        self.lstMsgId = Listbox(self.lstmsgpan)
        self.lstmsgpan.add(self.lstMsgId)#self.lstMsgId.grid(row=0,column=0,sticky=N+W+E+S)

        self.lstMsgContent = Listbox(self.lstmsgpan)
        self.lstMsgContent.bind("<Double-Button-1>",self.changeMsgContent)
        self.lstmsgpan.add(self.lstMsgContent)#.grid(row=0,column=1,sticky=N+E+S+W)

        #self.loadBtn = Button(self,text="Load",command=self.loadfile)
        #self.loadBtn.grid(padx=5,pady=5,row=1,column=0,sticky=W+S)

        #self.expBtn = Button(self,text="Export",command=self.export)
        #self.expBtn.grid(padx=5,pady=5,row=1,column=1,sticky=E+S)

    def load(self):
        self.lstMsgId.delete(0,END)
        #for wid in self.lstMsgContent.winfo_children():
            #wid.destroy()
        self.lstMsgContent.delete(0,END)
        for msgid in self.msgs.keys():
            self.lstMsgId.insert(END,msgid)
            self.lstMsgContent.insert(END,repr(self.msgs[msgid]))
            #ent = Entry(self.lstMsgContent,style="T.TEntry")
            #ent.insert(END,self.msgs[msgid])
            #ent.grid(sticky=N+E+W)
            #self.content.append(ent)
            #self.lstMsgContent.add(ent)
            #self.lstMsgContent.insert(END,Entry())


paras =sys.argv[1:]
#paras = ["potpo","C:\\Users\\p.seelk\\Desktop\\test.pot","C:\\Users\\p.seelk\\Desktop\\ausgabe.po"]
#paras = ["editpo","C:\\Users\\p.seelk\\Desktop\\ausgabe.po",'world="Welt"']
if paras:
    if paras[0] == "potpo" and len(paras) >= 3:
        pfi = PyFileImport()
        pfi.openPot(paras[1])
        pfi.writeNewPo(paras[2])
    elif paras[0] == "pomo" and len(paras) >= 3:
        pfi = PyFileImport()
        pfi.poToMo(paras[2])

    elif paras[0] == "editpo" and len(paras) >= 3:
        pfi = PyFileImport()
        pfi.openPot(paras[1])
        print(pfi.ofile)
        for para in paras[2:]:
            msgid,msg = para.split("=")
            pfi.msgs[msgid] = msg.replace('"',"")
            print("Set",msgid,"to",msg)
        pfi.savePoFile()
    else:
        print("No")
else:
    PyFileImport().mainloop()

