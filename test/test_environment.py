# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

from asv import config
from asv import environment
from asv import util


def test_matrix_environments(tmpdir):
    try:
        util.which('python2.7')
    except RuntimeError:
        raise RuntimeError(
            "python 2.7 must be installed for this test to pass")

    try:
        util.which('python3.3')
    except RuntimeError:
        raise RuntimeError(
            "python 3.3 must be installed for this test to pass")

    conf = config.Config()

    conf.env_dir = six.text_type(tmpdir.join("env"))

    conf.pythons = ["2.7", "3.3"]
    conf.matrix = {
        "six": ["1.4", None],
        "psutil": ["1.2", "1.1"]
    }

    environments = list(environment.get_environments(conf))

    assert len(environments) == 2 * 2 * 2

    # Only test the first two environments, since this is so time
    # consuming
    for env in environments[:2]:
        env.setup()
        env.install_requirements()

        output = env.run(
            ['-c', 'import six, sys; sys.stdout.write(six.__version__)'])
        if env._requirements['six'] is not None:
            assert output.startswith(six.text_type(env._requirements['six']))

        output = env.run(
            ['-c', 'import psutil, sys; sys.stdout.write(psutil.__version__)'])
        assert output.startswith(six.text_type(env._requirements['psutil']))
