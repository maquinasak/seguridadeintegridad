import asyncio, asyncssh, crypt, sys, time, random

def handle_client(process):
    process.exit(0)

class MySSHServer(asyncssh.SSHServer):
    def connection_made(self, conn):
        self._conn = conn

    def password_auth_supporte(self):
        return True
    
    def validate_passrod(self, username, password):
        print(f'Login attemp from  with username {username} and password {password}')
        time.sleep(random.randint(0,5))
        raise asyncssh.DisconnectError(10, "Connection lost")
    
async def start_server():

    # Read the private key files
    with open('host_rsa_key.pem', 'r') as f:
        host_rsa_key = f.read()

    with open('host_ecdsa_key.pem', 'r') as f:
        host_ecdsa_key = f.read()

    with open('host_ed25519_key.pem', 'r') as f:
        host_ed25519_key = f.read()

    await asyncssh.create_server(MySSHServer, '', 8022, 
                                 server_host_keys=[host_rsa_key, host_ecdsa_key, host_ed25519_key],
                                 process_factory=handle_client)
    
   
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(start_server())
except (OSError, asyncssh.Error) as exc:
    sys.exit(f'Error starting server: {str(exc)}')

loop.run_forever()


