class IndoorPersonTrackerAPI:

    def __init__(self):
        from suds.client import Client
        url = 'http://10.0.0.8:8080/WebServices/iptwebservice?wsdl'
        self.client = Client(url)

    def register(self, identifier):
        self.client.service.register(identifier)
	
    def updateDetection(self, identifier, probFalseDetection):
        self.client.service.updateDetection(identifier, probFalseDetection)

    def updateIdentification(self, identifier, personName, probFalseDetection):
        self.client.service.updateIdentification(identifier, personName, probFalseDetection)