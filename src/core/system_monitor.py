import time

class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.data_count = 0
        self.error_count = 0
        
    def update_stats(self, success=True):
        self.data_count += 1
        if not success:
            self.error_count += 1
            
    def get_system_status(self):
        uptime = time.time() - self.start_time
        success_rate = (self.data_count - self.error_count) / self.data_count if self.data_count > 0 else 0
        return {
            'uptime': uptime,
            'data_count': self.data_count,
            'error_count': self.error_count,
            'success_rate': success_rate
        } 