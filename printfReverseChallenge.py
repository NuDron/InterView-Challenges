"""
Method reproduce the C++ printf method and prints numbers from n variable in reverse order.
"""
#Recreation of C++ printf method
def printf(format, *values):
    print(format % values )

n = 1024
while(n>0):
    printf("%d", n % 10)
    n = n / 10
