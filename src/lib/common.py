import os
import subprocess
import logging


logger = logging.getLogger('dicthub')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())

APP_VERSION = '0.1.0'
APPINDICATOR_ID = 'dictindicator'
APPINDICATOR_ICON = 'dict-indicator'
ICON_THEM_PATH = '/usr/share/icons/hicolor/scalable/devices'
PACKAGE_DIR = os.path.dirname(__file__)
CONFIG_DIR = os.path.expanduser("~/.config/dicthub")
AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")
SYSTEMD_DIR = '/lib/systemd/system'
SYSTEMD_USER_DIR = '/etc/systemd/system/multi-user.target.wants'
SERVICE_FILENAME = 'dicthub-web.service'
DESKTOP_FILENAME = 'dicthub-indicator.desktop'
WEB_PORT_DEFAULT = 5678
WEB_TEMPLATE_FILEPATH = '%s/data/template.htm' % PACKAGE_DIR
DB_FILEPATH = os.path.join(CONFIG_DIR, 'dicts.db')
DB_SCHEME_FILEPATH = os.path.join(PACKAGE_DIR, 'data', 'dict_scheme.sql')


def check_conf_dir():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)


def shell_exec(cmd):
    try:
        output = subprocess.getoutput(cmd)
    except AttributeError:
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output, error = p.communicate()
        if error != '':
            output = error
    logger.info(cmd)
    if output != '':
        logger.info(output)
    return output
