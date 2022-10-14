"""A system for creating pretty class representations.

:copyright: (c) 2022 Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""


__title__ = "prepr"
__author__ = "Tanner B. Corcoran"
__email__ = "tannerbcorcoran@gmail.com"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022 Tanner B. Corcoran"
__version__ = "0.0.1"
__description__ = "A system for creating pretty class representations"
__url__ = "https://github.com/tanrbobanr/prepr"
__download_url__ = "https://pypi.org/project/prepr"


from . import types
from .models import CSHandler, Colorspace, settings, prepr_str
from .main import prepr
