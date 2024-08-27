import os
import pytest

import pip

#os.system("pip install "+os.path.dirname(os.path.dirname(__file__)))
pip.main(['install', os.path.dirname(os.path.dirname(__file__))])