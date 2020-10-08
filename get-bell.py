import sys, getopt, time
from decimal import Decimal

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'h')
    except getopt.GetoptError:
        print('get-bell.py <n>')
        sys.exit(2)

    for opt, _ in opts:
        if opt == '-h':
            print('get-bell.py <n>')
            sys.exit()

    if not args:
        print('usage: get-bell.py <n>')
        sys.exit(2)

    n = int(args[0])

    if n < 0:
        print('Number must be greater than or equal to zero')
        sys.exit(2)

    if n == 1:
        ordinal = '1st'
    elif n == 2:
        ordinal = '2nd'
    elif n == 3:
        ordinal = '3rd'
    else:
        ordinal = '{:,}th'.format(n)

    description = 'Bell number of the empty set (set with 0 elements)' if n == 0 \
        else ordinal + ' Bell number'

    print('Computing the {}...\n'.format(description))
    start_time = time.time()
    try:
        bell_num = get_bell(n)
    except KeyboardInterrupt:
        print('Aborted after {:e} seconds'.format(time.time() - start_time))
        sys.exit()

    bellWithThousands = '{:,}'.format(bell_num)
    bellScientific = '{:0.5e}'.format(Decimal(bell_num))
    bellDigits = len(str(bell_num))

    resultStr = '\nThe {} is exactly:\n{}\n\nOr approx. {}\n\nIt has {} digits.'
    print(resultStr.format(description, bellWithThousands, bellScientific, bellDigits))

    seconds = time.time() - start_time
    print('\nComputed in {:e} seconds'.format(seconds))


def get_bell(n):
    "Calculate the Bell number using a number triangle"

    if n == 0:
        # Bell number of the empty set is 1
        print('Method: Empty set')
        return 1

    print('Method: Number triangle')

    padding = len('{:,}'.format(n))

    # First row
    curr_row = [1]
    print('{} -> 1'.format('1'.rjust(padding)))

    # Subsequent rows
    for num in range(1, n):
        prev_row = curr_row

        # Current row starts with the last index of the previous row
        curr_row = [prev_row[len(prev_row) - 1]]

        for i in range(len(prev_row)):
            # Add previous index in the current row to the previous index
            # in the previous row
            prev_addend = prev_row[i]
            curr_addend = curr_row[i]
            curr_row.append(prev_addend + curr_addend)

        # Print the (approx.) result for this row of the number triangle
        bell_num = curr_row[len(curr_row) - 1]
        nStr = '{:,}'.format(num + 1).rjust(padding)
        result = '{} -> {:0.5e}'
        print(result.format(nStr, Decimal(bell_num)))

        # Print the row in this number triangle
        # row_str = ''
        # for el in curr_row:
        #     row_str = row_str + str(el) + ' '
        # print(row_str)

    # The nth Bell number is the last index of the current row
    return bell_num


if __name__ == "__main__":
    main(sys.argv[1:])
