def choose_config(app_config):
    base = 'main.configs.' + app_config + '.'
    config_class = app_config.capitalize() + 'Config'
    return base + config_class
