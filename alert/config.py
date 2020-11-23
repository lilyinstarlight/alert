import json as _json
import logging as _logging
import os as _os
import os.path as _path
import sys as _sys

import fooster.web as _web


# address to listen on
addr = ('', 8000)

# log locations
log = '/var/log/alert/alert.log'
http_log = '/var/log/alert/http.log'

# template directory to use
template = _path.dirname(__file__) + '/html'

# source and destination number
source = '+18001234567'
number = '+18005555555'

# account or key details
auth = ('AC0123456789abcdef0123456789abcdef', '0123456789abcdef0123456789abcdef')


# store config in env var
def _store():
    config = {key: val for key, val in globals().items() if not key.startswith('_')}

    _os.environ['ALERT_CONFIG'] = _json.dumps(config)


# load config from env var
def _load():
    config = _json.loads(_os.environ['ALERT_CONFIG'])

    globals().update(config)

    # automatically apply
    _apply()


# apply special config-specific logic after changes
def _apply():
    # setup logging
    if log:
        _logging.getLogger('alert').addHandler(_logging.FileHandler(log))
    else:
        _logging.getLogger('alert').addHandler(_logging.StreamHandler(_sys.stdout))

    _logging.getLogger('alert').setLevel(_logging.INFO)

    if http_log:
        http_log_handler = _logging.FileHandler(http_log)
        http_log_handler.setFormatter(_web.HTTPLogFormatter())

        _logging.getLogger('http').addHandler(http_log_handler)

    # automatically store if not already serialized
    if 'ALERT_CONFIG' not in _os.environ:
        _store()


# load if config already serialized in env var
if 'ALERT_CONFIG' in _os.environ:
    _load()
