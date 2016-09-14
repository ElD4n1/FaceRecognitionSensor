import serverconfig

class IndoorPersonTrackerAPI:

    def __init__(self):
        from suds.client import Client
        url = 'http://{}:{}/WebServices/iptwebservice?wsdl'.format(serverconfig.IP, serverconfig.PORT)
        self.client = Client(url)

    def register(self, identifier):
        return self.client.service.register(identifier)

    def deregister(self, identifier):
        self.client.service.deregister(identifier)

    def updateDetection(self, identifier):
        self.client.service.updateDetection(identifier)

    def updateDetectionCustomPFD(self, identifier, probFalseDetection):
        self.client.service.updateDetectionCustomPFD(identifier, probFalseDetection)

    def updateIdentification(self, identifier, personName):
        self.client.service.updateIdentification(identifier, personName)

    def updateIdentificationCustomPFD(self, identifier, personName, probFalseDetection):
        self.client.service.updateIdentificationCustomPFD(identifier, personName, probFalseDetection)