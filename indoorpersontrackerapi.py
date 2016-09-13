class IndoorPersonTrackerAPI:

    def __init__(self):
        from suds.client import Client
        url = 'http://10.0.0.8:8080/WebServices/iptwebservice?wsdl'
        self.client = Client(url)

    def updateDetection(self, roomNumber, probFalseDetection):
        self.client.service.updateDetection(roomNumber, probFalseDetection)

    def updateIdentification(self, roomNumber, personName, probFalseDetection):
        self.client.service.updateIdentification(roomNumber, personName, probFalseDetection)

