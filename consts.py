import os

VERSION = "v0.1"

PORT = 8000

ROOT_DIR = str(os.path.dirname(os.path.realpath(__file__))) + "/root_dir"
TEMPLATES_DIR = str(os.path.dirname(os.path.realpath(__file__))) + "/templates"
IMAGES_DIR = str(os.path.dirname(os.path.realpath(__file__))) + "/images"
OFFLINE_ICON_PATH = IMAGES_DIR + "/offline_icon.png"
ONLINE_ICON_PATH = IMAGES_DIR + "/online_icon.png"
