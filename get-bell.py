import sys, getopt, time
from decimal import Decimal

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'n:o:h', ['number=', 'output=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    n, output = None, None
    for opt, arg in opts:
        if opt in ('-n', '--number'):
            n = int(arg)
        elif opt in ('-o', '--output'):
            output = arg
        elif opt in ('-h', '--help'):
            usage()
            sys.exit()
        else:
            usage()
            sys.exit(2)

    if not n:
        if args:
            n = int(args[0])
        else:
            print('Missing <number>')
            usage()
            sys.exit(2)

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
        print('\nAborted after {:e} seconds'.format(time.time() - start_time))
        sys.exit()

    bellWithThousands = '{:,}'.format(bell_num)
    bellScientific = '{:0.5e}'.format(Decimal(bell_num))

    approxResultStr = 'The {} is approximately:\n{}'.format(description, bellScientific)
    exactResultStr = 'The {} is exactly:\n{}'.format(description, bellWithThousands)

    seconds = time.time() - start_time
    executionStr = 'Computed in {:e} seconds'.format(seconds)
    print('\n' + executionStr)

    if displayScientific(bell_num):
        print('\n' + approxResultStr)

    print('\n' + exactResultStr)

    # Print to output file if selected
    if output:
        with open(output, "w") as output_file:
            output_file.write(executionStr + '\n\n')
            if displayScientific(bell_num):
                output_file.write(approxResultStr + '\n\n')
            output_file.write(exactResultStr)


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

        # Print the row number to indicate progress
        print(str(num + 1))

    # The nth Bell number is the last index of the current row
    return curr_row[len(curr_row) - 1]

def usage():
    print('usages:')
    print('\tget-bell.py <number>')
    print('\tget-bell.py -n <number>')
    print('\tget-bell.py --number=<number>')
    print('\noptions:')
    print('\t-h, --help\tDisplay this help information')
    print('\t-o, --output\tOutput results to the given file')

def displayScientific(num):
    # Show a scientific notation approximation for numbers greater than
    # a billion
    return num > 10 ** 9


if __name__ == "__main__":
    main(sys.argv[1:])
