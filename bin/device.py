#!/usr/bin/env python
import logging

from functools import partial
from argparse import ArgumentParser
from uuid import uuid4

from zmq.eventloop.ioloop import IOLoop
from tornado.platform.twisted import TornadoReactor

from pycloudia.uitls.net import get_ip_address
from pycloudia.devices.consts import DEVICE
from pycloudia.devices.beans import DeviceConfig
from pycloudia.reactor.twisted_impl import ReactorAdapter
from pycloudia.sockets.zmq_impl.factory import SocketFactory


class Factory(object):
    logger = logging.getLogger('device')

    def __init__(self, config):
        self.config = config
        self.io_loop = IOLoop.instance()
        self.reactor = ReactorAdapter(TornadoReactor(self.io_loop))
        self.sockets = SocketFactory.create_instance(self.io_loop)

    def initialize(self):
        agent = self._create_discovery_agent()
        self.reactor.call_when_running(agent.start)
        agent = self._create_discovery_agent()
        self.reactor.call_when_running(agent.start)

    def _create_discovery_agent(self):
        from pycloudia.devices.discovery.agent import AgentFactory
        from pycloudia.devices.discovery.udp import UdpMulticast
        from pycloudia.devices.discovery.protocol import DiscoveryProtocol
        factory = AgentFactory(self.sockets)
        factory.reactor = self.reactor
        factory.broadcast_factory = partial(UdpMulticast, DEVICE.UDP.HOST, DEVICE.UDP.PORT)
        factory.protocol = DiscoveryProtocol()
        return factory(str(uuid4()), self.config)

    def start(self):
        try:
            self.io_loop.start()
            self.logger.info('Started')
        except KeyboardInterrupt:
            self.reactor.subject.fireSystemEvent('shutdown')
            self.reactor.subject.disconnectAll()
            self.logger.info('Stopped')


def main():
    args = parse_args()
    config = create_config(args)
    factory = Factory(config)
    factory.initialize()
    factory.start()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--host', type=str, default=None, help='Bind host name or IP', required=False)
    parser.add_argument('-i', '--interface', type=str, default='', help='Bind interface name')
    parser.add_argument('--min-port', type=int, default=49152, help='Lower bound of ports range')
    parser.add_argument('--max-port', type=int, default=65536, help='Higher bound of ports range')
    return parser.parse_args()


def create_config(args):
    return DeviceConfig(
        host=get_host_from_args(args),
        min_port=args.min_port,
        max_port=args.max_port,
        interface=args.interface,
    )


def get_host_from_args(args):
    if args.host is not None:
        return args.host
    return get_ip_address(args.interface)


if __name__ == '__main__':
    main()
