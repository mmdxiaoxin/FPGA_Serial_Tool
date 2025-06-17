from datetime import datetime
from .global_vars import g_vars

class SecurityManager:
    def __init__(self):
        self.access_log = []
        self.operation_log = []
        
    def log_access(self, user, action):
        self.access_log.append({
            'timestamp': datetime.now(),
            'user': user,
            'action': action
        })
        
    def log_operation(self, operation, details):
        self.operation_log.append({
            'timestamp': datetime.now(),
            'operation': operation,
            'details': details
        })
        
    def encrypt_data(self, data):
        return g_vars.cipher_suite.encrypt(str(data).encode())
        
    def decrypt_data(self, encrypted_data):
        return g_vars.cipher_suite.decrypt(encrypted_data).decode() 