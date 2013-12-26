class ChatBootstrap(object):
    logger = None
    device_one = None
    device_two = None
    starter = None

    def start(self):
        self.device_one.initialize()
        self.device_two.initialize()
        self.starter.start()
