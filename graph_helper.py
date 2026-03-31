import warnings
import urllib3
from requests import sessions

# Disable SSL warnings when verification is disabled
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Monkey patch requests to disable SSL verification for corporate proxy compatibility
original_request = sessions.Session.request

def patched_request(self, method, url, *args, **kwargs):
    kwargs['verify'] = False
    return original_request(self, method, url, *args, **kwargs)

sessions.Session.request = patched_request