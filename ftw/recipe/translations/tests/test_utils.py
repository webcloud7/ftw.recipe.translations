from __future__ import print_function
from ftw.recipe.translations import utils
from ftw.recipe.translations.testing import TEMP_DIRECTORY_FIXTURE
from ftw.recipe.translations.utils import find_package_directory
from io import BytesIO
from unittest2 import TestCase
import os
import sys


class TestCaptureStreams(TestCase):

    def test_captures_stdout(self):
        stdout = BytesIO()
        with utils.capture_streams(stdout=stdout):
            print('Foo')
        self.assertEquals('Foo\n', stdout.getvalue())

    def test_captures_stderr(self):
        stderr = BytesIO()
        with utils.capture_streams(stderr=stderr):
            print('Error', file=sys.stderr)
        self.assertEquals('Error\n', stderr.getvalue())

    def test_captures_all_streams_parallel(self):
        stdout = BytesIO()
        stderr = BytesIO()
        with utils.capture_streams(stdout=stdout, stderr=stderr):
            print('Foo')
            print('Bar', file=sys.stderr)
        self.assertEquals('Foo\n', stdout.getvalue())
        self.assertEquals('Bar\n', stderr.getvalue())


class TestFindPackageNamespace(TestCase):

    layer = TEMP_DIRECTORY_FIXTURE

    def setUp(self):
        self.tempdir = self.layer['tempdir']

    def test_find_package_directory(self):
        os.makedirs(os.path.join(self.tempdir, 'foo/bar'))

        directory = find_package_directory(self.tempdir, 'foo.bar', None)
        self.assertEqual(os.path.join(self.tempdir, 'foo/bar'), directory)

    def test_find_package_directory_in_src_folder(self):
        os.makedirs(os.path.join(self.tempdir, 'src/foo/bar'))

        directory = find_package_directory(self.tempdir, 'foo.bar', None)
        self.assertEqual(os.path.join(self.tempdir, 'src/foo/bar'), directory)

    def test_find_package_directory_in_default_namespace_folder(self):
        os.makedirs(os.path.join(self.tempdir, 'src/foo.bar/foo/bar'))

        directory = find_package_directory(self.tempdir, 'foo.bar', None)
        self.assertEqual(os.path.join(self.tempdir, 'src/foo.bar/foo/bar'),
                         directory)

    def test_find_package_directory_in_custom_namespace_folder(self):
        os.makedirs(os.path.join(self.tempdir, 'my/package'))
        directory = find_package_directory(self.tempdir, 'foo.bar', 'my.package')
        self.assertEqual(os.path.join(self.tempdir, 'my/package'), directory)

    def test_package_namespace_has_precedence(self):
        os.makedirs(os.path.join(self.tempdir, 'my/package'))
        directory = find_package_directory(self.tempdir, 'my', 'my.package')
        self.assertEqual(os.path.join(self.tempdir, 'my/package'), directory)
