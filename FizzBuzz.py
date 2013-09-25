"""
Write a program that prints out the numbers 1 to 100 (inclusive).
If divisible by 3: print Fizz instead of the number
If divisible by 5: print Buzz
If divisible by both: print FizzBuzz
"""

n = 100
for x in range(1, n+1):
	if (x % 3): 
		n3 = False
	else:
		n3 = True

	if (x % 5): 
		n5 = False
	else:
		n5 = True

	if n3 and n5:
		print 'FizzBuzz'
	elif n3:
		print 'Fizz'
	elif n5:
		print 'Buzz'
	else:
		print x


