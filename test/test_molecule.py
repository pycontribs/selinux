# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import fnmatch
import os
import pytest
import subprocess


# detect if we have a working docker setup and skip with warning if not
docker_skip = False
docker_reason = ''
try:
    import docker
    client = docker.from_env(version='auto')
    if not client.ping():
        raise Exception("Failed to ping docker server.")
except Exception as e:
    docker_reason = "Skipping molecule tests due: %s" % e
    docker_skip = True
    raise e


def pytest_generate_tests(metafunc):
    # detects all molecule scenarios inside the project
    matches = []
    if 'testdata' in metafunc.fixturenames:
        for root, dirnames, filenames in os.walk('molecule'):
            for filename in fnmatch.filter(filenames, 'molecule.yml'):
                matches.append(os.path.basename(root))
    metafunc.parametrize('testdata', matches)


@pytest.mark.skipif(docker_skip, reason=docker_reason)
def test_molecule(testdata):
    cmd = ['python', '-m', 'molecule', 'test', '-s', testdata]
    print("running: %s" % " " .join(cmd))
    r = subprocess.call(cmd)
    assert r == 0
