from custom_bench.benchmarker import Benchmarker 
from custom_bench_fsr.reporter import FileSystemReporter

reporter = FileSystemReporter(
    outdir="./results",
    write_mode="replace"
)

benchmarker = Benchmarker(
    name="Demo Benchmark",
    description="Some demo benchmark.",
    has_items=False
) 

benchmarker.start()

for i in range(10000): 
    print(i)

benchmarker.end() 




