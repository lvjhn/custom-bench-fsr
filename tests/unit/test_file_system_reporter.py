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

    @patch("os.makedirs")
    def test_create_outdir_not_exists(self, makedirs):
        reporter = FileSystemReporter()
        reporter.create_outdir() 
        makedirs.assert_called_with(reporter.outdir, exist_ok=True)

    #
    # Test .clear_outdir() 
    # 

    @patch("os.path.exists")
    @patch("shutil.rmtree")
    def test_clear_outdir_exists(self, rmtree, exists):
        exists.return_value = True 
        reporter = FileSystemReporter()
        
        reporter.clear_outdir() 

        exists.assert_called_with(reporter.outdir)
        rmtree.assert_called_with(reporter.outdir)

    @patch("os.path.exists")
    @patch("shutil.rmtree")
    def test_clear_outdir_not_exists(self, rmtree, exists):
        exists.return_value = False 
        reporter = FileSystemReporter()
        
        reporter.clear_outdir() 

        exists.assert_called_with(reporter.outdir)
        rmtree.assert_not_called()

    #
    # Test .report()
    # 
    def test_report(self): 
        reporter = FileSystemReporter() 

        class MockBenchmarker:
            def __init__(self):
                pass 

        class MockContext:
            def __init__(self):
                pass 
            
        class MockUnit:
            def __init__(self): 
                pass 

        reporter = FileSystemReporter(
            Benchmarker = MockBenchmarker,
            Context = MockContext,
            Unit = MockUnit
        )

        reporter.report_benchmarker = Mock()
        mock_benchmarker = MockBenchmarker()

        reporter.report_context = Mock()
        mock_context = MockContext()

        reporter.report_unit = Mock()
        mock_unit = MockUnit()

        reporter.report(mock_benchmarker)
        reporter.report_benchmarker.assert_called_with(mock_benchmarker)

        reporter.report(mock_context)
        reporter.report_context.assert_called_with(mock_context)

        reporter.report(mock_unit)
        reporter.report_unit.assert_called_with(mock_unit)

        try:
            reporter.report(None)
            assert(False)
        except Exception as e: 
            assert("Unknown type" in repr(e))

    #
    # Test .report_benchmark_item()
    # 
    def test_report_benchmark_item(self): 
        reporter = FileSystemReporter() 

        class MockBenchmarkItem:
            def __init__(self):
                self.meta = {
                    "name" : "Some-Benchmarker",
                    "description" : "Some-Benchmarker-Description",
                    "ran_at" : "00/00/00 00:00:00"
                }

                self.summary = {
                    "start"         : 3,
                    "end"           : 12,
                    "skipped"       : 2, 
                    "duration_ns"   : 7,
                    "duration_ws"   : 9
                }

        benchmark_item = MockBenchmarkItem()

        T = reporter.report_benchmark_item(benchmark_item)

        assert("BENCHMARK RESULTS" in T)
        assert("Name" in T)
        assert("Description" in T)
        assert("Ran At" in T)

        assert("3 seconds" in T)
        assert("12 seconds" in T)
        assert("2 seconds" in T)
        assert("7 seconds" in T)
        assert("9 seconds" in T)

    #
    # Test .report_items()
    # 

    def test_report_items(self): 
        reporter = FileSystemReporter()

        class MockContext: 
            def __init__(self, state):
                self.state = state
                

        class MockBenchmarkItem:
            def __init__(self):
                self.has_items = True

                self.state = {
                    "children" : {
                        "n_items" : 3, 
                        "items_summary" : {}, # not involved,
                        "items" : {
                            "Context-1" : MockContext({
                                "meta" : {
                                    "name" : "Context-1", 
                                    "description" : "Some-Random-Context-1"
                                }, 
                                "summary" : {
                                    "start"         : 11234, 
                                    "end"           : 14321, 
                                    "skipped"       : 11111, 
                                    "duration_ns"   : 16789, 
                                    "duration_ws"   : 19876
                                }
                            }),
                            "Context-2" : MockContext({
                                "meta" : {
                                    "name" : "Context-2", 
                                    "description" : "Some-Random-Context-2"
                                }, 
                                "summary" : {
                                    "start"         : 21234, 
                                    "end"           : 24321, 
                                    "skipped"       : 21111, 
                                    "duration_ns"   : 26789, 
                                    "duration_ws"   : 29876
                                }
                            }),
                            "Context-3" : MockContext({
                                "meta" : {
                                    "name" : "Context-3", 
                                    "description" : "Some-Random-Context-3"
                                }, 
                                "summary" : {
                                    "start"         : 31234, 
                                    "end"           : 34321, 
                                    "skipped"       : 31111, 
                                    "duration_ns"   : 36789, 
                                    "duration_ws"   : 39876
                                }
                            })
                        }
                    }
                }

        benchmark_item = MockBenchmarkItem()

        T = reporter.report_items(benchmark_item)

        assert("Item 1 : Context-1" in T)
        assert("Item 2 : Context-2" in T)
        assert("Item 3 : Context-3" in T)

        assert("Some-Random-Context-1" in T)
        assert("Some-Random-Context-2" in T)
        assert("Some-Random-Context-3" in T)

        assert("11234" in T)
        assert("21234" in T)
        assert("31234" in T)
        
        assert("14321" in T)
        assert("24321" in T)
        assert("34321" in T)

        assert("11111" in T)
        assert("21111" in T)
        assert("31111" in T)

        assert("16789" in T)
        assert("26789" in T)
        assert("36789" in T)

        assert("19876" in T)
        assert("29876" in T)
        assert("39876" in T)

    #
    # Test .write_benchmark_file()
    # 
    @patch("builtins.open")
    def test_write_benchmark_file(self, open):
        reporter = FileSystemReporter()
        reporter.write_benchmark_file("OUTFILE", "TEXT") 
        open.assert_called_with("OUTFILE", "w")

    #
    # Test .report_benchmarker()
    # 

    def test_report_benchmarker(self):

        class Benchmarker: 
            def __init__(self):
                self.has_items = True
                self.name = "Test-Benchmarker"


        reporter = FileSystemReporter(Benchmarker=Benchmarker)

        benchmarker = Benchmarker() 

        reporter.report_benchmark_item = Mock(return_value="[SUMMARY]")
        reporter.report_items_summary = Mock(return_value="[ITEMS_SUMMARY]")
        reporter.save_benchmarker_report = Mock()
        reporter.make_plots = Mock()

        T = reporter.report_benchmarker(benchmarker)

        reporter.report_benchmark_item.assert_called_with(benchmarker) 
        reporter.report_items_summary.assert_called_with(benchmarker)
        reporter.save_benchmarker_report.assert_called_with(benchmarker, T)
        reporter.make_plots.assert_called_with(benchmarker)

        assert("[SUMMARY]" in T)
        assert("[ITEMS_SUMMARY]" in T)

    def test_report_benchmarker_with_individual_items(self):
        reporter = FileSystemReporter()

        class Benchmarker: 
            def __init__(self):
                self.has_items = True

        benchmarker = Benchmarker() 

        reporter.report_benchmark_item = Mock(return_value="[SUMMARY]")
        reporter.report_items_summary = Mock(return_value="[ITEMS_SUMMARY]")
        reporter.report_items = Mock(return_value="[ITEMS]")
        reporter.save_benchmarker_report = Mock()
        reporter.make_plots = Mock()

        T = reporter.report_benchmarker(
            benchmarker, report_individual_items=True
        )

        reporter.report_benchmark_item.assert_called_with(benchmarker) 
        reporter.report_items_summary.assert_called_with(benchmarker)
        reporter.save_benchmarker_report.assert_called_with(benchmarker, T)
        reporter.make_plots.assert_called_with(benchmarker)

        assert("[SUMMARY]" in T)
        assert("[ITEMS_SUMMARY]" in T)
        assert("[ITEMS]" in T)

    #
    # Test .prepare_benchmarker_dir()
    #  

    @patch("os.mkdir")
    @patch("custom_bench_fsr.reporter.os.path.exists")
    def test_prepare_benchmarker_dir(self, exists, mkdir):
        exists.return_value = False 

        reporter = FileSystemReporter() 

        class MockBenchmarker: 
            def __init__(self): 
                self.name = "Mock-Benchmarker"

        benchmarker = MockBenchmarker()

        benchmarker_dir = reporter.outdir + "/" + benchmarker.name
        
        O = reporter.prepare_benchmarker_dir(benchmarker)

        mkdir.assert_called_with(benchmarker_dir)
        
        assert(O == benchmarker_dir)

    
    #
    # Test .save_benchmarker_report()
    #

    @patch("os.mkdir")
    def test_save_benchmarker_report(self, mkdir): 
        reporter = FileSystemReporter() 

        class MockBenchmarker: 
            def __init__(self): 
                self.name = "Mock-Benchmarker"

        benchmarker = MockBenchmarker()

        reporter.prepare_benchmarker_dir = \
                Mock(return_value="./results/Mock-Benchmarker") 
        reporter.write_benchmark_file = \
                Mock()

        reporter.save_benchmarker_report(benchmarker, "[RESULT]")

        main_dir  = "./results/Mock-Benchmarker/@benchmark" 
        main_file = main_dir + "/_results_.txt" 

        reporter.prepare_benchmarker_dir.assert_called_with(benchmarker) 
        reporter.write_benchmark_file.assert_called_with(main_file, "[RESULT]")
        mkdir.assert_called_with(main_dir)

    #
    # Test .report_context()
    # 

    def test_report_context(self):
        reporter = FileSystemReporter()

        class Context: 
            def __init__(self):
                self.has_items = True

        context = Context() 

        reporter.report_benchmark_item = Mock(return_value="[SUMMARY]")
        reporter.report_items_summary = Mock(return_value="[ITEMS_SUMMARY]")
        reporter.save_benchmarker_report = Mock()
        reporter.make_plots = Mock()

        T = reporter.report_benchmarker(context)

        reporter.report_benchmark_item.assert_called_with(context) 
        reporter.report_items_summary.assert_called_with(context)
        reporter.save_benchmarker_report.assert_called_with(context, T)
        reporter.make_plots.assert_called_with(context)

        assert("[SUMMARY]" in T)
        assert("[ITEMS_SUMMARY]" in T)

    def test_report_context_with_individual_items(self):
        reporter = FileSystemReporter()

        class Benchmarker: 
            def __init__(self):
                self.has_items = True

        context = Benchmarker() 

        reporter.report_benchmark_item = Mock(return_value="[SUMMARY]")
        reporter.report_items_summary = Mock(return_value="[ITEMS_SUMMARY]")
        reporter.report_items = Mock(return_value="[ITEMS]")
        reporter.save_benchmarker_report = Mock()
        reporter.make_plots = Mock()

        T = reporter.report_benchmarker(
            context, report_individual_items=True
        )

        reporter.report_benchmark_item.assert_called_with(context) 
        reporter.report_items_summary.assert_called_with(context)
        reporter.save_benchmarker_report.assert_called_with(context, T)
        reporter.make_plots.assert_called_with(context)

        assert("[SUMMARY]" in T)
        assert("[ITEMS_SUMMARY]" in T)
        assert("[ITEMS]" in T)

    def test_make_plots(self): 

        class MockBenchmarkItem:
            def __init__(self): 
                self.has_items = True
                self.outdir = "./results"
                self.name   = "Mock-Benchmark-Item" 

            def get_duration_ns_non_outliers(self):
                return

            def get_start(self):
                return

            def get_end(self):
                return

        benchmark_item = MockBenchmarkItem()

        reporter = FileSystemReporter(
            Context = MockBenchmarkItem
        )

        reporter.resolve_names = \
            Mock(return_value=("[MOCK-NAME]", "[MOCK-SUBNAME]")) 

        benchmark_item.get_duration_ns_non_outliers = \
            Mock(return_value="[DURATION_NS]")
        benchmark_item.get_start = \
            Mock(return_value="[START_TIMES]") 
        benchmark_item.get_end = \
            Mock(return_value="[END_TIMES]") 

        reporter.make_histogram = Mock()
        reporter.make_lines = Mock()
        reporter.make_average_plot = Mock()

        reporter.make_plots(benchmark_item)

        reporter.make_histogram.assert_called_with(
            "[DURATION_NS]",
            "Histogram : Duration (Without Skipped)", 
            "Duration",
            "Frequency", 
            "./results/[MOCK-NAME]/[MOCK-SUBNAME]/" 
        )

        reporter.make_lines.assert_called_with(
            "[START_TIMES]",
            "[END_TIMES]",
            "Start Time - End Time", 
            "Item",
            "Time", 
            "./results/[MOCK-NAME]/[MOCK-SUBNAME]/" 
        )

        reporter.make_average_plot.assert_called_with(
            "[DURATION_NS]",
            "Average Plot : Duration (Without Skipped)", 
            "Item",
            "Time", 
            "./results/[MOCK-NAME]/[MOCK-SUBNAME]/" 
        )

    def test_resolve_names(self): 

        class MockContext:
            def __init__(self): 
                self.name = "Mock-Context"
                self.benchmarker = None

        class MockBenchmarker:
            def __init__(self):
                self.name = "Mock-Benchmarker"

        benchmarker = MockBenchmarker()
        
        context = MockContext()
        context.benchmarker = benchmarker


        reporter = FileSystemReporter(
            Benchmarker = MockBenchmarker,
            Context = MockContext
        )

        name, subname = reporter.resolve_names(benchmarker)
        assert(name == "Mock-Benchmarker")
        assert(subname == "@benchmark")

        name, subname = reporter.resolve_names(context)
        assert(name == "Mock-Benchmarker")
        assert(subname == "Mock-Context")