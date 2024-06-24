from unittest.mock import Mock, patch, call
import unittest

import uuid 
import datetime
import time

import os 
import shutil

from custom_bench_fsr.reporter import FileSystemReporter 

class TestFileSystemReporter:
    
    #
    # Test Constructor 
    # 
    def test_constructor(self): 

        original = FileSystemReporter.prepare
        FileSystemReporter.prepare = Mock()

        reporter = FileSystemReporter(
            outdir="./results",
            write_mode="replace"
        )  
        
        assert(reporter.outdir == "./results")
        assert(reporter.write_mode == "replace")

        reporter.prepare.assert_called()

        FileSystemReporter.prepare = original

    #
    # Test .prepare()
    # 
    def test_prepare(self): 
        reporter = FileSystemReporter()

        reporter.prepare_outdir = Mock()

        reporter.prepare()

        reporter.prepare_outdir.assert_called()

    #
    # Test .prepare_outdir()
    # 
    def test_prepare_outdir_replace_mode(self):
        reporter = FileSystemReporter(write_mode="replace")

        reporter.clear_outdir = Mock() 
        reporter.create_outdir = Mock() 

        reporter.prepare_outdir() 

        reporter.clear_outdir.assert_called()
        reporter.create_outdir.assert_called()

    def test_prepare_outdir_merge_mode(self):
        reporter = FileSystemReporter(write_mode="merge")

        reporter.clear_outdir = Mock() 
        reporter.create_outdir = Mock() 

        reporter.prepare_outdir() 

        reporter.clear_outdir.assert_not_called()
        reporter.create_outdir.assert_called()

    #
    # Test .create_outdir() 
    # 

    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_create_outdir_not_exists(self, makedirs, exists):
        exists.return_value = False 
        reporter = FileSystemReporter()
        
        reporter.create_outdir() 

        exists.assert_called_with(reporter.outdir)
        makedirs.assert_called_with(reporter.outdir, exist_ok=True)

    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_create_outdir_exists(self, makedirs, exists):
        exists.return_value = True 
        reporter = FileSystemReporter()
        
        reporter.create_outdir() 

        exists.assert_called_with(reporter.outdir)
        makedirs.assert_not_called()

    #
    # Test .clear_outdir() 
    # 

    @patch("os.path.exists")
    @patch("shutil.rmtree")
    def test_create_outdir_exists(self, rmtree, exists):
        exists.return_value = True 
        reporter = FileSystemReporter()
        
        reporter.clear_outdir() 

        exists.assert_called_with(reporter.outdir)
        rmtree.assert_called_with(reporter.outdir)

    @patch("os.path.exists")
    @patch("shutil.rmtree")
    def test_create_outdir_not_exists(self, rmtree, exists):
        exists.return_value = False 
        reporter = FileSystemReporter()
        
        reporter.clear_outdir() 

        exists.assert_called_with(reporter.outdir)
        rmtree.assert_not_called()