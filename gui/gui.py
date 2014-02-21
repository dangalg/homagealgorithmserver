# Synchronous App
# from logic.logic_services.parameter_logic import get_all_params
# from models.parameter import Parameter
# from runcycle.cycle import run_cycle, get_general_params
#
# from tkinter import *
# __author__ = 'danga_000'
#
# import tkinter as tk
#
# class Application(tk.Frame):
#     def get_params_into_listbox(self):
#         for i in range(0, len(self.params)):
#             self.lbparams.insert(str(i), str(self.params[i].name)
#                                          + "," + str(self.params[i].min)
#                                          + "," + str(self.params[i].max)
#                                          + "," + str(self.params[i].change)
#                                          + "," + str(self.params[i].default))
#
#     def __init__(self, master=None):
#         algooutput, algoversion, algorunoptimization, videospath = get_general_params()
#         self.optimize = IntVar()
#         self.optimize.set(algorunoptimization)
#         self.algoversion = StringVar()
#         self.algoversion.set(algoversion)
#         self.algooutputfolder = StringVar()
#         self.algooutputfolder.set(algooutput)
#         self.videofolder = StringVar()
#         self.videofolder.set(videospath)
#         self.addparam = StringVar()
#         tk.Frame.__init__(self, master)
#         self.lblstatus = Label(self, text="Ready")
#         self.lbparams = tk.Listbox(self)
#         self.lbparams.bind("<Double-Button-1>", self.OnDouble)
#         self.params = get_all_params()
#         self.get_params_into_listbox()
#         self.grid()
#         self.createWidgets()
#
#
#     def createWidgets(self):
#         # Algorithm Version
#         self.L1 = Label(self, text="Algorithm Version").grid(row=0, sticky=W)
#         self.E1 = Entry(self, bd =5, textvariable=self.algoversion).grid(row=0, column=1)
#         # self.E1.insert(0,"1")
#
#         # Algorithm Output Folder
#         self.L2 = Label(self, text="Algorithm Output Folder").grid(row=1, sticky=W)
#         self.E2 = Entry(self, bd =5, textvariable=self.algooutputfolder).grid(row=1, column=1)
#
#         # Video Folder
#         self.L3 = Label(self, text="Video Folder").grid(row=2, sticky=W)
#         self.E3 = Entry(self, bd =5, textvariable=self.videofolder).grid(row=2, column=1)
#
#         # Add Update Remove Parameter
#         self.addupdateparambutton = tk.Button(self, text="Add or Update Parameter",command=self.add_update_param).grid(row=3, column=0)
#         self.removeparambutton = tk.Button(self, text="Remove Parameter",command=self.remove_param).grid(row=3, column=2)
#         self.addparamentry = Entry(self, bd =5, textvariable=self.addparam).grid(row=3, column=1)
#
#         # Optimize radio button
#         self.R1 = tk.Radiobutton(self, text="Optimize", variable=self.optimize, value=1).grid(row=4,column=0)
#         self.R2 = tk.Radiobutton(self, text="Default", variable=self.optimize, value=0).grid(row=4,column=1)
#
#         # Run Cycle Button
#         self.runcyclebutton = tk.Button(self)
#         self.runcyclebutton["text"] = "Run Cycle"
#         self.runcyclebutton["command"] = self.runcycle
#         self.runcyclebutton.grid(row=5,column=0)
#
#         # Parameter List
#         self.lbparams.grid(row=6,column=0)
#
#         # Status Label
#         self.lblstatus.grid(row=6, column=1)
#
#     def runcycle(self):
#         run_cycle(str(self.optimize.get()),
#                   str(self.algoversion.get()),
#                   str(self.algooutputfolder.get()),
#                   str(self.videofolder.get()),
#                   self.params)
#         self.lblstatus['text'] = "Finished Test"
#         print("Finished running test!")
#
#     def refresh_param_listbox(self):
#         self.lbparams.delete(0, 10)
#         self.get_params_into_listbox()
#         self.addparam.set('')
#
#     def add_update_param(self):
#         #create param from user insert and append to list
#         if str(self.addparam.get()) != '':
#             list = self.addparam.get().split(',')
#             p = Parameter(str(list[0]),list[1],list[2],list[3],list[4])
#             update = False
#             for i in range(0, len(self.params)):
#                 if self.params[i].name == p.name:
#                     self.params[i].min = p.min
#                     self.params[i].max = p.max
#                     self.params[i].change = p.change
#                     self.params[i].default = p.default
#                     update = True
#             if not update:
#                 self.params.append(p)
#             self.refresh_param_listbox()
#
#     def remove_param(self):
#         if str(self.addparam.get()) != '':
#             list = self.addparam.get().split(',')
#             p = Parameter(str(list[0]),list[1],list[2],list[3],list[4])
#             for i in range(0, len(self.params)):
#                 if self.params[i].name == p.name:
#                     p = self.params[i]
#             self.params.remove(p)
#             self.refresh_param_listbox()
#
#     def OnDouble(self, event):
#         widget = event.widget
#         selection=widget.curselection()
#         value = widget.get(selection[0])
#         self.addparam.set(value)
#
# app = Application(master=tk.Tk())
# app.mainloop()