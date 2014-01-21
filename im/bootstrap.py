class ChatBootstrap(object):
    """
    :type logger: L{logging.Logger}
    :type device_one: L{pycloudia.bootstrap.device.Device}
    :type device_two: L{pycloudia.bootstrap.device.Device}
    :type starter: L{pycloudia.bootstrap.interfaces.IStarter}
    """
    logger = None
    device_one = None
    device_two = None
    starter = None

    def start(self):
        self.device_one.start()
        self.device_two.start()
        self.starter.start()
