import os
import sys
from pathlib import Path

# ads 앱이 있는 ad_server 폴더를 검색 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "ad_config.settings"
    execute_from_command_line(sys.argv)