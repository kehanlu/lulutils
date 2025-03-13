import subprocess
import time
import logging
import argparse
from datetime import datetime
import requests


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Telegram bot for GPU monitoring')
    parser.add_argument('--name', "-n", type=str, default="GPU server", help='Name of the server')
    parser.add_argument('--interval', type=int, default=1800, help='Check interval in seconds')
    parser.add_argument('--chat_id', type=str, help='Telegram chat ID', required=True)
    parser.add_argument('--token', type=str, help='Telegram bot token', required=True)
    return parser.parse_args()


class GPUMonitorBot:
    def __init__(self, args):
        # Configure logging
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
        
        # Store arguments
        self.args = args
        
        # Set up the Telegram API URL
        self.api_url = f"https://api.telegram.org/bot{self.args.token}/sendMessage"

    def get_gpu_status(self):
        """Get GPU status using nvidia-smi command"""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=index,utilization.gpu,memory.used,memory.total,temperature.gpu', '--format=csv,noheader,nounits'],
                capture_output=True, text=True, check=True
            )
            
            gpu_info = []
            for line in result.stdout.strip().split('\n'):
                index, util, mem_used, mem_total, temp = line.split(',')
                gpu_info.append({
                    'index': int(index),
                    'utilization': float(util),
                    'memory_used': float(mem_used),
                    'memory_total': float(mem_total),
                    'temperature': float(temp)
                })
            return gpu_info
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running nvidia-smi: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None

    def is_gpu_idle(self, gpu_info, utilization_threshold=30, memory_threshold_percent=30):
        """Check if GPU is considered idle based on utilization and memory usage"""
        return (gpu_info['utilization'] <= utilization_threshold and
                (gpu_info['memory_used'] / gpu_info['memory_total'] * 100) <= memory_threshold_percent)

    def format_status_message(self, gpu_list):
        """Format status message for all GPUs"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # larger text for name
        message = f"<b>GPU server: {self.args.name}</b>\n"
        
        # sort by index
        gpu_list.sort(key=lambda x: x['index'])
        for gpu in gpu_list:
            message += f"{'🟢' if self.is_gpu_idle(gpu) else '🔴'} "
        message += f"\n{current_time}"
        
        return message

    def send_telegram_message(self, message):
        """Send message using Telegram API"""
        try:
            params = {
                'chat_id': self.args.chat_id,
                'text': message,
                'disable_notification': True,
                'parse_mode': 'HTML'
            }
            response = requests.get(self.api_url, params=params)
            if response.status_code == 200:
                self.logger.info("Message sent successfully")
            else:
                self.logger.error(f"Failed to send message: {response.text}")
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")

    def check_and_notify(self):
        """Check all GPUs and send notification if any GPU is idle"""
        gpu_status = self.get_gpu_status()
        
        if gpu_status is None:
            self.logger.error("Failed to get GPU status")
            return
        
        # Check if at least one GPU is idle
        if any(self.is_gpu_idle(gpu) for gpu in gpu_status):
            message = self.format_status_message(gpu_status)
            self.send_telegram_message(message)

    def run(self):
        """Main method to run the bot"""
        self.logger.info(f"GPU monitoring started for {self.args.name}!")
        
        while True:
            try:
                self.check_and_notify()
                time.sleep(self.args.interval)
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                time.sleep(self.args.interval)


if __name__ == '__main__':
    # Parse command line arguments separately
    args = parse_args()
    
    # Initialize and run the bot with the parsed arguments
    bot = GPUMonitorBot(args)
    bot.run()