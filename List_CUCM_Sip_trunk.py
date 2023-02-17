from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree
 
disable_warnings(InsecureRequestWarning)

# Cluster specific variables
username = 'username'
password = 'password'
server = 'PublisherIP'

wsdl = f'https://{server}:8443/realtimeservice2/services/RISService70?wsdl'
location = f'https://{server}:8443/realtimeservice2/services/RISService70'
binding = '{http://schemas.cisco.com/ast/soap}RisBinding'

session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, password)

transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
client = Client(wsdl=wsdl, transport=transport, plugins=[history])
service = client.create_service(binding, location)

CmSelectionCriteria = {
    'MaxReturnedDevices': '1000',
    'DeviceClass': 'SIPTrunk',
    'Model': '131',
    'Status': 'Any',
    'NodeName': '',
    'SelectBy': 'IPV4Address',
    'SelectItems': {
        'item': [
            '*'
        ]
    },
    'Protocol': 'Any',
    'DownloadStatus': 'Any'
}

StateInfo = ''

try:
    resp = service.selectCmDevice(CmSelectionCriteria=CmSelectionCriteria, StateInfo=StateInfo)
except Fault as e:
    print(f'Error: {e}')
else:
    servers=resp.SelectCmDeviceResult.CmNodes.item
    for server in servers:
        if server.ReturnCode == 'Ok':
            with open(f'/usr/local/nagios/libexec/check_sip/{server.Name}_sip_status','w') as srvfile:
                for trunk in server.CmDevices.item:
                     srvfile.write(f'{server.Name}:{trunk.Name}:{trunk.Status}\n')
