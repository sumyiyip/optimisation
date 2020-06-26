#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 21:41:26 2020

@author: yeh
"""

from __future__ import division
from pyomo.environ import *

import numpy as np
import sys


opt = SolverFactory('cplex',executable = '/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx/cplex')

model = AbstractModel()
# data = DataPortal()

model.C = Set()
#set of the cities

model.n = Param(within=PositiveIntegers)

model.L = Param(model.C, within=Any)
#the coordinates of the cities

# model.c1 = Param(model.C)
# #the starting city
# model.D = Param(within=PositiveIntegers)
#departture city

model.M = RangeSet(model.n)
model.N = RangeSet(model.n)

model.S = RangeSet(1,model.n-1)
#the index of the cities, depending on the size of the city set

model.x = Var(model.N, model.M, within=Binary, initialize=0)



model.s = Var(model.S, within=IntegerSet)


#whether path x is selected 

# model.k = Var(model.N,within=PositiveIntegers, bounds=(1,4))
#the kth city being visited


model.d = Param(model.N, model.M, initialize= lambda model, i, j : sqrt(((model.L[i][0]- model.L[j][0])**2) + ((model.L[i][1]- model.L[j][1])**2) ))
#the direct distance between city i and j 

# =============================================================================
# def obj_expression(model):
#     return sum(model.x[i, j] * model.d[i, j] for i in model.N for j in model.M)
# 
# model.OBJ = Objective(sense=minimize, rule=obj_expression)
# =============================================================================
def obj_func(model):
    return sum(model.x[i,j] * model.d[i,j] for i in model.N for j in model.M)

model.objective = Objective(rule=obj_func,sense=minimize)

model.cuts = ConstraintList()
    

def obj_constraint_1(model, M):
    return sum(model.x[i,M] for i in model.N if i != M) ==1

model.const_1 = Constraint(model.M,rule=obj_constraint_1)

def obj_constraint_2(model, N):
    return sum(model.x[N,i] for i in model.M if i != N) ==1

model.const_2 = Constraint(model.N,rule=obj_constraint_2)

data = {None:{
    'C':{None:[1,2,3,4,5]},
    'L':{1:(0,0), 2:(0,2), 3:(1,1), 4:(2,0), 5:(2,2)},
    'n':{None: 5}
    }}

instance = model.create_instance(data)
results = opt.solve(instance)


instance.display()


# =============================================================================
# 
# next = [None]*(len(instance.C)+1)
# tour  = []
# first = list(instance.C)[0]
# min_tour = []
# size = len(tour)
# u = set()
# 
# def successor():
#     for i in instance.C:
#         next[i] = sum(j*instance.x[i,j] for j in instance.C)
#         
# def getTour():
#     global first
#     while True:
#         tour.append(first)
#         first = int(value(next[first]))
#         if first == 1:
#             break
#             
# def get_min_tour():
#     global size
#     global tour
#     if size < value(instance.n):
#         min_tour = tour
#         if size > 2:
#             u = tour
#             for i in instance.C:
#                 if i not in u:
#                     tour = []
#                     first = 1
#                     while True():
#                         tour.append(first)
#                         first = next(first)
#                         if first == i:
#                             break
#                     u.add(tour)
#                     if size > len(tour):
#                         min_tour = tour
#                         size = len(min_tour)
#                     if size == 2:
#                         break
#                     
# # =============================================================================
# # 
# # def const_3(model):
# #     return sum(instance.x[i,next[i]] for i in instance.C ) <= len(min_tour) -1
# # =============================================================================
# successor()
# getTour()
# get_min_tour()
#                       
# 
# instance.cuts.add(sum(value(instance.x[i,next[i]]) for i in instance.C) <= len(min_tour) -1)
# results = opt.solve(instance)
# print ("\n===== iteration")
# 
# instance.display()
# 
# 
# for i in List:
#     if instance.x[i]() != 0:
#         print(i,'--', instance.x[i]())
# =============================================================================

# =============================================================================
# for i in range(5):
#     expr = 0
# 
#     for j in instance.x:
#         if value(instance.x[j]) == 0:
#             expr += instance.x[j]
#             
#         else:
#             expr += (1-instance.x[j])
#             subtour.append(j)
# 
#     cons = sum(instance.x[d] for d in instance.s
#     
# 
#     new_cons = sum(instance.x[d] for d in subtour)<= expr -1 
#     instance.cuts.add(new_cons)
#     results = opt.solve(instance)
#     print ("\n===== iteration",i)
#     List = list(instance.x.keys())
#     for i in List:
#         if instance.x[i]() != 0:
#             print(i,'--', instance.x[i]())
# =============================================================================


        


'''如果存在subtour，是不是s的大小只要n/2就好了？？'''




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
# =============================================================================


    



    