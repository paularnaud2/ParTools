conf = {
    # Expected format:
    # ('ENV_NAME', 'DB_NAME'): 'USER/PWD@HOST:PORT/SERVICE_NAME',
    # Note that ENV_NAME doesn't play any role in the connexion string,
    # it is here to differentiate two DB of same name but of different env
    ('LOCAL', 'XE'):

    'PAUL/paul@localhost:1521/XE',
}
