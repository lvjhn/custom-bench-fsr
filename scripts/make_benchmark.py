from custom_bench.benchmarker import Benchmarker 
from custom_bench_fsr.reporter import FileSystemReporter

import json

reporter = FileSystemReporter(
    outdir="./results",
    write_mode="replace",
)

benchmarker = Benchmarker(
    name="Demo Benchmark",
    description="Some demo benchmark.",
    has_items=True
) 

benchmarker.start()

context = benchmarker.context(
    name="context-a", 
    description="Context A Results",
    has_items=True
)
context.start()
for i in range(1000): 
    unit = context.unit(name=f"unit-{i}")
    unit.start()
    o = i + 1
    unit.end()
context.end()
reporter.report(context)

context = benchmarker.context(
    name="context-b", 
    description="Context B Results",
    has_items=True
)
context.start()
for i in range(100): 
    unit = context.unit(name=f"unit-{i}")
    unit.start()
    for k in range(i):
        for j in range(i * int(k)):
            o = i * j * k
    unit.end()
context.end()
reporter.report(context)

benchmarker.end() 
reporter.report(benchmarker)

# print(reporter.report_outliers(benchmarker.state["children"]["items_summary"]["outliers_info"]))


