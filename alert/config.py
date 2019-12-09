# address to listen on
addr = ('', 8000)

# log locations
log = '/var/log/alert/alert.log'
http_log = '/var/log/alert/http.log'

# template directory to use
import os.path
template = os.path.dirname(__file__) + '/html'

# source and destination number
source = '+18001234567'
number = '+18005555555'

# account or key details
auth = ('AC0123456789abcdef0123456789abcdef', '0123456789abcdef0123456789abcdef')
