import random
numberOfStreaks = 0
for experimentNumber in range(10000):
    # Code that creates a list of 100 'heads' or 'tails' values.
    toss_results = list([])
    for i in range(100):
        toss_results.append(random.randint(0, 1))

    # Code that checks if there is a streak of 6 heads or tails in a row.
    # Convert the list of 0s and 1s into a string (using list comprehension)
    # https://www.w3schools.com/python/python_lists_comprehension.asp
    results2str = ''.join(str(item) for item in toss_results)
    # results2str = ''.join(map(str, toss_results))
    if '000000' in results2str or '111111' in results2str:
        numberOfStreaks += 1
print('Chance of streak: %s%%' % (numberOfStreaks / 100))