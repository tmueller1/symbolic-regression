import numpy
import random2
import operator
import math
import xlrd
from pythonds.basic.stack import Stack
from sympy import simplify, cos, sin, sqrt, exp, symbols
from deap import algorithms, base, creator, tools, gp

MAX = 1000000000  #When an undefined value appears in the calculation, assign this constant to the individual as fitness
train_par = 1.0  #Proportion of training set
Num_of_generation = 40  #number of generations, default is 40
lensheet = -1  #number of samples
widthsheet = -1  #number of varialbes (including the dependent variable)
Num = 1
Num_sub = 0  #number of submodels
Titel = []  #Arrays for storing variable names
namda2 = 0.01  #Value to indicate importance of size, default value is 0.01
mod = -1
doc = open('mod.txt', 'r')
sstr = doc.read()
doc.close()
sstr = sstr.strip('\n')
if (sstr == "1"):
    mod = 1
else:
    mod = 2
doc = open('para.txt', 'r')
sss = doc.read()
doc.close()
if (len(sss) > 1):
    namda2 = float(sss)
tag = [0 for i in range(605)
      ]  #was used to randomly select samples for the training set


# Define protected version of division and square root 
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1


def protectedsqrt(hh):
    if (hh < 0):
        return MAX
    else:
        return math.sqrt(hh)


# Input the submodels and save them in variable "new_Submodel"
Submodel = []
doc = open("Text.txt", 'r', encoding='gbk')
line = doc.readline()
while line:
    Submodel.append(line),
    line = doc.readline()
doc.close()


def not_empty(s):
    return s and s.strip()


global new_Submodel
tmp = list(filter(not_empty, Submodel))
new_Submodel = tmp
print(len(new_Submodel))

# Get the number of samples("lensheet") and the number of variables("widthsheet")
ss = "fileName.xls"
book = xlrd.open_workbook(filename=ss, formatting_info=True)
sheet = book.sheet_by_index(0)
while 1:
    try:
        cell = sheet.cell(Num, 1).value
        # print(cell)
        Num = Num + 1
    except:
        lensheet = Num - 1
        break
Num = 1
while 1:
    try:
        cell = sheet.cell(rowx=1, colx=Num).value

        Num = Num + 1
    except:
        widthsheet = Num
        break

#Generate some random numbers in the sample size range
# so that the samples for generating the training and test sets later are randomly selected
b_list = range(2, lensheet + 1)
random2.seed(1)
blist_webeld = (random2.sample(b_list, (int)((lensheet - 1) * train_par)))

# Some input operations:Store the training set data using X, Y variables and
# save the name of the parameters in "Titel", return the hyperparameters
X = [[0] * (len(blist_webeld)) for i in range(widthsheet + 1)]
Y = [0] * (len(blist_webeld))
XX = [[0] * (lensheet - len(blist_webeld)) for i in range(widthsheet + 1)]
YY = [0] * (lensheet - len(blist_webeld))


def getin(X, XX):
    num = 2
    hypp = []
    while num <= widthsheet:
        Sum = 0
        while Sum <= len(blist_webeld) - 1:
            hh = blist_webeld[Sum]
            X[num - 1][Sum] = sheet.cell(rowx=hh, colx=num - 1).value
            if (num == 2):
                Y[Sum] = sheet.cell(rowx=hh, colx=0).value
            Sum = Sum + 1
        Sum = 1
        step = 0
        while Sum <= lensheet - 2:
            if blist_webeld.count(Sum) == 0:
                XX[num - 1][step] = sheet.cell(rowx=Sum, colx=num - 1).value
                if (num == 2):
                    YY[step] = sheet.cell(rowx=Sum, colx=0).value
                step = step + 1
            Sum = Sum + 1
        num = num + 1
    for i in range(0, widthsheet):
        Titel.append(sheet.cell(rowx=0, colx=i).value)
    print(Titel)
    doc = open('NOG.txt', 'r')
    sstr = doc.read()
    doc.close()
    doc = open('NOG.txt', 'w')
    doc.truncate()
    doc.close()
    sstr = sstr.strip('\n')
    if (sstr == ""):
        hypp.append(Num_of_generation)
    else:
        hypp.append(int(sstr))
    doc = open('cxbp.txt', 'r')
    sstr = doc.read()
    doc.close()
    doc = open('cxbp.txt', 'w')
    doc.truncate()
    doc.close()
    sstr = sstr.strip('\n')
    if (sstr == ""):
        hypp.append(0.5)
    else:
        hypp.append(float(sstr))
    doc = open('mutpb.txt', 'r')
    sstr = doc.read()
    doc.close()
    doc = open('mutpb.txt', 'w')
    doc.truncate()
    doc.close()
    sstr = sstr.strip('\n')
    if (sstr == ""):
        hypp.append(0.2)
    else:
        hypp.append(float(sstr))
    doc = open('num_in_gen.txt', 'r')
    sstr = doc.read()
    doc.close()
    doc = open('num_in_gen.txt', 'w')
    doc.truncate()
    doc.close()
    sstr = sstr.strip('\n')
    if (sstr == ""):
        hypp.append(100)
    else:
        hypp.append(int(sstr))
    return hypp


# Set the standard of individual excellence, the smaller the fitness value, the better
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Tree", gp.PrimitiveTree, fitness=creator.FitnessMin, size=-1)

#Basic settings for primitive set
pset = gp.PrimitiveSet(name="MAIN", arity=widthsheet - 1 +
                       len(new_Submodel))  # The number of variables
pset.addPrimitive(operator.add, arity=2)  # add operators to primitive set
pset.addPrimitive(operator.sub, arity=2)
pset.addPrimitive(operator.mul, arity=2)
pset.addPrimitive(protectedDiv, arity=2)
pset.addPrimitive(protectedsqrt, arity=1)
#pset.addPrimitive(math.cos, 1)
#pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant(
    "rand101",
    lambda: 10 * random2.random())  # add ephemeral constant to primitive set


#Function for simulation of expression
def sim(tmmp):
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24 = symbols(
        'ARG0 ARG1 ARG2 ARG3 ARG4 ARG5 ARG6 ARG7 ARG8 ARG9 ARG10 ARG11 ARG12 ARG13 ARG14 ARG15 ARG16 ARG17 ARG18 ARG19 ARG20 ARG21 ARG22 ARG23'
    )
    f = simplify(tmmp)
    return f


# Function to transfer obtained expression from framework like "mul(add(x,y),z)" to "(x+y)*z"
def change(str, leng):
    step = 0
    ret = []
    Len = 0
    save = Stack()
    while step <= leng - 1:
        tag = 0
        if (str[step] == 'p'):
            tag = 1
            step = step + 9
            continue
        if (str[step] == 'a'):
            tag = 1
            save.push(1)
            step = step + 3
            continue
        if (str[step] == 's' and str[step + 1] == 'u'):
            tag = 1
            save.push(2)
            step = step + 3
            continue
        if (str[step] == 'm'):
            tag = 1
            save.push(3)
            step = step + 3
            continue
        if (str[step] == 'D'):
            tag = 1
            save.push(4)
            step = step + 3
            continue
        if (str[step] == ','):
            tag = 1
            c = save.pop()
            if (c == 1):
                ret.append('+')
            if (c == 2):
                ret.append('-')
            if (c == 3):
                ret.append('*')
            if (c == 4):
                ret.append('/')
            step = step + 1
            continue
        if (str[step] == 'A' and str[step + 1] == 'd'):

            ret.append('+')
            step = step + 3
        if (tag == 0):
            if (str[step] != ' '):
                ret.append(str[step])
            step = step + 1
    hhhh = ''.join(ret)
    return hhhh


# Function for calculating the size of the expression
def calen(ss):
    step = 0
    ret = 0
    while step <= len(ss) - 1:
        if (ss[step] == '/'):
            ret = ret + 1
            step = step + 1
            continue
        if (ss[step] == '+'):
            ret = ret + 1
            step = step + 1
            continue
        if (ss[step] == '*'):
            ret = ret + 1
            step = step + 1
            continue
        if (ss[step] == '/'):
            ret = ret + 1
            step = step + 1
            continue
        if (ss[step] == 'c'):
            ret = ret + 1
            step = step + 3
            continue
        if (ss[step] == 's'):
            ret = ret + 1
            step = step + 3
            continue
        if (ss[step] == 'A'):
            ret = ret + 1
            step = step + 1
        step = step + 1
    return ret


# Converts the default name of a variable in an expression to the variable name entered by the user
# For example: "ARG0 + ARG1" to "Temperatur + volumn". Here Temperatur and volumn are names of the first two variables
def rett(str):
    step = 0
    rets = ""
    siz = len(str)
    while (step <= siz - 1):
        if (str[step] == 'A'):
            step = step + 3
            num = 0
            while step <= siz - 1 and str[step] <= '9' and str[step] >= '0':
                num = num * 10
                num = num + int(str[step])
                step = step + 1
            rets = rets + Titel[num + 1]
        else:
            rets = rets + str[step]
            step = step + 1
    return rets


# Function for calculating individual FITNESS
def evaluateRegression(individual, Y, X, pset, m):

    # calculate the size of expression("mul2")

    func = gp.compile(expr=individual, pset=pset)
    sstr = ''
    doc = open('out.txt', 'w')
    print(individual, file=doc)
    doc.close()
    doc = open('out.txt', 'r')
    sstr = doc.read()
    doc.close()
    doc = open('out.txt', 'w')
    doc.truncate()
    doc.close()
    result = change(sstr, len(sstr))
    luck = 0
    hhhhh = str(result)
    mul2 = calen(hhhhh)

    #calculate the RMSE of the individual

    sqerrors = []
    for i in range(0, len(Y)):
        tmp = []
        for j in range(1, widthsheet):
            tmp.append(X[j][i])
        for j in range(0, len(new_Submodel)):
            dic = {}
            for k in range(1, widthsheet):
                dic[Titel[k]] = X[k][i]
            tmmp = new_Submodel[j]

            for key, value in dic.items():
                new_Submodel[j] = new_Submodel[j].replace(
                    key, str(value * 1.00000))
            ans = eval(new_Submodel[j])
            new_Submodel[j] = tmmp
            tmp.append(ans)
        sqerrors.append((func(*tmp) - Y[i])**2)
    # return the multieobjective fitness as the fitness of individual
    ret = math.sqrt(numpy.sum(sqerrors) / len(Y))
    if m == 2:
        ret = ret * ret
    ret = ret + mul2**2 * namda2
    return (ret,)


# Basic setting for the framework
toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1,
                 max_=3)  # The minimal and maximal height of initial tree
toolbox.register("individual", tools.initIterate, creator.Tree, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluateRegression, Y=Y, X=X, pset=pset, m=mod)
toolbox.register(
    "mate",
    gp.cxOnePoint)  # use one point crossover as the algorithm for mating
toolbox.register(
    "expr_mut", gp.genFull, min_=0, max_=2
)  # use one point mutation as the algorithm for mutation. The newly generated subtree's height in range(0,2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.register(
    "select", tools.selTournament,
    tournsize=5)  # use tournament algorithm to select individuals for mating

import numpy as np

# main function
if __name__ == "__main__":
    cnm = getin(X, XX)
    pop = toolbox.population(n=cnm[3])
    hof = tools.HallOfFame(
        50)  # the best 50 individuals in all generation are saved here

    def display_min(ind):
        fitness_list = [x.fitness.values[0] for x in ind]
        global fitness_min
        fitness_min = np.min(fitness_list)

        ind_min_number = np.where(fitness_list == fitness_min)
        ind_min = ind[ind_min_number[0][0]]

        doc = open('out.txt', 'w')
        print(ind_min, file=doc)
        doc.close()
        doc = open('out.txt', 'r')
        sstr = doc.read()
        doc.close()
        doc = open('out.txt', 'w')
        doc.truncate()
        doc.close()
        result = change(sstr, len(sstr))
        hhhhh = str(result)
        mul2 = calen(hhhhh)
        global rmse_min
        rmse_min = fitness_min - mul2**2 * namda2

        return rmse_min

    def display_max(ind):
        fitness_list = [x.fitness.values[0] for x in ind]
        fitness_max = np.max(fitness_list)

        ind_max_number = np.where(fitness_list == fitness_max)
        ind_max = ind[ind_max_number[0][0]]

        doc = open('out.txt', 'w')
        print(ind_max, file=doc)
        doc.close()
        doc = open('out.txt', 'r')
        sstr = doc.read()
        doc.close()
        doc = open('out.txt', 'w')
        doc.truncate()
        doc.close()
        result = change(sstr, len(sstr))
        hhhhh = str(result)
        mul2 = calen(hhhhh)
        rmse_max = fitness_max - mul2**2 * namda2

        return rmse_max

    def ind_min(ind):
        fitness_list = [x.fitness.values[0] for x in ind]
        fitness_min = np.min(fitness_list)

        ind_min_number = np.where(fitness_list == fitness_min)
        ind_min = ind[ind_min_number[0][0]]

        doc = open('out.txt', 'w')
        print(ind_min, file=doc)
        doc.close()
        doc = open('out.txt', 'r')
        sstr = doc.read()
        doc.close()
        doc = open('out.txt', 'w')
        doc.truncate()
        doc.close()
        result = change(sstr, len(sstr))
        hhhhh = str(result)

        return hhhhh

    #Display the average, square root and maximum and minimum values for individuals in each generation at the terminal

    stats = tools.Statistics(lambda ind: ind)
    stats.register("min", display_min)
    stats.register("max", display_max)
    #stats.register("ind_min", ind_min)

    #Run the algorithm
    algorithms.eaSimple(pop,
                        toolbox,
                        cxpb=cnm[1],
                        mutpb=cnm[2],
                        ngen=cnm[0],
                        stats=stats,
                        halloffame=hof,
                        verbose=True)

    #Output the optimal individual as solution
    #(as some illegal solutions may be generated, find the optimal 40 individuals first, and select the individuals with the best fitness among them)
    step = 0
    luckk = 0
    while (step <= 50):

        individuals = hof
        fitness_list = [x.fitness.values[0] for x in individuals]
        fitness_min = np.min(fitness_list)

        ind_min_number = np.where(fitness_list == fitness_min)
        indd = individuals[ind_min_number[0][0]]

        print(
            "------------------------------------------------------------------"
        )
        doc = open('out.txt', 'w')
        print(indd, file=doc)
        doc.close()
        doc = open('out.txt', 'r')
        sstr = doc.read()
        doc.close()
        doc = open('out.txt', 'w')
        doc.truncate()
        doc.close()
        result = change(sstr, len(sstr))
        for i in range(0, len(new_Submodel)):
            mtp = "ARG" + str(widthsheet - 1 + i)
            result = result.replace(mtp, "(" + new_Submodel[i] + ")")
        for i in range(1, widthsheet):
            result = result.replace(Titel[i], "ARG" + str(i - 1))
        #print(result)
        fk = ''
        fk = sim(result)
        hhhh = str(fk)
        #print(fk)
        if (not ("nan" in hhhh) and not ("zoo" in hhhh)):
            mul2 = calen(hhhh)
            doc = open('out.txt', 'w')
            print(hhhh, file=doc)
            doc.close()
            doc = open('out.txt', 'r')
            fk = doc.read()
            doc.close()
            doc = open('out.txt', 'w')
            doc.truncate()
            doc.close()
            fin_ans = rett(hhhh)
            if luckk == 0:
                doc = open('tmp.txt', 'w')
                print(fin_ans, file=doc)
                print(rmse_min, file=doc)
                print(fitness_min, file=doc)
                luckk = 1
                doc.close()
                print("Best Formula")
                print(fin_ans)
                print("Best RMSE")
                print(rmse_min)
                print("Best Multifitness")
                print(fitness_min)
                # print("on test set")
                # print(
                #     evaluateRegression(indd, YY, XX, pset, mod)[0] -
                #     namda2 * mul2**2)
                break
            step = step + 1
