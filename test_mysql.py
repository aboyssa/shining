import requests
import json

print('🧪 Testing MySQL Flask server...\n')

def test_server():
    try:
        # Test health endpoint
        print('🔍 Testing health endpoint...')
        response = requests.get('http://localhost:5000/health')
        print(f'   Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print('✅ Server is running!')
            print(f'   Database: {data.get("database", "Unknown")}')
            print(f'   Discord: {data.get("discord", {}).get("clientId", "Unknown")}')
        else:
            print('❌ Server not responding properly')
            return
        
        # Test login endpoint
        print('\n🔍 Testing login endpoint...')
        login_data = {
            'discordId': '651015003843067904',
            'password': 'TestPass123!'
        }
        
        response = requests.post('http://localhost:5000/auth/login-password', 
                               json=login_data,
                               headers={'Content-Type': 'application/json'})
        
        print(f'   Status: {response.status_code}')
        print(f'   Response: {response.json()}')
        
        if response.status_code == 200:
            print('✅ Login successful!')
        else:
            print('❌ Login failed!')
            
    except requests.exceptions.ConnectionError:
        print('❌ Cannot connect to server. Make sure Flask server is running!')
    except Exception as e:
        print(f'❌ Error: {str(e)}')

if __name__ == '__main__':
    test_server() 