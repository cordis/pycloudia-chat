class ChatBootstrap(object):
    """
    :type logger: L{logging.Logger}
    :type device: L{pycloudia.bootstrap.device.Device}
    :type starter: L{pycloudia.bootstrap.interfaces.IStarter}
    """
    logger = None
    device = None
    starter = None

    def start(self):
        self.device.start()
        self.starter.start()
