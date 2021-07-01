import sys


def get_min(number_list):
    return min(number_list)


if __name__ == "__main__":
    input_list = []
    input_number = input('key in number: ')
    while input_number:
        if input_number == "9999":
            print(f'mininum number is {get_min(input_list)}')
            sys.exit()
        else:
            input_list.append(int(input_number))
            input_number = input('key in number: ')
