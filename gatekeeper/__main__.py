from gatekeeper.cli import parse_args


def main():
    cmd = parse_args()
    cmd.func(cmd)


if __name__ == '__main__':
    main()
