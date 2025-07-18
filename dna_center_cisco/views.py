from django.shortcuts import render
import requests
from requests.auth import HTTPBasicAuth
from .dnac_config import DNAC
import urllib3
import sys
from .models import ActionLog
from .forms import AuthForm
from django.shortcuts import redirect

# Disable SSL warnings for sandbox
urllib3.disable_warnings()

class DNAC_Manager:
    def __init__(self, dnac_config=None):
        # Si no se pasa un diccionario, usa el importado por defecto
        from .dnac_config import DNAC as DEFAULT_DNAC
        self.DNAC = dnac_config if dnac_config else DEFAULT_DNAC.copy()
        self.token = None
    
    def get_auth_token(self, display_token=False):
        """Authenticates to DNA Center and stores token"""
        try:
            url = f"https://{self.DNAC['host']}:{self.DNAC['port']}/dna/system/api/v1/auth/token"
            response = requests.post(
                url,
                auth=HTTPBasicAuth(self.DNAC['username'], self.DNAC['password']),
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            self.token = response.json()['Token']
            
            if display_token:
                print("\n🔑 Authentication Token:")
                print("-"*50)
                print(self.token)
                print("-"*50)
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
            return False

    def get_network_devices(self):
        """Retrieves all network devices"""
        if not self.token:
            print("⚠️ Please authenticate first!")
            return None
            
        try:
            url = f"https://{self.DNAC['host']}:{self.DNAC['port']}/api/v1/network-device"
            headers = {"X-Auth-Token": self.token}
            response = requests.get(
                url, 
                headers=headers, 
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get('response', [])
            
        except Exception as e:
            print(f"❌ Failed to get devices: {str(e)}")
            return None

    def display_devices(self, devices):
        """Formats device list output"""
        if not devices:
            print("No devices found!")
            return
            
        print("\n📡 Network Devices")
        print("="*80)
        print(f"{'Hostname':20}{'IP Address':15}{'Platform':20}{'Status':10}")
        print("-"*80)
        
        for device in devices:
            print(
                f"{device.get('hostname', 'N/A'):20}"
                f"{device.get('managementIpAddress', 'N/A'):15}"
                f"{device.get('platformId', 'N/A'):20}"
                f"{device.get('reachabilityStatus', 'N/A'):10}"
            )

    def get_device_interfaces(self, device_ip):
        """Retrieves interfaces for specific device"""
        if not self.token:
            print("⚠️ Please authenticate first!")
            return None
            
        try:
            # Find device by IP
            devices = self.get_network_devices()
            device = next(
                (d for d in devices if d.get('managementIpAddress') == device_ip), 
                None
            )
            if not device:
                print(f"❌ Device {device_ip} not found!")
                return None
                
            # Get interfaces
            url = f"https://{self.DNAC['host']}:{self.DNAC['port']}/api/v1/interface"
            headers = {"X-Auth-Token": self.token}
            params = {"deviceId": device['id']}
            response = requests.get(
                url,
                headers=headers,
                params=params,
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get('response', [])
            
        except Exception as e:
            print(f"❌ Failed to get interfaces: {str(e)}")
            return None

    def display_interfaces(self, interfaces):
        """Formats interface output"""
        if not interfaces:
            print("No interfaces found!")
            return
            
        print("\n🔌 Device Interfaces")
        print("="*80)
        print(f"{'Interface':20}{'Status':10}{'VLAN':10}{'Speed':10}")
        print("-"*80)
        
        for intf in interfaces:
            print(
                f"{intf.get('portName', 'N/A'):20}"
                f"{intf.get('status', 'N/A'):10}"
                f"{intf.get('vlanId', 'N/A'):10}"
                f"{intf.get('speed', 'N/A'):10}"
            )
            
dnac_manager = DNAC_Manager();

def main():
    """Main program execution"""
    print("\n" + "="*50)
    print("Cisco DNA Center Network Automation")
    print("Canadian College of Technology and Business (CCTB)")
    print("="*50 + "\n")
    
    dnac = DNAC_Manager()
    
    while True:
        print("\n🔧 Main Menu")
        print("1. Authenticate & Show Token")
        print("2. List Network Devices")
        print("3. Show Device Interfaces")
        print("4. Exit")
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            if dnac.get_auth_token(display_token=True):
                print("✅ Authentication successful!")
                
        elif choice == "2":
            devices = dnac.get_network_devices()
            dnac.display_devices(devices)
            
        elif choice == "3":
            device_ip = input("Enter device IP address: ").strip()
            interfaces = dnac.get_device_interfaces(device_ip)
            dnac.display_interfaces(interfaces)
            
        elif choice == "4":
            print("Goodbye! 👋")
            sys.exit()
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

def authenticate_view(request):
    token = None
    success = False
    message = ""
    
    if dnac_manager.token:
        token = dnac_manager.token
        success = True
        message = "Authentication succeeded. Token acquired."
        context = {
                    'token': token,
                    'success': success,
                    'message': message
                }
        return render(request, 'authenticate.html', context)
    else:
        
        if request.method == 'POST':
            form = AuthForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                dnac_manager.DNAC['username'] = username
                dnac_manager.DNAC['password'] = password
                result = 'failure'
                try:
                    url = f"https://{dnac_manager.DNAC['host']}:{dnac_manager.DNAC['port']}/dna/system/api/v1/auth/token"
                    response = requests.post(
                        url,
                        auth=HTTPBasicAuth(username, password),
                        verify=False,
                        timeout=10
                    )
                    response.raise_for_status()
                    token = response.json()['Token']
                    dnac_manager.token = token
                    success = True
                    message = "Authentication succeeded. Token acquired."
                    result = 'success'
                except Exception as e:
                    success = False
                    message = f"Failed authentication:\n{str(e)}"
                ActionLog.objects.create(
                    action='authenticate',
                    result=result,
                    device_ip=None
                )
                context = {
                    'token': token,
                    'success': success,
                    'message': message
                }
                return render(request, 'authenticate.html', context)
            else:
                return render(request, 'index.html', {'form': form})
        else:
            form = AuthForm()
            return render(request, 'index.html', {'form': form})

def device_list_view(request):
    devices = None
    message = ""
    result = 'failure'
    
    if dnac_manager.token:
        devices = dnac_manager.get_network_devices()
        if devices:
            result = 'success'
        else:
            message = "No devices found or failed to retrieve devices."
    else:
        message = "You must authenticate first."
        
    ActionLog.objects.create(
        action='list_devices',
        result=result,
        device_ip=None,
    )
    context = {
        'devices': devices,
        'message': message
    }
    return render(request, 'devices.html', context)

def interface_list_view(request):
    device_ip = request.GET.get('ip')
    interfaces = None
    message = ""
    result = 'failure'
    
    if not device_ip:
        message = "Device IP not provided."
    elif not dnac_manager.token:
        message = "You must authenticate first."
    else:
        interfaces = dnac_manager.get_device_interfaces(device_ip)
        if interfaces:
            result = 'success'
        else:
            message = "No interfaces found or failed to retrieve interfaces."
    
    ActionLog.objects.create(
        action='list_interfaces',
        result=result,
        device_ip=device_ip,
    )
    
    context = {
        'interfaces': interfaces,
        'device_ip': device_ip,
        'message': message
    }
    return render(request, 'interfaces.html', context)

def logout_view(request):
    dnac_manager.token = None
    dnac_manager.DNAC['username'] = ''
    dnac_manager.DNAC['password'] = ''
    return redirect('/')
    
