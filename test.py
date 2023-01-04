x = ["x", "y", "z"]
y = "v w x"

print([character in x for character in y.split()])
if any([character in x for character in y.split()]):
    print("triggers")
else:
    print("doesn't trigger")
