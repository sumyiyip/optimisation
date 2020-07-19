from __future__ import division
from pyomo.environ import *

model = AbstractModel()

model.capacity = Param(within=NonNegativeIntegers)

model.size = Param(within=PositiveIntegers)

model.uncertainty = Param(within=PositiveReals)
# implement the baseline

model.Item = RangeSet(model.size)

model.value = Param(model.Item, within=PositiveIntegers)
model.weight = Param(model.Item, within=PositiveIntegers)

model.x = Var(model.Item, within=Binary)


def obj_expression(model):
    return sum(model.value[i] * model.x[i] for i in model.Item)


model.OBJ = Objective(sense=maximize, rule=obj_expression)


def ax_constraint_rule(model):
    return sum(model.weight[i]* (1+model.uncertainty) * model.x[i] for i in model.Item) <= model.capacity


model.AxbCOnstraint = Constraint(rule=ax_constraint_rule)

##TEST

data_init_1 = {None: dict(
    uncertainty = {None: 0.2},
    size={None: 15},
    capacity={None: 750},
    weight={1 : 70 ,
2 : 73 ,
3 : 77 ,
4 : 80 ,
5 : 82 ,
6 : 87 ,
7 : 90 ,
8 : 94 ,
9 : 98 ,
10 : 106 ,
11 : 110 ,
12 : 113 ,
13 : 115 ,
14 : 118 ,
15 : 120},
    value={1 : 135 ,
2 : 139 ,
3 : 149 ,
4 : 150 ,
5 : 156 ,
6 : 163 ,
7 : 173 ,
8 : 184 ,
9 : 192 ,
10 : 201 ,
11 : 210 ,
12 : 214 ,
13 : 221 ,
14 : 229 ,
15 : 240 }
)}

instance = model.create_instance(data_init_1)

if __name__ == '__main__':
    opt = SolverFactory('cplex', executable='/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx/cplex')
    results_1 = opt.solve(instance, tee=True)
    results_1.write()
    print("\n Solution: \n" + '-' * 60)
    instance.display()
