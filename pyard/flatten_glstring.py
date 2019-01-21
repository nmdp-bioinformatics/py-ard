from glstring import flatten
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile",
                        required=True,
                        help="input file",
                        type=str)

    parser.add_argument("-o", "--outfile",
                        required=True,
                        help="output file",
                        type=str)
    args = parser.parse_args()

    infile = args.infile
    outfile = args.outfile
    print("reading from ", infile)
    print("writing to ", outfile)

    fin = open(infile, 'r')
    fout = open(outfile, 'w')

    with fin as lines:
        for line in lines:
            (id, gl) = line.rstrip().split('%')
            fgl = flatten(gl)
            fout.write('%'.join([id, fgl]) + '\n')
    fin.close()
    fout.close()


if __name__ == '__main__':
    """The following will be run if file is executed directly,
    but not if imported as a module"""
    main()
