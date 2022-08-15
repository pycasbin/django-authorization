from pathlib import Path

# Dauthz
DAUTHZ = {
    # set default enforcer
    'DEFAULT': 'BASIC',
    # BASIC Dauthz enforcer
    'BASIC': {
        # Casbin model setting.
        'MODEL': {
            # Available Settings: "file", "text"
            'CONFIG_TYPE': 'file',
            'CONFIG_FILE_PATH': Path(__file__).parent.joinpath('dauthz-model.conf'),
            'CONFIG_TEXT': '',
        },

        # Casbin adapter .
        'ADAPTER': {
            'NAME': 'casbin_adapter.adapter.Adapter',
            # 'OPTION_1': '',
        },
        'LOG': {
            # Changes whether Dauthz will log messages to the Logger.
            'ENABLED': False,
        },
        'CACHE': {

        },
    },
}
