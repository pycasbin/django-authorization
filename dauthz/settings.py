from pathlib import Path
# Dauthz
DAUTHZ = {
    # Default Dauthz enforcer
    'DEFAULT' : {
        # Casbin model setting.
        'MODEL' : {
            # Available Settings: "file", "text"
            'CONFIG_TYPE' : 'file',
            'CONFIG_FILE_PATH' :  Path(__file__).parent.joinpath('dauthz-model.conf'),
            'CONFIG_TEXT' : '',
        },

        # Casbin adapter .
        'ADAPTER' : 'casbin_adapter.adapter.Adapter',
        # Database setting.
        'DATABASE' : {
            # Database connection for following tables.
            'CONNECTION' : '',
        },

        'LOG' : {
            # Changes whether Dauthz will log messages to the Logger.
            'ENABLED' : False,
        },

        'CACHE' : {
            
        },
    },
}