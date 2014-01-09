#!/usr/bin/env python

from argparse import ArgumentParser

from springpython.context import ApplicationContext

from im.ioc_config import ChatConfig


def main():
    args = parse_args()
    context = ApplicationContext(ChatConfig(args))
    bootstrap = context.get_object('bootstrap')
    bootstrap.start()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--host', type=str, default=None, help='Bind host', required=False)
    parser.add_argument('-i', '--interface', type=str, default='', help='Bind interface name')
    parser.add_argument('--min-port', type=int, default=49152, help='Lower bound of ports range')
    parser.add_argument('--max-port', type=int, default=65536, help='Higher bound of ports range')
    parser.add_argument('--udp-host', type=str, default='228.0.0.1', help='UDP group host')
    parser.add_argument('--udp-port', type=int, default=5000, help='UDP group port')
    parser.add_argument('--identity', type=str, default=None, help='Device identity')
    return parser.parse_args()


if __name__ == '__main__':
    main()
