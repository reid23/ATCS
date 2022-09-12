'''
Author: Reid Dye

This is my Recursion Menu file!

It contains the palindrome, digitsToWords,
sumToTarget, and choose methods, as well
as a simple CLI to demonstrate their use.
'''

import numpy as np

def palindrome(word: str) -> bool:
    # base case
    # if the first and last letter are not the same, 
    # it can't be a palindrome, so return false
    if word[0]!=word[-1]: return False

    # recurse to next word by removing first and last chars
    # if there's nothing left, there will be an IndexError,
    # meaning we got all the way through the word without
    # finding anything that breaks the palindrome pattern,
    # so return true.
    try:
        return palindrome(word[1:-1])
    except IndexError:
        return True


def digitsToWords(n: int) -> str:
    # init a pseudo-dict of idx:word
    words = [' zero',
            ' one',
            ' two',
            ' three',
            ' four',
            ' five',
            ' six',
            ' seven',
            ' eight',
            ' nine',
            ' ten']
    
    # base case: if there's only one digit,
    # just look up that digit, and remove 
    # the first char (space) because this 
    # is the first word. It's first because
    # this algorithm starts with the 1s place.
    if n<10: return words[n][1:]

    # recurse! get text for n with the ones 
    # digit removed, and tack on the ones 
    # digit's text to the end.
    return digitsToWords(n//10) + words[n%10]


def sumToTarget(nums: list[int], x: int) -> bool:
    # base case: if we've taken just the right
    # set of numbers to make a sum of x, x will
    # be zero because we subtract at every recursion
    # so return true and it will propagate up
    if x==0: return True

    # otherwise, for each element of nums, subtract
    # that element from x and see if you can sum to 
    # the target with that new sum. 
    for i in range(len(nums)):
        if sumToTarget(np.delete(nums, i), x-nums[i]): return True

    # if we got here, it means we didn't find the target
    # in any location, so we return false
    # aka another base case
    return False


def choose(n: int, k: int) -> int:
    # just an implementation of the given formula

    # base cases: 
    # if n<k, you can't choose a subset of size k
    if n<k: return 0

    # if k==0, you can't choose a subset of size 0
    if k==0: return 0

    #and the main recursion. Given in the problem.
    return choose(n-1, k) + choose(n-1, k-1)

def main():
    print('Welcome to the Recursion Calculator')
    main_menu='''
Choose a function:
1) palindrome
2) digitsToWords
3) sumToTarget
4) choose
9) Quit

Option: '''

    while True:
        match input(main_menu):
            case '1':
                possible_palindrome = input('\nEnter a possible palindrome: ')
                is_or_is_not = ['is not', 'is'][int(palindrome(possible_palindrome))]
                print(f'{possible_palindrome} {is_or_is_not} a palindrome.\n')
            case '2':
                while True:
                    try:
                        digit = int(input('\nEnter a positive integer: '))
                        assert digit>=0
                        break
                    except:
                        print('Not a valid positive integer, try again.')
                print(f'{digit} can be read as {digitsToWords(digit)}\n')
            case '3':
                print('\nEnter integers representing a list one at a time. Enter q to finish.')
                arr = []
                while True:
                    val = input('Enter a integer: ')
                    if val=='q': break
                    try: arr.append(int(val))
                    except: print('not a valid integer, try again.')
                while True:
                    try:
                        target = int(input('enter a target sum (integer): '))
                        break
                    except:
                        print('Not a valid integer, try again.')
                
                is_or_is_not = ['is not', 'is'][sumToTarget(arr, target)]
                print(f'There {is_or_is_not} a subset of {arr} whose sum is {target}\n')
            case '4':
                while True:
                    try:
                        n = int(input('\nEnter a total (positive integer): '))
                        assert n>=0
                        break
                    except:
                        print('Not a valid positive integer, try again')
                while True:
                    try:
                        k = int(input('\nEnter a number to choose (positive integer): '))
                        assert k>=0
                        break
                    except:
                        print('Not a valid positive integer, try again')
                
                print(f'{n} choose {k} is {choose(n, k)}')
            case '9':
                print('Exiting.')
                break
            case a:
                print(f'Expected valid option in 1, 2, 3, 4, 9 but received {a}. Try again.')

if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt: print('Exiting.')
    except EOFError: print('Exiting.')
