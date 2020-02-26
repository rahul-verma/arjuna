
def give_me_squares(n):
    for i  in range(n):
        yield i**2

g = give_me_squares(5)
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))