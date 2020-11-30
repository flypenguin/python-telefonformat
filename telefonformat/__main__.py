
if __name__ == "__main__":
    import sys
    from .formatter import format
    print("\n".join(format(sys.argv[1])))
