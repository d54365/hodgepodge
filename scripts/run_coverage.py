import os
import sys

import coverage
from django.core.management import execute_from_command_line

cov = coverage.Coverage()
cov.start()

os.environ["DJANGO_SETTINGS_MODULE"] = "hodgepodge.settings"

try:
    execute_from_command_line(["manage.py", "test"])
    exit_code = 0
except SystemExit as e:
    exit_code = e.code

cov.stop()
cov.save()

cov.report()

threshold = 90
coverage_percentage = cov.report()
if coverage_percentage < threshold:
    print(f"ERROR: Coverage is below {threshold}% (actual: {coverage_percentage}%)")
    sys.exit(1)

sys.exit(exit_code)
