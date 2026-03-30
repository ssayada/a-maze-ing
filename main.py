from launcher import launcher


def main():
    try:
        launcher()
    except OSError as e:
        print(e)


if __name__ == "__main__":
    main()
