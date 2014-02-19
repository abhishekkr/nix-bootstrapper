#


import logging


INIT_NOVA_AGENT_LOG = "/var/log/init-nova-agent.log"


logging.basicConfig(filename=INIT_NOVA_AGENT_LOG,
                    format='%(asctime)s [%(levelname)s]: %(funcName)s LOG: %(message)s',
                    level=logging.DEBUG)

def log(logger, message, **kwargs):
    if len(kwargs) > 0:
        _info = lambda _key_val: "%s: %s" % _key_val
        _info = map(_info, kwargs.items())
        _info = "\n".join(_info)
        message = "%s\n%s" % (message, _info)

    logger(message)
