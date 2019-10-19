# -*- coding: UTF-8 -*-
def integer_error_handle(input):
    if input.isdigit():
        return int(input)
    else:
        print('Please input integer')
        exit()

def division(divisor, dividend_array):
    print('Output:')
    for x in range(divisor):
        count = 0
        for y in range(len(dividend_array)):
            if dividend_array[y]%divisor == x:
                count = count+1
        print(count, end=" ")
            
def main():
    print('Input:')
    dividend_array = []
    divisor = input()
    divisor = integer_error_handle(divisor)
    while(True):
        dividend = input()
        if dividend == '-1':
            break
        else:
            dividend = integer_error_handle(dividend)
            dividend_array.append(dividend)
    division(divisor, dividend_array)

if __name__ == "__main__":
    main()