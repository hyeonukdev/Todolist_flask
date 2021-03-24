
def return_test(a, b):
    c1 = "apple " + str(a)
    c2 = "banana " + str(b)

    print("c1_type : {}".format(type(c1)))

    return c1, c2


result = return_test(1, 2)
print("result : {}".format(result))
print("resutl_type : {}".format(type(result)))