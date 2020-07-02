from __future__ import division
from pyomo.environ import *


model = AbstractModel()

model.capacity = Param(within=NonNegativeIntegers)

model.size = Param(within=PositiveIntegers)

model.Item = RangeSet(model.size)

model.value = Param(model.Item, within=PositiveIntegers)
model.weight = Param(model.Item, within=PositiveIntegers)

model.x = Var(model.Item, within=Binary)

def obj_expression(model):
	return sum(model.value[i]*model.x[i] for i in model.Item)

model.OBJ = Objective(sense=maximize, rule=obj_expression)

def ax_constraint_rule(model):
	return sum(model.weight[i] * model.x[i] for i in model.Item) <= model.capacity

model.AxbCOnstraint = Constraint(rule=ax_constraint_rule)


##TEST

data_init_1 = {None: dict(
        size = {None:6},
        capacity = {None : 190},
        # Item = {None: ["Apple", "Pear", "Orange", "Strawberry"]},
        weight = {1 : 56 ,
2 : 59 ,
3 : 80 ,
4 : 64 ,
5 : 75 ,
6 : 17},
        value = {1 : 50 ,
2 : 50 ,
3 : 64 ,
4 : 46 ,
5 : 50 ,
6 : 5 }
        )}



instance = model.create_instance(data_init_1)



if __name__ == '__main__':
    opt = SolverFactory('cplex',executable = '/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx/cplex')
    results_1 = opt.solve(instance, tee=True)
    results_1.write()
    print("\n Solution: \n" + '-'*60)
    instance.display()
