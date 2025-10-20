"""
Webhook service for HeroCal.
Handles sending data to external webhook endpoints.
"""

import json
import logging
import requests
import time
from typing import Dict, Any, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future


class WebhookService:
    """Service for sending data to webhook endpoints"""
    
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.logger = logging.getLogger(__name__)
        self.executor = ThreadPoolExecutor(max_workers=2)
        self._session = requests.Session()
        
        # Set default headers
        self._session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'HeroCal/1.0.0'
        })
    
    def is_enabled(self) -> bool:
        """Check if webhook is enabled"""
        return self.settings_manager.get_setting('webhook.enabled', False)
    
    def get_webhook_url(self) -> Optional[str]:
        """Get the webhook URL from settings"""
        return self.settings_manager.get_setting('webhook.url')
    
    def send_calculation_result(self, module_name: str, inputs: Dict[str, Any], 
                              outputs: Dict[str, Any], execution_time: float) -> Future:
        """Send calculation result to webhook"""
        if not self.is_enabled() or not self.settings_manager.get_setting('webhook.send_calculations', True):
            return None
        
        payload = {
            'event_type': 'calculation_result',
            'timestamp': datetime.utcnow().isoformat(),
            'module_name': module_name,
            'inputs': inputs,
            'outputs': outputs,
            'execution_time': execution_time,
            'application': 'HeroCal',
            'version': '1.0.0'
        }
        
        return self._send_async(payload)
    
    def send_error(self, error_type: str, error_message: str, 
                  module_name: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> Future:
        """Send error information to webhook"""
        if not self.is_enabled() or not self.settings_manager.get_setting('webhook.send_errors', True):
            return None
        
        payload = {
            'event_type': 'error',
            'timestamp': datetime.utcnow().isoformat(),
            'error_type': error_type,
            'error_message': error_message,
            'module_name': module_name,
            'context': context or {},
            'application': 'HeroCal',
            'version': '1.0.0'
        }
        
        return self._send_async(payload)
    
    def send_project_save(self, project_name: str, file_path: str, 
                         project_data: Dict[str, Any]) -> Future:
        """Send project save event to webhook"""
        if not self.is_enabled() or not self.settings_manager.get_setting('webhook.send_project_saves', False):
            return None
        
        payload = {
            'event_type': 'project_save',
            'timestamp': datetime.utcnow().isoformat(),
            'project_name': project_name,
            'file_path': file_path,
            'project_size': len(json.dumps(project_data)),
            'application': 'HeroCal',
            'version': '1.0.0'
        }
        
        return self._send_async(payload)
    
    def send_custom_event(self, event_type: str, data: Dict[str, Any]) -> Future:
        """Send custom event to webhook"""
        if not self.is_enabled():
            return None
        
        payload = {
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data,
            'application': 'HeroCal',
            'version': '1.0.0'
        }
        
        return self._send_async(payload)
    
    def _send_async(self, payload: Dict[str, Any]) -> Future:
        """Send payload to webhook asynchronously"""
        return self.executor.submit(self._send_sync, payload)
    
    def _send_sync(self, payload: Dict[str, Any]) -> bool:
        """Send payload to webhook synchronously"""
        webhook_url = self.get_webhook_url()
        if not webhook_url:
            self.logger.warning("No webhook URL configured")
            return False
        
        timeout = self.settings_manager.get_setting('webhook.timeout', 30)
        retry_attempts = self.settings_manager.get_setting('webhook.retry_attempts', 3)
        
        for attempt in range(retry_attempts):
            try:
                self.logger.debug(f"Sending webhook payload (attempt {attempt + 1}): {payload['event_type']}")
                
                response = self._session.post(
                    webhook_url,
                    json=payload,
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    self.logger.debug(f"Webhook sent successfully: {payload['event_type']}")
                    return True
                else:
                    self.logger.warning(f"Webhook returned status {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                self.logger.warning(f"Webhook timeout (attempt {attempt + 1})")
            except requests.exceptions.ConnectionError:
                self.logger.warning(f"Webhook connection error (attempt {attempt + 1})")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Webhook request error (attempt {attempt + 1}): {e}")
            except Exception as e:
                self.logger.error(f"Unexpected webhook error (attempt {attempt + 1}): {e}")
            
            # Wait before retry (exponential backoff)
            if attempt < retry_attempts - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
        
        self.logger.error(f"Failed to send webhook after {retry_attempts} attempts: {payload['event_type']}")
        return False
    
    def test_webhook(self) -> bool:
        """Test webhook connectivity"""
        test_payload = {
            'event_type': 'test',
            'timestamp': datetime.utcnow().isoformat(),
            'message': 'HeroCal webhook test',
            'application': 'HeroCal',
            'version': '1.0.0'
        }
        
        return self._send_sync(test_payload)
    
    def update_webhook_url(self, new_url: str):
        """Update webhook URL in settings"""
        self.settings_manager.set_setting('webhook.url', new_url)
        self.logger.info(f"Webhook URL updated to: {new_url}")
    
    def shutdown(self):
        """Shutdown webhook service"""
        self.executor.shutdown(wait=True)
        self._session.close()
        self.logger.info("Webhook service shutdown")
