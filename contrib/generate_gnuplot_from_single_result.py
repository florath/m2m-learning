import json
import sys
import numpy as np

def compute_mean(r, i, over):
    if i == 0:
        return 0
    elif i < over:
        return np.mean(r[0:i])
    else:
        return np.mean(r[i-over:i])

mean_over = [ 10, 100, 1000 ]
    
def main():
    with open(sys.argv[1], "r") as fd:
        res = json.load(fd)

    for i in range(len(res)):
        means = [ "%f" % compute_mean(res, i, x) for x in mean_over ]
        print("%d\t%f\t%s" % (i, res[i], "\t".join(means)))

if __name__ == '__main__':
    main()
