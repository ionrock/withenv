import time
import subprocess
import tempfile
import signal


class TestMain(object):

    def test_we_return_code(self):
        assert subprocess.check_output('which we'.split()) != ""
        assert subprocess.check_output('which echo'.split()) != ""
        assert subprocess.call('we echo'.split()) == 0
        assert subprocess.call('we eccho'.split()) == 127

    def test_we_catches_ctrl_c(self):
        fd, path = tempfile.mkstemp()
        with open(path, 'wb+') as fh:
            proc = subprocess.Popen(['we', 'sleep', '10'],
                                    stdout=fh,
                                    stderr=subprocess.STDOUT)
            time.sleep(.5)
            proc.send_signal(signal.SIGINT)
            proc.wait()

        assert open(path).read() == ''
