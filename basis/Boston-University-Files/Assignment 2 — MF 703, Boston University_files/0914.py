# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 15:39:58 2017

@author: Administrator
"""

# always do the base case first!!!


def fac(n):
    print('fac(',n,')')
    if n <= 1:
        print('fac(',n,')','return 1')
        return 1
    
    fac_rest = fac(n-1)
    
    return n * fac_rest

print(fac(5))

def power(b,p):
    # base case
    if p == 0:
        return 1
    #handle negative powers:
    if p<0:
        denominator = power(b,-p)
        return 1/denominator
    #recursive case:
    else:
        power_rest = power(b,p-1)
        # do one step
        return b * power_rest
    
def mylen(s):
    #base case:
    if s == '':
        print('mylen(',s,'),return 0')
        return 0
    
    #recursive case:
    len_rest = mylen(s[1:])  #length of the string after s[0]
    
    #do our one step:
    print('mylen(',s,'),return', 1 + len_rest)
    return 1 + len_rest  #count 1 for s[0] + len_rest

#mylen("adfadsf,asdfadsf")

def double(s):
    #base case
    if s == '':
        return ''
    
    #recursive case:
    double_rest = double(s[1:])
    
    #our one step: handle s[0]
    return s[0] *2 + double_rest

#double("adfads")

def mymax(values):
    #base case:
    if len(values) == 1:
        print('mymax(',values,')','retuen',values[0])
        return values[:]  #return the value of first item
    
    #recursive case:
    max_rest = mymax(values[1:])
    if values[0] > max_rest:
        print('mymax(',values,')','returns',values[0])
        return values[0]
    else:
        print('mymax(',values,')','returns','mymax(values[1:])')
        return max_rest
    
#mymax("adxfykj")
    
    