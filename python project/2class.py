import random

print(random.random())
print(random.randint(2,9))
print(random.randrange(0,9,2))
print(random.uniform(2,5))
# prints .random any float no. from 0.0 to 1.0
# print .randiant(range-a,b)gives random no. between the range a and b
# print .randrange(start,stop,step) gives random no. even no.
# print .uniform(a,b) gives random float no. between a and b
# print .choice(list) gives random element from the list
#  print .shuffle (list) shuffles the list in place
# print .choice(list) gives random element from the list
numbers = [ 10,20,30]
print(random.choices(numbers,weights=[1,1,3],k=3))
# print .choices(list,weights,k) 
# gives random elements from the list with weights and k is the number of elements wants to print
dice = random.randint(1,6)
print(dice)


s = list(range(1, 29))
weights = [1,1,1,1,1,11,1,1,1,1,1,1,1,1,1,11,1,1,1,1,1,1,4,5,6,6,344,3]
result = random.choices(s, weights=weights, k=100)
print(result)

