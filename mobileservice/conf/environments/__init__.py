CONFIG_MAP = {
    'prod': 'production',
    'dev': 'development'
}

def get_config(env):
    return '.'.join(['mobileservice', 'conf', 'environments',
                     CONFIG_MAP.get(env, env), 'Config'])
