import sys

dicta = []
dicta.append((1,1))
dicta.append((2,2))
dicta.append((3,0))

dicta.sort(key= lambda key: key[0],reverse=True)

print dicta


print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', repr(sys.argv)
