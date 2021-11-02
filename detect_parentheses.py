'''
https://www.codewars.com/kata/52774a314c2333f0a7000688/train/python
Write a function that takes a string of parentheses, and determines if the order of the parentheses is valid. The function should return true if the string is valid, and false if it's invalid.
'''


def valid_parentheses(string):
    left_parenthese = 0
    right_parenthese = 0
    for char_of_string in string:
        if char_of_string == "(":
            left_parenthese += 1
        elif char_of_string == ")":
            right_parenthese += 1
        if right_parenthese - left_parenthese > 0:
            return False
    if left_parenthese - right_parenthese != 0:
        return False
    else:
        return True
