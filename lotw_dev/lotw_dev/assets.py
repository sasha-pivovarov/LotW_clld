from clldutils.path import Path
from clld.web.assets import environment

import lotw_dev


environment.append_path(
    Path(lotw_dev.__file__).parent.joinpath('static').as_posix(),
    url='/lotw_dev:static/')
environment.load_path = list(reversed(environment.load_path))
