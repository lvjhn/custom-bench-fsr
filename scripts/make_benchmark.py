from custom_bench.benchmarker import Benchmarker 
from custom_bench_fsr.reporter import FileSystemReporter

reporter = FileSystemReporter("./results")

benchmarker = Benchmarker(
    name="Demo Benchmark",
    description="Some demo benchmark."
) 

benchmarker.start()

for i in range(10000): 
    print(i)

benchmarker.end() 




