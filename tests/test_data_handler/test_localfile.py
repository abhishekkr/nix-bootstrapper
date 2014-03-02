# ./data_handler/provider/local_file

from data_handler.provider import local_file

import tests.fakers

from nose.tools import assert_equal
import mox
import fake_filesystem

filesystem = fake_filesystem.FakeFilesystem()
local_file.os = fake_filesystem.FakeOsModule(filesystem)
local_file.open = fake_filesystem.FakeFileOpen(filesystem)


class TestLocalFile(object):

    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""
        klass.test_file_path = "/test/file"
        klass.test_file_data = "{hostname': 'abc', 'password': 'verystrong'}"
        filesystem.CreateFile(klass.test_file_path,
                              contents=klass.test_file_data)

        klass._fakeparser = tests.fakers.FakeParser()
        klass._local_file = local_file.LocalFile(parser=klass._fakeparser,
                                                 filepath=klass.test_file_path)

    def setUp(self):
        self.m = mox.Mox()
        self.m.StubOutWithMock(self._local_file, 'parse')
        self._local_file.parse(self.test_file_data).AndReturn({"hostname": "abc"})
        self.m.ReplayAll()

    def tearDown(self):
        self.m.VerifyAll()
        self.m.UnsetStubs()

    def test__get_value_for(self):
        assert_equal(self._local_file._get_value_for("hostname"), "abc")

    def test_get_value_for(self):
        assert_equal(self._local_file._get_value_for("hostname"), "abc")
