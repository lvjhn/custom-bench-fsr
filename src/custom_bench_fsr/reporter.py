import shutil
import os

from custom_bench.benchmarker import Benchmarker 
from custom_bench.context import Context
from custom_bench.unit import Unit

class FileSystemReporter:
    """
        Basic FileSystemReporter object. 
    """ 

    def __init__(self, **kwargs): 
        """
            Creates a basic FileSystemReporter object. 
        """

        # output directory
        self.outdir = kwargs.get("outdir", "./results") 

        # merge or replace
        self.write_mode = kwargs.get("write_mode", "merge") 

        # dependencies 
        self.Benchmarker = kwargs.get("Benchmarker", Benchmarker)
        self.Context = kwargs.get("Context", Context) 
        self.Unit = kwargs.get("Unit", Unit)

        self.prepare() 

    def prepare(self):
        """ 
            Prepate reporter.
        """ 
        self.prepare_outdir()

    def prepare_outdir(self): 
        """ 
            Prepare output directory.
        """ 
        if self.write_mode == "replace":
            self.clear_outdir() 
            self.create_outdir() 
        elif self.write_mode == "merge":
            self.create_outdir()
        else: 
            raise Exception(f"Unknown write mode `{self.write_mode}`")

    def create_outdir(self):
        """
            Creates output directory.
        """
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir, exist_ok=True)

    def clear_outdir(self): 
        """
            Clears output directory. 
        """
        if os.path.exists(self.outdir): 
            shutil.rmtree(self.outdir)

    def report(self, benchmark_item):
        if type(benchmark_item) == self.Benchmarker:
            self.report_benchmarker(benchmark_item)
        elif type(benchmark_item) == self.Context:
            self.report_context(benchmark_item) 
        elif type(benchmark_item) == self.Unit:
            self.report_unit(benchmark_item) 
        else: 
            raise Exception("Unknown type.")