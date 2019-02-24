import sys
from payments.server import run_app


if __name__ == '__main__':
    try:
        port = sys.argv[1]
    except IndexError:
        port = 8080
    run_app(port)
