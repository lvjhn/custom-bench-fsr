import shutil
import os

from custom_bench.benchmarker import Benchmarker 
from custom_bench.context import Context
from custom_bench.unit import Unit

import numpy as np 

import matplotlib.pyplot as plt

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
        os.makedirs(self.outdir, exist_ok=True)

    def clear_outdir(self): 
        """
            Clears output directory. 
        """
        if os.path.exists(self.outdir): 
            shutil.rmtree(self.outdir)

    def report(self, benchmark_item, **kwargs):
      
        if type(benchmark_item) == self.Benchmarker:
            self.report_benchmarker(benchmark_item, **kwargs)
        elif type(benchmark_item) == self.Context:
            self.report_context(benchmark_item, **kwargs) 
        elif type(benchmark_item) == self.Unit:
            self.report_unit(benchmark_item, **kwargs) 
        else: 
            raise Exception("Unknown type.")

    def report_benchmark_item(self, benchmark_item):
        meta    = benchmark_item.meta
        summary = benchmark_item.summary

        T  = f"BENCHMARK RESULTS\n"
        T += "========================================================\n"
        T += f"Name            : {meta['name']}\n" 
        T += f"Description     : {meta['description']}\n"
        T += f"Ran At          : {meta['ran_at']}\n"
        T += f"-------------------------------------------------------\n"
        T += f"Summary\n"
        T += f"    | Start                   : {summary['start']} seconds\n"
        T += f"    | End                     : {summary['end']} seconds\n"
        T += f"    | Skipped                 : {summary['skipped']} seconds\n"
        T += f"    | Duration (w.o. Skipped) : {summary['duration_ns']} seconds\n"
        T += f"    | Duration (w. Skipped)   : {summary['duration_ws']} seconds\n" 
        T += f"-------------------------------------------------------\n"

        return T

    def report_items(self, benchmark_item): 
        if not benchmark_item.has_items:
            return ""

        T = ""
        T  = f"Items\n"
        T += f"-------------------------------------------------------\n" 
        items = benchmark_item.state["children"]["items"]
        i = 0
        for item in items:
            item_obj = items[item] 
            meta = item_obj.state["meta"]
            summary = item_obj.state["summary"]
            T += f"    Item {i + 1} : {meta['name']}\n"
            T += f"         | Description   : {meta['description']}\n"
            T += f"         | Start         : {summary['start']} seconds\n"
            T += f"         | End           : {summary['end']} seconds\n"
            T += f"         | Skipped       : {summary['skipped']} seconds\n"
            T += f"         | Duration (NS) : {summary['duration_ns']} seconds\n"
            T += f"         | Duration (WS) : {summary['duration_ws']} seconds\n"
            i += 1
        T += f"-------------------------------------------------------\n" 
        T += "\n"
        return T

    def report_part(self, part, indent="\t"):
        T  = ""
        T += f"{indent}| Mean           : {part['mean']} seconds\n"
        T += f"{indent}| Mode Value     : {part['mode_val']} seconds\n"
        T += f"{indent}| Mode Count     : {part['mode_count']} items\n"
        T += f"{indent}| Median         : {part['median']} seconds\n"
        T += f"{indent}| Variance       : {part['variance']} seconds\n"
        T += f"{indent}| Std. Dev.      : {part['std_dev']} seconds\n"
        T += f"{indent}| Coef. Var.     : {part['coef_var']}\n"
        T += f"{indent}| Skewness       : {part['skewness']}\n"
        T += f"{indent}| Kurtosis       : {part['kurtosis']}\n"
        T += f"{indent}| Percentiles\n"
        T += f"{indent}    | %1     : {part['percentile_1']}\n"
        T += f"{indent}    | %5     : {part['percentile_5']}\n"
        T += f"{indent}    | %10    : {part['percentile_10']}\n"
        T += f"{indent}    | %20    : {part['percentile_20']}\n"
        T += f"{indent}    | %25    : {part['percentile_25']}\n"
        T += f"{indent}    | %50    : {part['percentile_50']}\n"
        T += f"{indent}    | %75    : {part['percentile_75']}\n"
        T += f"{indent}    | %80    : {part['percentile_80']}\n"
        T += f"{indent}    | %90    : {part['percentile_90']}\n"
        T += f"{indent}    | %95    : {part['percentile_95']}\n"
        T += f"{indent}    | %99    : {part['percentile_99']}\n"
        T += f"{indent}| Normality\n"
        T += f"{indent}    | Shapiro-Wilk         : {part['normality_sw']}\n"
        T += f"{indent}    | Kolmogorov-Smirnov   : {part['normality_ks']}\n"
        T += f"{indent}    | Anderson-Darling     : {part['normality_ad']}\n"
        T += f"{indent}| Stationarity\n"
        T += f"{indent}    | Aug. Dickey-Fuller    : {part['stationarity_adf']}\n"
        T += f"{indent}    | KPSS                  : {part['stationarity_kpss']}\n"

        return T

    def report_outliers(self, outliers, indent="\t"):
        T  = ""
        T += f"{indent}| Threshold      : {outliers['thres']}\n"
        T += f"{indent}| Lower Bound    : {outliers['lb']}\n"
        T += f"{indent}| Upper Bound    : {outliers['ub']}\n"
        T += f"{indent}| Counts\n"
        T += f"{indent}    | Below Lower Bound : {outliers['qty_below_lb']}\n"
        T += f"{indent}    | Above Upper Bound : {outliers['qty_above_ub']}\n"
        T += f"{indent}    | Total             : {outliers['n_outliers']}\n"
        T += f"{indent}| Proportion to Total Items\n"
        T += f"{indent}    | Below Lower Bound : {outliers['b_lb_perc_total']}\n"
        T += f"{indent}    | Above Upper Bound : {outliers['a_ub_perc_total']}\n"
        T += f"{indent}    | Both              : {outliers['both_perc_total']}\n"
        T += f"{indent}| Proportion to Outliers\n"
        T += f"{indent}    | Below Lower Bound : {outliers['b_lb_perc_outlier']}\n"
        T += f"{indent}    | Above Upper Bound : {outliers['a_ub_perc_outlier']}\n"
        T += f"{indent}| Proportion to Non-Outliers\n"
        T += f"{indent}    | Below Lower Bound : {outliers['b_lb_perc_non_outlier']}\n"
        T += f"{indent}    | Above Upper Bound : {outliers['a_ub_perc_non_outlier']}\n"
        T += f"{indent}    | Both              : {outliers['outlier_perc_non_outlier']}\n"

        return T

    def report_items_summary(self, benchmark_item):
        if not benchmark_item.has_items: 
            return ""

        items_summary = \
            benchmark_item.state["children"]["items_summary"]
        
        with_outliers = items_summary["with_outliers"]
        outliers_info = items_summary["outliers_info"]
        no_outliers = items_summary["no_outliers"]

        T  = "" 
        T += f"Items Summary\n"
        T += f"\t| No. of Items\n"
        T += f"\t\t| {benchmark_item.state['children']['n_items']}\n"
        T += f"\t| With Outliers\n"
        T += self.report_part(with_outliers, "\t\t")
        T += f"\t| Outliers Info\n"
        T += self.report_outliers(outliers_info, "\t\t")
        T += f"\t| No Outliers\n"
        T += self.report_part(no_outliers, "\t\t")
        T += "\n"

        return T

    def write_benchmark_file(self, outfile, T):
        open(outfile, "w").write(T) 

    #
    # BENCHMAKER REPORTER
    # 
    
    def report_benchmarker(self, benchmarker, **kwargs):
        T = "" 
        T += self.report_benchmark_item(benchmarker)
        T += self.report_items_summary(benchmarker)
        if kwargs.get("report_individual_items", False):
            T += self.report_items(benchmarker)
        self.save_benchmarker_report(benchmarker, T)
        self.make_plots(benchmarker)
        return T

    def prepare_benchmarker_dir(self, benchmarker):
        base_dir = self.outdir 
        benchmarker_dir = base_dir + "/" + benchmarker.name
        if not os.path.exists(benchmarker_dir):
            os.mkdir(benchmarker_dir)
        return benchmarker_dir

    def save_benchmarker_report(self, benchmarker, T):
        benchmarker_dir = self.prepare_benchmarker_dir(benchmarker)
        
        main_dir = benchmarker_dir + "/@benchmark" 
        os.mkdir(main_dir)

        self.write_benchmark_file(main_dir + "/_results_.txt" , T)
    
    #
    # CONTEXT REPORTER
    # 

    def report_context(self, context, **kwargs): 
        T = "" 
        T += self.report_benchmark_item(context)
        T += self.report_items_summary(context)
        if kwargs.get("report_individual_items", False):
            T += self.report_items(context)
        self.save_context_report(context, T)
        self.make_plots(context)
        return T

    def save_context_report(self, context, T):
        benchmarker_dir = self.prepare_benchmarker_dir(context.benchmarker)
        
        main_dir = benchmarker_dir + "/" + context.name 
        os.mkdir(main_dir)

        self.write_benchmark_file(main_dir + "/_results_.txt" , T)

    #
    # PLots 
    #
    # 1) Histogram of Durations (NS/WS)
    # 2) Line Chart of Start and End Time
    # 3) Averages
    #

    def make_plots(self, benchmark_item):
        if not benchmark_item.has_items:    
            return 

        outdir = self.outdir 
        base_name, subname = self.resolve_names(benchmark_item)
        base_dir = self.outdir + "/" + base_name + "/" + subname + "/"

        duration_ns = benchmark_item.get_duration_ns_non_outliers(benchmark_item)
        start       = benchmark_item.get_start(benchmark_item)
        end         = benchmark_item.get_end(benchmark_item)

        self.make_histogram(
            duration_ns, 
            "Histogram : Duration (Without Skipped)",
            "Duration", 
            "Frequency", 
            base_dir
        )

        self.make_lines(
            start, 
            end,
            "Start Time - End Time",
            "Item", 
            "Time", 
            base_dir
        )

        self.make_average_plot(
            duration_ns, 
            "Average Plot : Duration (Without Skipped)",
            "Item", 
            "Time", 
            base_dir
        )

    def make_histogram(self, items, title, x_axis, y_axis, base_dir): 
        plt.figure()
        plt.title(title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.hist(items)
        plt.savefig(base_dir + "/" + title + ".png")

    def make_lines(self, start, end, title, x_axis, y_axis, base_dir): 
        plt.figure()
        plt.title(title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.plot(start, label="start")
        plt.plot(end, label="end")
        plt.savefig(base_dir + "/" + title + ".png")

    def make_average_plot(self, items, title, x_axis, y_axis, base_dir): 
        if len(items) <= 0: 
            open(base_dir + "/" + title, "w").write("Plot Not Available")

        ave = sum(items) / len(items)
        std = []

        total = 0
        averages = [] 
        for i in range(len(items)):
            total += items[i]
            averages.append(total / (i + 1))
            std.append(np.std(items[:(i + 1)]))

        fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(12, 8))
        fig.tight_layout(pad=5.0)

        plt.title(title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)

        ax0.set_title("Plot of Cumulative Average")
        ax0.plot(averages, label="average")
        ax0.plot([ave for i in range(len(items))], label="start")

        ax1.set_title("Raw Item Durations")
        ax1.bar(range(len(items)), items)

        ax2.set_title("Std. Dev. over Increasing No. of Items")
        ax2.plot(std)

        plt.savefig(base_dir + "/" + title + ".png")

    def resolve_names(self, benchmark_item):
        base_name = None 
        subname = None 

        if type(benchmark_item) is self.Benchmarker:
            base_name = benchmark_item.name 
            subname = "@benchmark"
        elif type(benchmark_item) is self.Context:
            base_name = benchmark_item.benchmarker.name 
            subname = benchmark_item.name
        else:
            raise Exception("Unknown benchmark_item type.")
        
        return base_name, subname
        