import time
import threading
import random
import queue
import tkinter as tk
from runcycle.cycle import run_cycle, get_general_params
from tkinter.filedialog import *


class Application(tk.Frame):

    def __init__(self, thread,  master, queue, endCommand):
        self.thread = thread
        self.queue = queue
        self.endcommand = endCommand
        algoversion, algofolder, algorunoptimization, videospath, paramspath = get_general_params()
        self.optimize = IntVar()
        self.optimize.set(algorunoptimization)

        self.algofolder = StringVar()
        self.algofolder.set(algofolder)

        self.algoversion = StringVar()
        self.algoversion.set(algoversion)

        self.videofolder = StringVar()
        self.videofolder.set(videospath)

        self.paramsfilepath = StringVar()
        self.paramsfilepath.set(paramspath)

        # self.addparam = StringVar()
        tk.Frame.__init__(self, master)
        self.lblstatus = Label(self, text="Ready")
        # self.lbparams = tk.Listbox(self)
        self.lbreport = tk.Listbox(self, width=100)
        # self.lbparams.bind("<Double-Button-1>", self.OnDouble)
        # self.params = get_params_by_algo_version(algoversion)
        # self.get_params_into_listbox()
        self.grid()
        self.createWidgets()


    def createWidgets(self):


        # self.E1.insert(0,"1")

        # Algorithm Folder
        self.L1 = Label(self, text="Algorithm Folder").grid(row=0, column=0)
        self.E1 = Entry(self, bd =5, textvariable=self.algofolder, width=50).grid(row=0, column=1)
        self.getalgofolderbutton = tk.Button(self, text="Choose Folder",command=self.ChooseE1Folder).grid(row=0, column=2)

        # Algorithm Version
        self.L2 = Label(self, text="Algorithm Version").grid(row=1, column=0)
        self.E2 = Entry(self, bd =5, textvariable=self.algoversion, width=50).grid(row=1, column=1)
        self.getalgoversionbutton = tk.Button(self, text="Choose Folder",command=self.ChooseE2Folder).grid(row=1, column=2)

        # Video Folder
        self.L4 = Label(self, text="Video Folder").grid(row=2, sticky=W)
        self.E4 = Entry(self, bd =5, textvariable=self.videofolder, width=50).grid(row=2, column=1)
        self.getvideofolderbutton = tk.Button(self, text="Choose Folder",command=self.ChooseE4Folder).grid(row=2, column=2)

        # Video Folder
        self.L5 = Label(self, text="Params File").grid(row=3, sticky=W)
        self.E5 = Entry(self, bd =5, textvariable=self.paramsfilepath, width=50).grid(row=3, column=1)
        self.getparamsfilepathbutton = tk.Button(self, text="Choose File",command=self.ChooseE5Folder).grid(row=3, column=2)

        # self.L6 = Label(self, text="Name,Min,Max,Change,Default").grid(row=5, column=1)

        # # Add Update Remove Parameter
        # self.addupdateparambutton = tk.Button(self, text="Add or Update Parameter",command=self.add_update_param).grid(row=6, column=0)
        # self.removeparambutton = tk.Button(self, text="Remove Parameter",command=self.remove_param).grid(row=6, column=2)
        # self.addparamentry = Entry(self, bd =5, textvariable=self.addparam).grid(row=6, column=1)

        # Optimize radio button
        self.R1 = tk.Radiobutton(self, text="Optimize", variable=self.optimize, value=1).grid(row=5,column=0)
        self.R2 = tk.Radiobutton(self, text="Default", variable=self.optimize, value=0).grid(row=5,column=1)

        # Run Cycle Button
        self.runcyclebutton = tk.Button(self)
        self.runcyclebutton["text"] = "Run Cycle"
        self.runcyclebutton["command"] = self.runcyclethread
        self.runcyclebutton.grid(row=6,column=1)

        # Status Label
        self.lblstatus.grid(row=7, column=1)

        # # Parameter List
        # self.lbparams.grid(row=10,column=0)

        # Report List
        self.lbreport.grid(row=8,column=1)

    def runcyclethread(self):
         # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.lblstatus['text'] = "Running..."
        self.thread.running = 1
        self.thread.thread1 = threading.Thread(target=self.runcycle)
        self.thread.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.thread.periodicCall()

    def runcycle(self):
        run_cycle(self,str(self.optimize.get()),
                  str(self.algoversion.get()),
                  str(self.algofolder.get()),
                  str(self.videofolder.get()),
                  str(self.paramsfilepath.get()))
        self.lblstatus['text'] = "Ready"

        print("Finished running test!")

    def ChooseE1Folder(self):
        options = {}
        options['initialdir'] = 'C:\\'
        options['title'] = 'Please select the Algorithem Folder'
        folder = askdirectory(**options)
        self.algofolder.set(folder + '/')

    def ChooseE2Folder(self):
        options = {}
        if self.algofolder is not None:
            options['initialdir'] = self.algofolder.get()
        else:
            options['initialdir'] = 'C:\\'
        options['title'] = 'Please select the Algorithem Version Folder'
        folder = askdirectory(**options)
        self.algoversion.set(os.path.split(folder)[-1])

    def ChooseE4Folder(self):
        options = {}
        options['initialdir'] = 'C:\\'
        options['title'] = 'Please select the Video Folder'
        folder = askdirectory(**options)
        self.videofolder.set(folder + '/')

    def ChooseE5Folder(self):
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'permutations.txt'
        options['title'] = 'Please select the permutations file'
        filename = askopenfilename(**options)
        self.paramsfilepath.set(filename)

    # def get_params_into_listbox(self):
    #     for i in range(0, len(self.params)):
    #         self.lbparams.insert(str(i), str(self.params[i].name)
    #                                      + "," + str(self.params[i].min)
    #                                      + "," + str(self.params[i].max)
    #                                      + "," + str(self.params[i].change)
    #                                      + "," + str(self.params[i].default))
    #
    # def refresh_param_listbox(self):
    #     self.lbparams.delete(0, 10)
    #     self.get_params_into_listbox()
    #     self.addparam.set('')
    #
    # def add_update_param(self):
    #     #create param from user insert and append to list
    #     if str(self.addparam.get()) != '':
    #         list = self.addparam.get().split(',')
    #         p = Parameter(self.algoversion, str(list[0]),list[1],list[2],list[3],list[4])
    #         update = False
    #         for i in range(0, len(self.params)):
    #             if self.params[i].name == p.name:
    #                 self.params[i].min = p.min
    #                 self.params[i].max = p.max
    #                 self.params[i].change = p.change
    #                 self.params[i].default = p.default
    #                 update = True
    #         if not update:
    #             self.params.append(p)
    #         self.refresh_param_listbox()
    #
    # def remove_param(self):
    #     if str(self.addparam.get()) != '':
    #         list = self.addparam.get().split(',')
    #         p = Parameter(self.algoversion, str(list[0]),list[1],list[2],list[3],list[4])
    #         for i in range(0, len(self.params)):
    #             if self.params[i].name == p.name:
    #                 p = self.params[i]
    #         self.params.remove(p)
    #         self.refresh_param_listbox()

    def OnDouble(self, event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        self.addparam.set(value)

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                print(msg)
            except queue.Empty:
                pass


class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = Application(self, master, self.queue, self.endApplication)

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            time.sleep(rand.random() * 0.3)
            msg = rand.random()
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0

rand = random.Random()
app = tk.Tk()

client = ThreadedClient(app)
app.mainloop()