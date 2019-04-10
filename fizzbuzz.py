"""
My take on popular Interview exercise called FizzBuzz.

"""

class Solution:

    def run(self, N, M):
        newM = M + 1
        sequence = ""
        for num in range(N,newM):
            if num % 3 == 0 and num % 5 == 0:
                sequence = sequence + "FizzBuzz" + ","
                continue
            elif num % 5 != 0 and num % 3 != 0:
                sequence = sequence + str(num) + ","
                continue
            elif num % 3 == 0:
                sequence = sequence + "Fizz" + ","
                continue
            elif num % 5 == 0:
                sequence = sequence + "Buzz" + ","
                continue

        sequence = sequence[:-1]
        return sequence

solution = Solution()
print(solution.run(5,15))