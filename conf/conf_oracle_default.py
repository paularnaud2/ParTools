# yapf: disable

conf = {
    # Expected format:
    # 'DB_NAME': 'USER/PWD@HOST:PORT/SERVICE_NAME',
    # Or
    # ('DB_NAME', 'ENV_NAME'): 'USER/PWD@HOST:PORT/SERVICE_NAME',
    # Note that ENV_NAME can be defined to differentiate between two DB of same
    # name but of different environment.

    'XE': 'USERNAME/PWD@localhost:1521/XE',
    ('XE', 'LOCAL'): 'USERNAME/PWD@localhost:1521/XE',
}
