"""
Q1. Write the script to find the teams to play matches with the opponent.
Input:
Team1
Team2
Team3
Team4
Team5

Output:
Team1	Team2
Team1	Team3
Team1	Team4
Team1	Team5
Team2	Team3
Team2	Team4
Team2	Team5
Team3	Team4
Team3	Team5
Team4	Team5
"""

total_teams = int(input('Enter Total number of Teams:'))
teams = []
for team in range(total_teams):
    teams.append(input('Enter Team Name:')) 

matches = []
for index, team1 in enumerate(teams):
    # If teams are not finished to match with others
    if not(index == len(teams)-1):
        # Get the remaining teams for team1 to play match with
        for team2 in teams[index+1:]:
            matches.append([team1, team2])
    
for index, match in enumerate(matches):
    print(f'Match {index+1}: {match[0]} and {match[1]}')

# -----------------------------------------------------------------------------
"""
Q2:
Write a program using Python to add the fraction numbers from an expression given in a list. 
Compute the sum and fully reduce the resultant fraction to its simplest form.
e.g
Input = ['1/2+1/3', '1/2+1/6', '2/4+3/5']

Output = ['5/6', '2/3', '11/10']
"""

def gcd(num1, num2):
    """
    Returns GCD of Two Numbers
    """
    if num1 == 0:
        return num2
    return gcd(num2%num1, num1)

def simplest_form(numerator, denominator):
    """
    Returns simplest form of numerator and denominator
    """
    # Get the gcd number to divide the numbers to get simplest form
    gcd_number = gcd(numerator,denominator)
    # Get the simplest form by diving gcd_number 
    simplest_numerator = numerator/gcd_number
    simplest_denominator = denominator/gcd_number
    return simplest_numerator, simplest_denominator

def add_fraction(numerators, denominators):
    """
    Adds Two Fractions and returns simplest form of the answer
    """
    denominator = (denominators[0]*denominators[1])/gcd(
        denominators[0], denominators[1]
    )
    numerator = numerators[0]*(denominator/denominators[0]) + \
        numerators[1]*(denominator/denominators[1])
    return simplest_form(numerator, denominator)

numbers_list = ['1/2+1/3', '1/2+1/6', '2/4+3/5']
print(f'Input = {numbers_list}')
numerators = []
denominators = []
output = []
for numbers in numbers_list:
    # Lets get two numbers
    num1, num2 = numbers.split("+")
    # Seperate out numerators and denominators
    num1_numerator, num1_denominator = num1.split('/')
    num2_numerator, num2_denominator = num2.split('/')
    # Group numerators of two numbers together in a list
    numerators.append([int(num1_numerator), int(num2_numerator)])
    # Group denominators of two numbers together in a list
    denominators.append([int(num1_denominator), int(num2_denominator)])

for numerator, denominator in zip(numerators, denominators):
    numerator, denominator = add_fraction(numerator, denominator)
    output.append(f'{int(numerator)}/{int(denominator)}')

print(f'Output = {output}')