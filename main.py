import tkinter
import os
import tkinter.filedialog
import xlrd
from xlutils.copy import copy
from tkinter import *

coeff = -1  #Intermediate variables for the input parameters
str = ""


# Function for toggle_button 
def toggle(show, toggle_button, Label_self):
    if bool(show.get()):
        Label_self.pack()
    else:
        Label_self.forget()


#Display a prompt box to allow the user to select the file to be used
#Intermediate variables for the input parameters
def direc():
    default_dir = r"path"
    fname = tkinter.filedialog.askopenfilename(title=u'select the file',
                                               initialdir=(os.path.expanduser(
                                                   (default_dir))))
    desktop_path = ''
    oldWb = xlrd.open_workbook(fname, formatting_info=True)
    oldWbS = oldWb.sheet_by_index(0)
    newWb = copy(oldWb)
    newWs = newWb.get_sheet(0)
    step = 0

    #transfer dummy variables to normal variables and save in a new excel file
    for colindex in range(0, oldWbS.ncols):
        if (type(oldWbS.cell(1, colindex).value) == type("a")):
            setname = set()
            for rowIndex in range(1, oldWbS.nrows):
                setname.add(oldWbS.cell(rowIndex, colindex).value)
            size = len(setname)
            li_setname = list(setname)
            for i in range(0, size):
                newWs.write(0, colindex + i, li_setname[i])
                for j in range(1, oldWbS.nrows):
                    if oldWbS.cell(j, colindex).value == li_setname[i]:
                        newWs.write(j, step + i, 1)
                    else:
                        newWs.write(j, step + i, 0)
            step = step + size
        else:
            for rowIndex in range(0, oldWbS.nrows):
                newWs.write(rowIndex, step,
                            oldWbS.cell(rowIndex, colindex).value)
            step = step + 1

    newWb.save('fileName.xls')
    file = open("pth.txt", 'w')
    file.write("fileName.xls")
    file.close()


#Save the inputted importance of size and store it in the file para.txt
def savecoeff():
    coeff = entry.get()
    button4["text"] = "inputed"
    doc = open('para.txt', 'w')
    print(coeff, file=doc)
    doc.close()


#Save the inputted number of generations and store it in the file NOG.txt
def save_NOG():
    coeff = entry_NOG.get()
    button_NOG["text"] = "inputed"
    doc = open('NOG.txt', 'w')
    print(coeff, file=doc)
    doc.close()


#Save the inputted number of individuals in initial population and store it in the file num_in_gen.txt
def save_num_in_gen():
    print("!!!!!!!!!!!!!!")
    coeff = entry_num_in_gen.get()
    button_num_in_gen["text"] = "inputed"
    doc = open('num_in_gen.txt', 'w')
    print(coeff, file=doc)
    doc.close()
    print("num_in_gen")
    print(coeff)


#Save the inputted possibility of crossover and store it in the file cxbp.txt
def save_cxpb():
    coeff = entry_cxpb.get()
    button_cxpb["text"] = "inputed"
    doc = open('cxbp.txt', 'w')
    print(coeff, file=doc)
    doc.close()
    print("cxbp")
    print(coeff)


#Save the inputted possibility of mutation and store it in the file mutpb.txt
def save_mutpb():
    coeff = entry_mutpb.get()
    button_mutpb["text"] = "inputed"
    doc = open('mutpb.txt', 'w')
    print(coeff, file=doc)
    doc.close()
    print("mutpb")
    print(coeff)


#Create a new window for entering submodels
def addsub():
    window2 = tkinter.Toplevel(window)
    Info_add = tkinter.Label(
        master=window2,
        text="To add some for submodel that might be in the final result\n"
        "For example: (x1+x2)^2+sin(x3)*exp(x5)\n"
        "support sin,cos,tan,+,-,*,/,exp,sqrt\n"
        "exp(x) means e^(x)\n"
        "** as power"
        "each formular per line",
    )
    Info_add.pack()
    text_sub = tkinter.Text(master=window2)

    def close_h():
        str = text_sub.get("1.0", tkinter.END)
        doc = open('Text.txt', 'w')
        print(str, file=doc)
        doc.close()
        window2.destroy()

    text_sub.pack()
    button_fin = tkinter.Button(
        master=window2,
        text="finish",
        # width=25,
        # height=1,
        bg="grey",
        fg="yellow",
        command=close_h)
    button_fin.pack()


#Call the main program symbolic_regression_backend.py and print the output formular and fitness
def solv():
    str = ('python symbolic_regression_backend.py')
    doc = open("mod.txt", "w")
    print("1", file=doc)
    doc.close()
    p = os.system(str)
    doc = open('tmp.txt', 'r')
    ss = doc.read()
    doc.close()
    formu = ""
    fit = ""
    fit2 = ""
    step = 0
    lenss = len(ss)

    while (step <= len(ss) - 1 and ss[step] != '\n'):
        formu = formu + ss[step]
        step = step + 1
    while (step <= lenss - 1 and (ss[step] > '9' or ss[step] < '0')):
        step = step + 1
    while (step <= lenss - 1 and (ss[step] != '\n')):
        fit = fit + ss[step]
        step = step + 1
    while (step <= len(ss) - 1 and (ss[step] > '9' or ss[step] < '0')):
        step = step + 1
    while (step <= len(ss) - 1 and (ss[step] != '\n')):
        fit2 = fit2 + ss[step]
        step = step + 1

    moresult = tkinter.Label(master=frame1,
                             text="Symbolic Regression_Result",
                             background="black",
                             fg="white")

    # Output formula
    formula = tkinter.Label(master=frame1,
                            text="Formular \n" + formu,
                            background="black",
                            fg="white")

    # Output fitness
    fitness = tkinter.Label(master=frame1,
                            text="RMSE \n" + fit,
                            background="black",
                            fg="white")

    # Output multiobjective fitness
    fitness2 = tkinter.Label(master=frame1,
                             text="Multifitness \n" + fit2,
                             background="black",
                             fg="white")
    formula.place(x=10, y=40)
    fitness.place(x=10, y=100)
    fitness2.place(x=200, y=100)


def solv2():
    str = ('python symbolic_regression_backend.py')
    doc = open("mod.txt", "w")
    print("2", file=doc)
    doc.close()
    p = os.system(str)
    doc = open('tmp.txt', 'r')
    ss = doc.read()
    doc.close()
    formu = ""
    fit = ""
    fit2 = ""
    step = 0
    lenss = len(ss)

    while (step <= len(ss) - 1 and ss[step] != '\n'):
        formu = formu + ss[step]
        step = step + 1
    while (step <= lenss - 1 and (ss[step] > '9' or ss[step] < '0')):
        step = step + 1
    while (step <= lenss - 1 and (ss[step] != '\n')):
        fit = fit + ss[step]
        step = step + 1
    while (step <= len(ss) - 1 and (ss[step] > '9' or ss[step] < '0')):
        step = step + 1
    while (step <= len(ss) - 1 and (ss[step] != '\n')):
        fit2 = fit2 + ss[step]
        step = step + 1

    moresult = tkinter.Label(master=frame1,
                             text="Symbolic Regression_Result",
                             background="black",
                             fg="white")

    # Output formula
    formula = tkinter.Label(master=frame1,
                            text="Formular \n" + formu,
                            background="black",
                            fg="white")

    # Output fitness
    fitness = tkinter.Label(master=frame1,
                            text="MSE \n" + fit,
                            background="black",
                            fg="white")

    # Output multiobjective fitness
    fitness2 = tkinter.Label(master=frame1,
                             text="Multifitness \n" + fit2,
                             background="black",
                             fg="white")
    formula.place(x=10, y=40)
    fitness.place(x=10, y=100)
    fitness2.place(x=200, y=100)


#main function
if __name__ == '__main__':

    # Instantiating class
    window = Tk()

    #Contruct two frame widgets
    frame1 = tkinter.Frame(master=window, bg="red", width=1400, height=150)
    frame2 = tkinter.Frame(master=window, bg="blue", width=1400, height=200)

    #Label widgets for welcome message and parameters
    greeting = tkinter.Label(master=frame2,
                             text="Symbolic Regression",
                             background="black",
                             fg="white")
    Imp = tkinter.Label(master=frame2,
                        text="Importance of Formula Length",
                        foreground="white",
                        background="black")
    num_in_gen = tkinter.Label(master=frame2,
                               text="Population size",
                               foreground="white",
                               background="black")
    Num_of_gen = tkinter.Label(master=frame2,
                               text="Number of generations",
                               foreground="white",
                               background="black")
    mutpb = tkinter.Label(master=frame2,
                          text="posibility of  mutation",
                          foreground="white",
                          background="black")
    moresult = tkinter.Label(master=frame1,
                             text="Symbolic Regression_Result",
                             background="black",
                             fg="white")
    CXPB = tkinter.Label(master=frame2,
                         text="posibility of crossover",
                         foreground="white",
                         background="black")

    # Entry widgets for each inputted parameters
    entry_NOG = tkinter.Entry(master=frame2)
    entry = tkinter.Entry(master=frame2)
    entry_mutpb = tkinter.Entry(master=frame2)
    entry_cxpb = tkinter.Entry(master=frame2)
    entry_num_in_gen = tkinter.Entry(master=frame2)

    # Button widgets for running programs, adding submodels, and loading data
    button1 = tkinter.Button(
        master=frame2,
        text="Load data",
        #width=25,
        #height=1,
        bg="grey",
        fg="yellow",
        command=direc)
    button2 = tkinter.Button(
        master=frame2,
        text="Add Submodels",
        # width=25,
        # height=1,
        bg="grey",
        fg="yellow",
        command=addsub)
    button3 = tkinter.Button(
        master=frame2,
        text="Calculate Model(RMSE)",
        # width=25,
        # height=1,
        bg="grey",
        fg="yellow",
        command=solv)
    button_MSE = tkinter.Button(
        master=frame2,
        text="Calculate Model(MSE)",
        # width=25,
        # height=1,
        bg="grey",
        fg="yellow",
        command=solv2)

    #Buttons to confirm that information has been entered(In GUI: the "->" symbol after parameters)
    button4 = tkinter.Button(
        master=frame2,
        text="\N{RIGHTWARDS BLACK ARROW}",
        #width=2,
        #height=1,
        bg="grey",
        fg="yellow",
        command=savecoeff)
    button_NOG = tkinter.Button(
        master=frame2,
        text="\N{RIGHTWARDS BLACK ARROW}",
        # width=25,
        # height=1,
        bg="grey",
        fg="yellow",
        command=save_NOG)
    button_num_in_gen = tkinter.Button(
        master=frame2,
        text="\N{RIGHTWARDS BLACK ARROW}",
        # width=25,
        # height=1,
        bg="grey",
        fg="yellow",
        command=save_num_in_gen)
    button_cxpb = tkinter.Button(
        master=frame2,
        text="\N{RIGHTWARDS BLACK ARROW}",
        # width=25,
        # height=1,
        bg="grey",
        fg="yellow",
        command=save_cxpb)
    button_mutpb = tkinter.Button(
        master=frame2,
        text="\N{RIGHTWARDS BLACK ARROW}",
        # width=25,
        # height=1,
        bg="grey",
        fg="yellow",
        command=save_mutpb)

    # Label widgets info box of each parameters
    Info_lenth = tkinter.Label(master=frame2,
                               text="0 means the size of result has not \n"
                               "consider as an influence factor\n"
                               "bigger the number is, more important\n"
                               "role plays the size,usually in range of\n"
                               "[0,0.1*means of dependent variable]",
                               foreground="white",
                               background="black")
    Info_generation = tkinter.Label(
        master=frame2,
        text="with more generation is more likely  \n"
        "to get better result but will \n"
        "take more time by default is 40\n"
        "generations(takes about 10 minutes)",
        foreground="white",
        background="black")
    Info_cxpb = tkinter.Label(
        master=frame2,
        text=
        "The probability of mating two individuals and mutating an individual\n"
        "in genetic programming algorithm by default is 0.5 and 0.2\n"
        "usually respectively in range of [0.5,1] and [0.001,0.2]\n"
        "with the increasing of the number, diversity would be increased\n"
        "Stability would be reduced",
        foreground="white",
        background="black")
    Info_loadin = tkinter.Label(master=frame2,
                                text="File must be transfered to  .xlsx\n"
                                "the name of the sheet need to\n be 'Sheet1'",
                                foreground="white",
                                background="black")
    Info_mut = tkinter.Label(master=frame2,
                             text="The probability of muation.\n"
                             "in genetic programming algorithm\n"
                             "usually in range of [0.001,0.2]"
                             "by default is 0.1",
                             foreground="white",
                             background="black")
    Info_num_in_gen = tkinter.Label(master=frame2,
                                    text="size of generation in algorithm.\n"
                                    "larger size means more Diversity\n"
                                    "and takes more time"
                                    "by default is 100",
                                    foreground="white",
                                    background="black")

    #Make the contents of the info box collapsible
    var_lenth = tkinter.IntVar()

    def check_lenth():
        if (var_lenth.get() == 1):
            Info_lenth.place(x=280, y=90)
        else:
            Info_lenth.place_forget()

    len_btn = tkinter.Checkbutton(master=frame2,
                                  text="info?",
                                  variable=var_lenth,
                                  command=check_lenth,
                                  onvalue=1,
                                  offvalue=0)
    var_num_in_gen = tkinter.IntVar()

    def check_num_in_gen():
        if (var_num_in_gen.get() == 1):
            Info_num_in_gen.place(x=1150, y=90)
        else:
            Info_num_in_gen.place_forget()

    num_in_gen_btn = tkinter.Checkbutton(master=frame2,
                                         text="info?",
                                         variable=var_num_in_gen,
                                         command=check_num_in_gen,
                                         onvalue=1,
                                         offvalue=0)
    var_gen = tkinter.IntVar()

    def check_gen():
        if (var_gen.get() == 1):
            Info_generation.place(x=510, y=90)
        else:
            Info_generation.place_forget()

    gen_btn = tkinter.Checkbutton(master=frame2,
                                  text="info?",
                                  variable=var_gen,
                                  command=check_gen,
                                  onvalue=1,
                                  offvalue=0)
    var_cxpb = tkinter.IntVar()

    def check_cxpb():
        if (var_cxpb.get() == 1):
            Info_cxpb.place(x=740, y=90)
        else:
            Info_cxpb.place_forget()

    cxpb_btn = tkinter.Checkbutton(master=frame2,
                                   text="info?",
                                   variable=var_cxpb,
                                   command=check_cxpb,
                                   onvalue=1,
                                   offvalue=0)
    var_loadin = tkinter.IntVar()

    def check_loadin():
        if (var_loadin.get() == 1):
            Info_loadin.place(x=100, y=90)
        else:
            Info_loadin.place_forget()

    loadin_btn = tkinter.Checkbutton(master=frame2,
                                     text="info?",
                                     variable=var_loadin,
                                     command=check_loadin,
                                     onvalue=1,
                                     offvalue=0)

    #Location of widgets
    frame2.pack()
    frame1.pack()
    num_in_gen_btn.place(x=1150, y=5)
    len_btn.place(x=300, y=5)
    gen_btn.place(x=510, y=5)
    cxpb_btn.place(x=740, y=5)
    loadin_btn.place(x=90, y=60)
    greeting.place(x=10, y=10)
    button1.place(x=15, y=60)
    button2.place(x=150, y=60)
    Imp.place(x=300, y=30)
    entry.place(x=300, y=60)
    Num_of_gen.place(x=510, y=30)
    entry_NOG.place(x=510, y=60)
    CXPB.place(x=740, y=30)
    entry_cxpb.place(x=740, y=60)
    mutpb.place(x=930, y=30)
    entry_mutpb.place(x=930, y=60)
    button3.place(x=150, y=20)
    button4.place(x=450, y=60)
    button_MSE.place(x=150, y=100)
    button_NOG.place(x=660, y=60)
    button_cxpb.place(x=880, y=60)
    button_num_in_gen.place(x=1295, y=60)
    entry_num_in_gen.place(x=1150, y=60)
    button_mutpb.place(x=1080, y=60)
    moresult.place(x=10, y=10)
    num_in_gen.place(x=1150, y=30)

    #Call the mainloop of TK
    window.mainloop()
