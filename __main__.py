import sys
from __init__ import analyzeModels, writeGraph


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "You must supply a model file and an output file."
        sys.exit()

    model_file = sys.argv[1]
    output_file = sys.argv[2]

    edges, inheritences, nodes = analyzeModels(model_file)
    writeGraph(edges, inheritences, nodes, output_file)
