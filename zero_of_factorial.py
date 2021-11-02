'''
https://www.codewars.com/kata/52f787eb172a8b4ae1000a34/train/python
Write a program that will calculate the number of trailing zeros in a factorial of a given number.
'''


def zeros(n):
    count = 0
    while(n/5 >= 1):
        count += int(n/5)
        n /= 5
    return count
