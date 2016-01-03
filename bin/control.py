import sys
sys.path.append('/opt/rover/lib')
from control_client import control_client

# Create client object from ZeroMQ Library
client = control_client.ControlClient(
    '192.168.1.190',    # Server IP Address
    '5550'              # Server PORT number
)

# Main Program
while True:
    payload = {}
    payload['control'] = {'xy': 234}
    payload['telemetry'] = {'lat': -123.3342234}
    client.send(payload)

