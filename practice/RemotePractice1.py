import argparse

parser = argparse.ArgumentParser()

parser.add_argument('NumTimes',type=int)

args = parser.parse_args()

for i in range(args.NumTimes):
    print(f"Hello World x{i+1}")
