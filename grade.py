# -*- coding: UTF-8 -*-
def integer_error_handle(input):
    if input.isdigit():
        return int(input)
    else:
        print('Please input integer')
        exit()

def grade_rank(number):
    grade_a_frequency = 0
    grade_b_frequency = 0
    grade_c_frequency = 0
    grade_d_frequency = 0
    for i in range(number):
        print('Score #%d:'%(i+1), end="")
        score = input()
        score = integer_error_handle(score)

        if score >= 87:
            grade_a_frequency = grade_a_frequency+1
        elif 87>score and score>=75:
            grade_b_frequency = grade_b_frequency+1
        elif 75>score and score>=65:
            grade_c_frequency = grade_c_frequency+1
        else:
            grade_d_frequency = grade_d_frequency+1

        return grade_a_frequency, grade_b_frequency, grade_c_frequency, grade_d_frequency

def count(n):
    for i in range(n):
        print('*', end="")

def output(a,b,c,d):
    print('\tGrade\tFrequency\tBar Chart')
    print('\tA\t%d\t', end="\t"%a)
    count(a)
    print("")
    print('\tB\t%d\t', end="\t"%b)
    count(b)
    print("")
    print('\tC\t%d\t', end="\t"%c)
    count(c)
    print("")
    print('\tD\t%d\t', end="\t"%d)
    count(d)
    print("")

def main():
    print('Number of Students:', end="")
    students_numbers = input()
    students_numbers = integer_error_handle(students_numbers)

    a,b,c,d = grade_rank(students_numbers)
    output(a,b,c,d)
    

if __name__ == "__main__":
    main()