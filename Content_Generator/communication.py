import random

from wikipedia.exceptions import RedirectError


def get_category():
    with open("content_generator/categories.txt") as f:
        file_data = f.read()

    categories = file_data.split('\n')
    categories.pop(-1)

    random_index = random.randint(0, len(categories)-1)

    return categories[random_index]


def create_life_generator_input_csv(category):
    print('Creating CSV file to request data from Life Generator')
    f = open('requested_data.csv', 'w')

    # Insert .csv header
    f.write('Content generator requests data on the following category:\n')
    f.write('toys,')
    f.write(category)
    f.write(',1\n')


def read_life_generator_output():
    print('Reading data sent by Life Generator')
    f = open('output.csv', 'r')
    f.readline()
    result = f.readline().split(',')
    if(len(result) > 3):
        result.pop(2)
        result.pop(2)
        result.pop(-1)
    else:
        result = ['No luck this time. Try again...']
        result.append(result[0])
        result.append(result[0])

    print('\n')
    return result

# if __name__ == '__main__':

#     x = get_category()
#     print(x)
#     create_life_generator_input_csv(x)
#     read_life_generator_output()
