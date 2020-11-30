
if __name__ == "__main__":
    import sys
    from .formatter import format_split, split
    info = split(sys.argv[1])
    print(format_split(info)+"\n"+info[-1])
