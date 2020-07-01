#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 15:04:33 2020

@author: yeh
"""

from pyomo.environ import *
import matplotlib.pyplot as plt


opt = SolverFactory('cplex',executable = '/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx/cplex')


model = AbstractModel()

model.N = Param(within=PositiveIntegers)
model.k = Param(within=RangeSet(model.N))#k个中心
model.M = Param(within=PositiveIntegers)

#the coordinates of the cities


model.c = RangeSet(model.N)#the location of the centers
model.i = RangeSet(model.M)#the location of the points

model.L = Param(model.i, within=Any)


model.d = Param(model.c, model.i, initialize= lambda model, i, j : sqrt(((model.L[i][0]- model.L[j][0])**2) + ((model.L[i][1]- model.L[j][1])**2) ))
#distance between c and i 

model.x = Var(model.c, model.i, within=Binary, initialize=0) #i 处在 c为中心的的范围内
model.y = Var(model.c, within=Binary) # 坐标c是否为中心
model.D = Var()


def obj_rule(model):
    return model.D


model.obj = Objective(sense=minimize, rule=obj_rule)


def x_constraint(model, m):
    return sum(model.x[n,m] for n in model.c) == 1
# all the vertices are covered and they can only have one center
model.x_cons = Constraint(model.i, rule=x_constraint)

def n_constraint(model, n):
    return sum(model.x[n,m] for m in model.i) >= 2*model.y[n]
model.n_const = Constraint(model.c, rule=n_constraint)
#every center must at least cover 2 points(including itself)

def y_constraint(model, m , n):
    return model.x[n, m] <= model.y[n]
model.y_cons = Constraint(model.c, model.i, rule=y_constraint)

def own_constraint(model, i):
    return model.x[i,i] == model.y[i]
model.o_cons = Constraint(model.c, rule=own_constraint)
#a center can be its own center


def k_rule(model):
    return sum( model.y[n] for n in model.c ) == model.k
model.k_cons = Constraint(rule=k_rule)
#restrict the number of centers to k

def D_constraint(model,c, i):
    return (model.d[c,i]*model.x[c,i]) <= model.D
model.D_cons = Constraint(model.c, model.i, rule=D_constraint)
#find the max distance of the vertice and its center

def x_y_constraint(model, b):
    return () 
    #if a and b are both centers, their areas cant be overlapped

data = {None:{
    'N':{None: 8},
    'k':{None: 3},
    'M':{None:8},
    'L':{1:(1150,1760),2:(630,1660),3:(40,2090),4:(750,1100),5:(750,2030),6:(1030,2070),7:(1650,650),8:(1490,1630)}
    
    }}

instance = model.create_instance(data)
results = opt.solve(instance)

instance.pprint()

for k in list(instance.L.values()):
    plt.scatter(k[0], k[1], color='b')
    
List = list(instance.x.keys())
for k in list(instance.L.values()):
    plt.scatter(k[0], k[1], color='b')

for i in List:
    if instance.x[i]() != 0:
        
        plt.plot([instance.L[i[0]][0],instance.L[i[1]][0]], [instance.L[i[0]][1],instance.L[i[1]][1]], color='r',linewidth=2)

        print(i,'--', instance.x[i]())






