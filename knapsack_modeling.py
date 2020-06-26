from __future__ import division
from pyomo.environ import *


model = AbstractModel()

model.capacity = Param(within=NonNegativeIntegers)

model.Item = Set()

model.value = Param(model.Item, within=PositiveIntegers)
model.weight = Param(model.Item, within=PositiveIntegers)

model.x = Var(model.Item, within=Binary)

def obj_expression(model):
	return summation(model.value, model.x)

model.OBJ = Objective(sense=maximize, rule=obj_expression)

def ax_constraint_rule(model):
	return sum(model.weight[i] * model.x[i] for i in model.Item) <= model.capacity

model.AxbCOnstraint = Constraint(rule=ax_constraint_rule)


##TEST

data_init_1 = {None: dict(
        capacity = {None : 10},
        Item = {None: ["Apple", "Pear", "Orange", "Strawberry"]},
        value = {"Apple":4, "Pear":2,"Orange":3, "Strawberry":5},
        weight = {"Apple":2, "Pear":3,"Orange":3, "Strawberry":4}
        )}

data_init_2 = {None: dict(
        capacity = {None : 10},
        Item = {None: ["Cat", "Dog", "Snake", "Monkey", "Fish"]},
        value = {"Cat":1, "Dog":2, "Snake":3, "Monkey":4, "Fish":1},
        weight = {"Cat":2, "Dog":3, "Snake":2, "Monkey":5, "Fish":1}
        )}



instance_1 = model.create_instance(data_init_1)
instance_2 = model.create_instance(data_init_2)



if __name__ == '__main__':
    opt = SolverFactory('cplex',executable = '/Applications/CPLEX_Studio1210/cplex/bin/x86-64_osx/cplex')
    results_1 = opt.solve(instance_1, tee=True)
    results_2 = opt.solve(instance_2, tee=True)
    results_1.write()
    print("\n Solution: \n" + '-'*60)
