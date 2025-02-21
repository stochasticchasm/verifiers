from verifiers.parsers import XMLParser

math_parser = XMLParser(fields=["reasoning", "answer"])
MATH_FEW_SHOT = [
    [
        {'role': 'user', 'content': 'What is the largest single-digit prime number?'},
        {'role': 'assistant', 'content': math_parser.format(
            reasoning='The largest single-digit prime number is 7.',
            answer='7'
        )}
    ]
]

DOUBLECHECK_FEW_SHOT = [
    [
        {'role': 'user', 'content': 'What is the largest single-digit prime number?'},
        {'role': 'assistant', 'content': math_parser.format(
            reasoning='The largest single-digit prime number is 7.',
            answer='7'
        )},
        {'role': 'user', 'content': 'Are you sure?'},
        {'role': 'assistant', 'content': math_parser.format(
            reasoning='The only larger single-digit numbers are 8 and 9, which are not prime. So yes, the answer is 7.',
            answer='7'
        )}
    ]
]

B64_FEW_SHOT = [
    [
        {'role': 'user', 'content': 'c2xpbWU='},
        {'role': 'assistant', 'content': math_parser.format(
            reasoning="""
Let me decode this step by step. The given base64 string is "c2xpbWU=".

We'll separate the input into 4-character groups:
Group 1: "c2xp"
Group 2: "bWU="

For Group 1 "c2xp", converting each character:
c (28) → 011100
2 (54) → 110110 
x (49) → 110001
p (41) → 101001

Concatenating and regrouping into 8-bit chunks:
01110011 → decimal 115 → 's'
01101100 → decimal 108 → 'l'
01101001 → decimal 105 → 'i'

For Group 2 "bWU=":
b (27) → 011011
W (22) → 010110
U (20) → 010100
= → padding

Concatenating and regrouping into 8-bit chunks:
01101101 → decimal 109 → 'm'
01100101 → decimal 101 → 'e'

Combining both decoded chunks "sli" + "me" gives us "slime".
            """,
            answer='slime'
        )},
        {'role': 'user', 'content': 'Are you sure?'},
        {'role': 'assistant', 'content': math_parser.format(
            reasoning='Yes, after checking walking throught the base64 decoding process, the decoded string is "slime".',
            answer='slime'
        )}
    ]
]

code_parser = XMLParser(fields=["reasoning", ("code", "answer")])
output_parser = XMLParser(fields=["output"])
CODE_FEW_SHOT = [
    [
        {
            'role': 'user',
            'content': 'What is sum of the first 100 positive even integers?'
        },
        {
            'role': 'assistant',
            'content': code_parser.format(
                reasoning='Let\'s compute the sum of the first 100 positive even integers.',
                code='print(sum(range(2, 102, 2)))'
            )
        },
        {
            'role': 'user', 
            'content': output_parser.format(output='2550')
        },
        {
            'role': 'assistant',
            'content': code_parser.format(reasoning='The answer is 2550.', answer='2550')
        },
        {
            'role': 'user',
            'content': 'What is the sum of the first 100 natural numbers, minus the largest prime number less than 100?'
        },
        {
            'role': 'assistant',
            'content': code_parser.format(
                reasoning='The sum of the first n natural numbers is given by the formula n(n+1)/2.',
                code='print(100*101/2)'
            )
        },
        {
            'role': 'user',
            'content': output_parser.format(output='5050')
        },
        {
            'role': 'assistant',
            'content': code_parser.format(
                reasoning='The sum of the first 100 natural numbers is 5050. Now we need to subtract the largest prime number less than 100.',
                code='print(5050 - 97)'
            )
        },
        {
            'role': 'user',
            'content': output_parser.format(output='4953')
        },
        {
            'role': 'assistant',
            'content': code_parser.format(
                reasoning='The largest prime number less than 100 is 97. Subtracting this from 5050 gives 4953.',
                answer='4953'
            )
        }
    ]
]