def tester( problemSize ):
    num_iters = 0
    while problemSize > 0:
        num_iters += 1
        problemSize = problemSize // 2
    return num_iters

counts = [ 1_000, 2_000, 4_000, 10_000, 100_000 ]
for n in counts:
    iters = tester( n )
    print( "Problem Size: %d" % n)
    print( "Iterations:   %d" % iters)
    print()

for n in range(100):
    first = n**4
    second = pow(2,n)
    if first >= second:
        print( "%d) %d - %d" % (n,first,second) )