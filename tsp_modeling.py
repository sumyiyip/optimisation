#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 21:41:26 2020

@author: yeh
"""

from __future__ import division
from pyomo.environ import *
import random

import numpy as np
import sys
import matplotlib.pyplot as plt

opt = SolverFactory('cplex',executable = '/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx/cplex')

model = AbstractModel()


model.C = Set()
#set of the cities

model.n = Param(within=PositiveIntegers)


model.L = Param(model.C, within=Any)
#the coordinates of the cities


model.M = RangeSet(model.n)
model.N = RangeSet(model.n)

model.uncertainty = Param(model.M
                          , initialize= lambda self: random.uniform(-0.2, 0.2))

model.S = RangeSet(1,model.n-1)
#the index of the cities, depending on the size of the city set

model.x = Var(model.N, model.M, within=Binary, initialize=0)



model.d = Param(model.N, model.M, initialize= lambda model, i, j : sqrt(((model.L[i][0]- model.L[j][0])**2) + ((model.L[i][1]- model.L[j][1])**2) ))

# data.load(filename='/Users/yeh/_summer_coProject/data_1.json')


def obj_func(model):
    return sum(model.x[i,j] * model.d[i,j]*(1+model.uncertainty[i]) for i in model.N for j in model.M)

model.objective = Objective(rule=obj_func,sense=minimize)

model.cuts = ConstraintList()
    

def obj_constraint_1(model, M):
    return sum(model.x[i,M] for i in model.N if i != M) ==1

model.const_1 = Constraint(model.M,rule=obj_constraint_1)

def obj_constraint_2(model, N):
    return sum(model.x[N,i] for i in model.M if i != N) ==1

model.const_2 = Constraint(model.N,rule=obj_constraint_2)

data = {None:{
    'C':{None:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]},
    'L':{1:(1150,1760),2:(630,1660),3:(40,2090),4:(750,1100),5:(750,2030),6:(1030,2070),7:(1650,650),8:(1490,1630),9:(790,2260),10:(710,1310),11:(840,550),12:(1170,2300),13:(970,1340),14:(510,700),15:(750,900),16:(1280,1200),17:(230,590),18:(460,860),19:(1040,950),20:(590,1390),21:(830,1770),22:(490,500),23:(1840,1240),24:(1260,1500),25:(1280,790),26:(490,2130),27:(1460,1420),28:(1260,1910),29:(360,1980)},
    'n':{None: 29}
    }}

instance = model.create_instance(data)
results = opt.solve(instance)


adj_city = {}
tour  = set() #set of cities inside the subtour
first = list(instance.C)[0] #the first city
min_tour = set() #the smallest subtour
size = len(tour) 
u = set()

def successor():
    for i in instance.C:
        adj_city[i] = sum(j*instance.x[i,j] for j in instance.C)
        
def getTour():
    global first
    global tour
    global size
    while True:
        tour.add(first)
        first = round(value(adj_city[first]))
        if first == 1:
            size = len(tour)
            break
            
def get_min_tour():
    global size
    global tour
    global min_tour
    global u
    if size < value(instance.n):
        min_tour = tour
        if size > 2:
            u = tour
            for i in instance.C:
                if i not in u:
                    tour = set()
                    first = i
                    while True:
                        tour.add(first)
                        first = round(value(adj_city[first]))
                        if first == i:
                            break 
                    u = u.union(tour)
                    if size >= len(tour):
                        min_tour = tour
                        size = len(min_tour)
                    if size == 2:
                        break
    else:
        min_tour = tour
        
                    
successor()
getTour()
get_min_tour()
                    
while len(min_tour) != len(list((instance.C))):
                          
    expr = sum(instance.x[i,round(value(adj_city[i]))] for i in min_tour)
    expr_2 = sum(instance.x[round(value(adj_city[i])),i] for i in min_tour)
    expr_3 = sum(instance.x[i, j] for i in min_tour for j in set(instance.C).difference(min_tour))
    
    instance.cuts.add(expr <= len(min_tour) -1)
    if len(min_tour) >2:
        instance.cuts.add(expr_2 <= len(min_tour) -1)
    instance.cuts.add(expr_3 >= 1)
        
    List = list(instance.x.keys())
    for i in List:
        if instance.x[i]() > 0 and instance.x[i]() < 1:
            instance.x[i].fix(1)
    
    

    results = opt.solve(instance)
    # List = list(instance.x.keys())
    # for i in List:
    #     if instance.x[i]() != 0:
            
    #         plt.plot(instance.L[i[0]], instance.L[i[1]], color='r',linewidth=2)
    #         plt.scatter(instance.L[i[0]], instance.L[i[1]], color='b')

    #         print(i,'--', instance.x[i]())
    # instance.cuts.display()
    
    adj_city = {}
    tour  = set() #set of cities inside the subtour
    first = list(instance.C)[0] #the first city
    size = len(tour) 
    u = set()
    

    successor()
    getTour()
    get_min_tour()
    
    
print(value(instance.objective))
print("min_tour:" + str(min_tour) + str(len(min_tour)))
List = list(instance.x.keys())
for k in list(instance.L.values()):
    plt.scatter(k[0], k[1], color='b')

for i in List:
    if instance.x[i]() != 0:
        
        plt.plot([instance.L[i[0]][0],instance.L[i[1]][0]], [instance.L[i[0]][1],instance.L[i[1]][1]], color='r',linewidth=2)
        print(instance.L[i[0]], '---',instance.L[i[1]])

        print(i,'--', instance.x[i]())



# =============================================================================
# 
# def obj_constraint_3(model,i,j):
#     if i!= j:
#         return model.k[j] - model.k[i] + 4*(1-model.x[i,j]) >= 1
#     #如果x[i,j]=1, 则等价于k[j]>=k[i]+1。如果x[i,j]=0，则右端小于等于0，恒小于等于左端，相当于该约束不存在。
#     else:
#         return model.k[i] == model.k[i] 
#      #x[i,j]means theres a path from i to j so k[i] is smaller than k[j] 
#     
# model.const_3 = Constraint(model.N, model.M, rule=obj_constraint_3)
#
#
##using MTH algoirthm to eliminate the subtour
# =============================================================================


    



    
