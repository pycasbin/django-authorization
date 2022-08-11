from pathlib import Path

# Dauthz
DAUTHZ = {
    'REQUEST_MIDDLEWARE': {
        'ENFORCER_NAME': 'DEFAULT',
    },
    'ENFORCER_MIDDLEWARE': {
        'ENFORCER_NAME': 'DEFAULT',
    },
    'ENFORCERS': {
        # Default Dauthz enforcer
        'DEFAULT': {
            # Casbin model setting.
            'MODEL': {
                # Available Settings: "file", "text"
                'CONFIG_TYPE': 'file',
                'CONFIG_FILE_PATH': Path(__file__).parent.joinpath('dauthz-model.conf'),
                'CONFIG_TEXT': '',
            },

            # Casbin adapter .
            'ADAPTER': 'casbin_adapter.adapter.Adapter',
            # Database setting.
            'STORAGE': {
                # Available Settings: "database", "file"
                'STORAGE_TYPE': 'database',
                # Database connection for following tables.
                'DATABASE_CONNECTION': '',
                # 'FILE_PATH':
            },

            'LOG': {
                # Changes whether Dauthz will log messages to the Logger.
                'ENABLED': False,
            },

            'CACHE': {

            },
        },
    }
}
