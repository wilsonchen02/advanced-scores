def print_list(input_list):
    # print everything like this until the last item
    for i in range(len(input_list) - 1):
        print(input_list[i], end=', ')

    # add "and" before the last item in the list
    print('and ' + input_list[-1])

def main():
    test_list = list(['bing', 'bong', 'bop', 'heehawww', 'wingdading', 'blehh'])
    print_list(test_list)

if __name__ == "__main__":
    main()