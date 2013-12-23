#!/usr/bin/env python
import logging

from argparse import ArgumentParser
from uuid import uuid4

from zmq.eventloop.ioloop import IOLoop
from tornado.platform.twisted import TornadoReactor

from pycloudia.uitls.net import get_ip_address
from pycloudia.devices.beans import DeviceConfig
from pycloudia.reactor.twisted_impl import ReactorAdapter
from pycloudia.streams.zmq_impl.factory import StreamFactory


class Factory(object):
    logger = logging.getLogger('device')

    def __init__(self, options):
        self.options = options
        self.io_loop = IOLoop.instance()
        self.reactor = ReactorAdapter(TornadoReactor(self.io_loop))
        self.streams = StreamFactory.create_instance(self.io_loop)

    def initialize(self):
        agent = self._create_discovery_agent(str(uuid4()))
        self.reactor.call_when_running(agent.start)
        agent = self._create_discovery_agent(str(uuid4()))
        self.reactor.call_when_running(agent.start)

    def _create_discovery_agent(self, identity):
        config = self._create_device_config()
        config.identity = identity
        from pycloudia.devices.discovery.agent import AgentFactory
        from pycloudia.devices.discovery.protocol import DiscoveryProtocol
        from pycloudia.devices.discovery.udp import UdpMulticastFactory
        factory = AgentFactory(self.streams)
        factory.reactor = self.reactor
        factory.protocol = DiscoveryProtocol()
        factory.broadcast_factory = UdpMulticastFactory(self.options.udp_host, self.options.udp_port)
        return factory(config)

    def start(self):
        try:
            self.io_loop.start()
            self.logger.info('Started')
        except KeyboardInterrupt:
            self.reactor.subject.fireSystemEvent('shutdown')
            self.reactor.subject.disconnectAll()
            self.logger.info('Stopped')

    def _create_device_config(self):
        return DeviceConfig(
            host=self._get_host_from_options(),
            min_port=self.options.min_port,
            max_port=self.options.max_port,
            identity=self.options.identity,
        )

    def _get_host_from_options(self):
        if self.options.host is not None:
            return self.options.host
        return get_ip_address(self.options.interface)


def main():
    args = parse_args()
    factory = Factory(args)
    factory.initialize()
    factory.start()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--host', type=str, default=None, help='Bind host', required=False)
    parser.add_argument('-i', '--interface', type=str, default='', help='Bind interface name')
    parser.add_argument('--min-port', type=int, default=49152, help='Lower bound of ports range')
    parser.add_argument('--max-port', type=int, default=65536, help='Higher bound of ports range')
    parser.add_argument('--udp-host', type=str, default='228.0.0.1', help='UDP group host')
    parser.add_argument('--udp-port', type=int, default=5000, help='UDP group port')
    parser.add_argument('--identity', type=str, default=str(uuid4()), help='Device identity')
    return parser.parse_args()


if __name__ == '__main__':
    main()
