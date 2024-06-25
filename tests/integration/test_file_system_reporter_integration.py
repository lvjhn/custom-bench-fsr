from unittest.mock import Mock, patch, call
import unittest

import uuid 
import datetime
import time

import os 
import shutil

from custom_bench_fsr.reporter import FileSystemReporter 

from custom_bench.benchmarker import Benchmarker 
from custom_bench.context import Context
from custom_bench.unit import Unit

class TestFileSystemIntegration:
    
    #
    # Test that reporter can report benchmarker object. 
    # 
    def test_can_report_benchmarker(self): 
        
        if os.path.exists("./results/Test-Benchmark"):
            shutil.rmtree("./results/Test-Benchmark")

        reporter = FileSystemReporter(
            outdir="./results",
            write_mode="replace"
        )  
        
        benchmarker = Benchmarker(
            name="Test-Benchmark",
            description="Some-Random-Test-Benchmark"
        )

        benchmarker.start()

        for i in range(100):
            j = i ** 5

        benchmarker.end() 

        reporter.report_benchmarker(benchmarker)

        assert(os.path.exists("./results/Test-Benchmark/@benchmark/_results_.txt"))

    #
    # Test that reporter can report context object with items. 
    # 
    def test_can_report_benchmarker(self): 
        
        if os.path.exists("./results/Test-Benchmark"):
            shutil.rmtree("./results/Test-Benchmark")

        reporter = FileSystemReporter(
            outdir="./results",
            write_mode="replace"
        )  
        
        benchmarker = Benchmarker(
            name="Test-Benchmark",
            description="Some-Random-Test-Benchmark"
        )

        benchmarker.start()

        context = benchmarker.context(name=f"test-context")
        context.start() 

        for i in range(100):
            j = i ** 5

        context.end()

        reporter.report_context(context)

        assert(os.path.exists("./results/Test-Benchmark/test-context/_results_.txt"))


        benchmarker.end() 
