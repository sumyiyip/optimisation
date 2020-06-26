#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 15:04:33 2020

@author: yeh
"""

from pyomo.environ import *

opt = SolverFactory('cplex',executable = '/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx/cplex')


model = AbstractModel()

model.N = Param(within=PositiveIntegers)
model.k = Param(within=RangeSet(model.N))#k个中心
model.M = Param(within=PositiveIntegers)

model.c = RangeSet(model.N)#the location of the centers
model.i = RangeSet(model.M)#the location of the points

model.d = Param(model.c, model.i) #distance between c and i 

model.x = Var(model.c, model.i, within=Binary, initialize=0) #i 处在 c为中心的的范围内
model.y = Var(model.c, within=Binary) # 坐标c是否为中心


def obj_rule(model):
    return max(model.d[c,i]*model.x[c,i] for c in model.c for i in model.i)


model.obj = Objective(sense=minimize, rule=obj_rule)

def x_constraint(model, m):
    return sum(model.x[n,m] for n in model.c) == 1
# all the vertices are covered
model.x_cons = Constraint(model.i, rule=x_constraint)

def y_constraint(model, m , n):
    return model.x[n, m] <= model.y[n]
model.y_cons = Constraint(model.c, model.i, rule=y_constraint)

def k_rule(model):
    return sum( model.y[n] for n in model.c ) == model.k
model.k_cons = Constraint(rule=k_rule)


data_1 = {None:{
    'N':{None: 5},
    'k':{None: 2},
    'M':{None: 5},
    'd':{
    (1, 1) :                0.0,
    (1, 2) :                2.0,
    (1, 3) : 1.4142135623730951,
    (1, 4) :                2.0,
    (1, 5) : 2.8284271247461903,
    (2, 1) :                2.0,
    (2, 2) :                0.0,
    (2, 3) : 1.4142135623730951,
    (2, 4) : 2.8284271247461903,
    (2, 5) :                2.0,
    (3, 1) : 1.4142135623730951,
    (3, 2) : 1.4142135623730951,
    (3, 3) :                0.0,
    (3, 4) : 1.4142135623730951,
    (3, 5) : 1.4142135623730951,
    (4, 1) :                2.0,
    (4, 2) : 2.8284271247461903,
    (4, 3) : 1.4142135623730951,
    (4, 4) :                0.0,
    (4, 5) :                2.0,
    (5, 1) : 2.8284271247461903,
    (5, 2) :                2.0,
    (5, 3) : 1.4142135623730951,
    (5, 4) :                2.0,
    (5, 5) :                0.0}
    
    }}

instance_1 = model.create_instance(data_1)
results = opt.solve(instance_1)

instance_1.pprint()






