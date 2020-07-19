#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 12:29:12 2020

@author: yeh
"""

with open("/Users/yeh/PycharmProjects/optimisation/knapsack_data/inst4_w.txt")  as f:
    try:
        data = f.readlines()
    finally:
        f.close()

p = []
count = 0
for l in data:
    count += 1
    p = l.strip().split(' ')
    print(count, ":", p[0], ",")
    