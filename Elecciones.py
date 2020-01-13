#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 20:22:01 2020

@author: samuel
"""
##################
####Parameters####
##################
population_size=1000000

iterations_per_sample=10
samples_to_test=[10,50,500,1000]


import matplotlib.pyplot as plt
import random

class Person:
    def __init__(self,age,religion,education,vote):
        self.age=age
        self.religion=religion
        self.education=education
        self.vote=vote

def get_age():
    x=random.randint(1,100)
    if 0<x<=30:
        return random.randint(18,30)
    if 30<x<=55:
        return random.randint(31,50)
    if 55<x<=75:
        return random.randint(51,70)
    if 75<x<=100:
        return random.randint(70,80)
    
def get_religion():
    x=random.randint(1,100)
    if 0<x<=70:
        return ("christian", 56)
    if 70<x<=90:
        return ("hindu", 73)
    if  90<x<=100:
        return ("athiest", 58)
def get_education():
    x=random.randint(1,100)
    if 0<x<=30:
        return ("elementary",58)
    if 30<x<=60:
        return ("middle", 57)
    if 60<x<=80:
        return ("high", 51)
    if 80<x<=95:
        return ("college",50)
    if 95<x<=100:
        return ("graduate",44)
    
def get_vote(p_age,p_religion,p_education):
    x=random.randint(1,100)
    avg_prob=(p_age+p_religion+p_education)/3
    if x<=avg_prob:
        return "a"
    else:
        return "b"

def get_stats():
    age=get_age()
    p_age=-35/62*(age-18)+65
    religion,p_religion=get_religion()
    education,p_education=get_education()
    
    vote=get_vote(p_age,p_religion,p_education)
    return age,religion,education,vote

def populate(population_size):
    population=[]
    votes_for_a=0
    votes_for_b=0
    for i in range(population_size):
        age,religion,education,vote=get_stats()
        population.append(Person(age,religion,education,vote))
        if vote=="a":
            votes_for_a+=1
        else:
            votes_for_b+=1
    if votes_for_a>votes_for_b:
        winner="a"
    elif votes_for_a<votes_for_b:
        winner="b"
    else:
        winner="tie"
    return (population,winner,votes_for_a,votes_for_b)

def get_sample(sample_size,population):
    if sample_size>len(population):
        raise NameError
    sample=[]
    for i in range(sample_size):
        x=random.randint(0,len(population)-1)
        sample.append(population[x])
    return sample

def count_votes(sample):
    d={}
    religions=["christian","hindu","athiest"]
    education=["elementary","middle","high","college","graduate"]
    d["votes_for_a"]=0
    d["votes_for_b"]=0
    #d[i]=[voted,voted_for_a]
    for i in range(18,81):
        d[i]=[0,0]
    for i in religions:
        d[i]=[0,0]
    for i in education:
        d[i]=[0,0]
    for person in sample:
        d[person.religion][0]+=1
        d[person.age][0]+=1
        d[person.education][0]+=1
        if person.vote=="a":
            d[person.religion][1]+=1
            d[person.age][1]+=1
            d[person.education][1]+=1
            d["votes_for_a"]+=1
        else:
            d["votes_for_b"]+=1
    return d
 
def s_age_probability(dictionary,probability_dictionary):
    vote=0
    vote_for_a=0
    for i in range(5):
        vote+=dictionary[18+i][0]
        vote_for_a+=dictionary[18+i][1]
    for i in range(3):
        if vote==0:
            probability_dictionary[18+i]=0
        else:
            probability_dictionary[18+i]=100*vote_for_a//vote
    #find probabilities of voting for "a" by gropus
    for age in range(21,79):
        vote-=dictionary[age-3][0]
        vote_for_a-=dictionary[age-3][1]
        vote+=dictionary[age+2][0]
        vote_for_a+=dictionary[age+2][1]
        if vote==0:
            probability_dictionary[age]=0
        else:
            probability_dictionary[age]=100*vote_for_a//vote
    probability_dictionary[79]=probability_dictionary[78]
    probability_dictionary[80]=probability_dictionary[78]
    #if probability is not defined, set it equal to the closest value
    for age in range(18,80):
        i=1
        while probability_dictionary[age]==0:
            if i+age==81:
                break
            probability_dictionary[age]=probability_dictionary[age+i]
            i+=1
            
        i=1
    return probability_dictionary

def s_religion_probability(dictionary,probability_dictionary):
    religions=["christian","hindu","athiest"]
    for religion in religions:
        vote=dictionary[religion][0]
        vote_for_a=dictionary[religion][1]
        if vote==0:
            probability_dictionary[religion]=50
        else:
            probability_dictionary[religion]=100*vote_for_a//vote
    return probability_dictionary
    
def s_education_probability(dictionary,probability_dictionary):
    education=["elementary","middle","high","college","graduate"]
    for edu in education:
        vote=dictionary[edu][0]
        vote_for_a=dictionary[edu][1]
        if vote==0:
            probability_dictionary[edu]=50
        else:
            probability_dictionary[edu]=100*vote_for_a//vote
    return probability_dictionary


    
def get_sample_probabilities(dictionary):
    probability_dictionary={}
    probability_dictionary=s_age_probability(dictionary,probability_dictionary)
    probability_dictionary=s_religion_probability(dictionary,probability_dictionary)   
    probability_dictionary=s_education_probability(dictionary,probability_dictionary)
    return probability_dictionary


def calculate_winner(probability_dictionary,population):
    votes_for_a=0
    votes_for_b=0
    for person in population:
        p_age=probability_dictionary[person.age]
        p_education=probability_dictionary[person.education]
        p_religion=probability_dictionary[person.religion]
        prob_for_a=(p_age+p_education+p_religion)//3
        x=random.randint(1,100)
        if x<=prob_for_a:
            votes_for_a+=1
        else:
            votes_for_b+=1
    if votes_for_a>votes_for_b:
        return ("a",votes_for_a,votes_for_b)
    if votes_for_a<votes_for_b:
        return ("b",votes_for_a,votes_for_b)
    else:
        return ("tie",votes_for_a,votes_for_b)


def monte_carlo(sample_size,population):
    sample=get_sample(sample_size,population)
    dictionary=count_votes(sample)
    #sample probabilities
    probability_dictionary=get_sample_probabilities(dictionary)
    s_winner,s_votes_for_a,s_votes_for_b=calculate_winner(probability_dictionary,population)
    return s_winner,probability_dictionary,s_votes_for_a,s_votes_for_b

def print_iteration_results(right_guess,wrong_guess,sample_size):
    print("The simulation was successfully ran with a sample size of:",sample_size)
    print("It got the winner right in", right_guess,"iterations")
    print("It got the winner wrong in", wrong_guess,"iterations")
    
    

population,winner,votes_for_a,votes_for_b=populate(population_size)
for sample_size in samples_to_test:
    right_guess=0
    wrong_guess=0
    for i in range(iterations_per_sample):
        sample=get_sample(sample_size,population)
        s_winner,probability_dictionary,s_votes_for_a,s_votes_for_b=monte_carlo(sample_size,population)
        if winner==s_winner:
            right_guess+=1
        else:
            wrong_guess+=1
    print_iteration_results(right_guess,wrong_guess,sample_size)
    
print("The winner of the election was",winner)
print(votes_for_a,"people voted for a")
print(votes_for_b,"people voted for b")

print("The simulation predicted", s_votes_for_a,"votes for a")
print("And",s_votes_for_b,"votes for b")


religions=["christian","hindu","athiest"]
education=["elementary","middle","high","college","graduate"]

xage=[]
yage=[]

xreligion=[]
yreligion=[]

xeducation=[]
yeducation=[]

for i in range(18,81):
    xage.append(i)
    yage.append(probability_dictionary[i])

for i in religions:
    xreligion.append(i)
    yreligion.append(probability_dictionary[i])

for i in education:
    xeducation.append(i)
    yeducation.append(probability_dictionary[i])
    


fig1,ax1=plt.subplots()

plt.plot(xage,yage)
fig1.suptitle('Probability function for age', fontsize=20)
fig1.savefig('Figure.jpg')
plt.show()

fig2,ax2=plt.subplots()


plt.plot(xreligion,yreligion)
fig2.suptitle('Probability function for religion', fontsize=20)
fig2.savefig('Figure2.jpg')
plt.show()

fig3,ax3=plt.subplots()

plt.plot(xeducation,yeducation)
fig3.suptitle('Probability function for education', fontsize=20)
fig3.savefig('Figure3.jpg')
plt.show()


    