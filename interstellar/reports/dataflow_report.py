import reports.writer as w
import reports.constants as c

from reports.basic_report import intro_page
from verbose.dataflow import find_best_schedules
from verbose.utils import identify_loops_in_brackets_str


def print_tables(pdf, key, loop):
    s = identify_loops_in_brackets_str(key)
    size = len(s)
    pdf.cell(4 * size, 10, s, 1, 0, 'C')
    cost_utilization = "[cost: " + str(loop[0]) + "pJ, utilization: " + str(loop[1]) + "%]"
    pdf.set_font('Arial', '', c.H4)
    pdf.cell(size, 10, border=0, ln=0)
    pdf.cell(70, 10, cost_utilization, 0, 0, 'L')
    pdf.ln(c.LARGE_NEW_LINE)
    pdf.set_font('Arial', 'B', c.H1)

    ## loop blocking
    pdf.cell(66, 10, "Loop Blocking (factors):", "B", 0, 'L')
    w.write_loops(loop[2].loop_blockings, pdf)

    ## loop partitioning
    pdf.set_font('Arial', 'B', c.H1)
    pdf.cell(69, 10, "Loop Partitioning (units): ", "B", 0, 'L')
    w.write_loops(loop[2].loop_partitionings, pdf)

    ## loop ordering
    pdf.set_font('Arial', 'B', c.H1)
    pdf.cell(100, 10, "Loop Ordering (from the innermost): ", "B", 0, 'L')
    w.write_loops(loop[2].loop_orders, pdf)


def write_optimality(pdf, loop_nest, dataflow_tb, title, best, note=False):
    pdf.cell(60, 10, title, 1, 0, 'C')
    if note:
        pdf.set_font('Arial', '', c.H4)
        pdf.cell(70, 10, "  [b: blocking factor, p: partitioning unit]")
    pdf.ln(c.INTER_MID_NEW_LINE)
    w.write_schedule(loop_nest(dataflow_tb[best][2]), pdf)
    pdf.ln(c.SMALL_NEW_LINE)


def write_best_cost_utilization(loop_nest, dataflow_tb, pdf):
    best_cost, best_util = find_best_schedules(dataflow_tb)

    if best_cost != best_util:
        write_optimality(pdf, loop_nest, dataflow_tb, "Optimal cost", best_cost, True)
        write_optimality(pdf, loop_nest, dataflow_tb, "Optimal utilization", best_util)
    else:
        write_optimality(pdf, loop_nest, dataflow_tb, "Optimal schedule", best_util, True)


def generate(loop_nest, dataflow_tb, arch_info, network_info, output_file="dataflow_output.pdf"):
    title = "Analyzer Report {Dataflow}"
    body = "This report generated by Convolutional Neural Network Inference Analyzer (CNN-IA) " + \
           "to summarize the analysis needed to reach the optimal of common energy-efficient " + \
           "dataflows for " + network_info['layer_name'] + "."

    pdf = intro_page(title, body, arch_info)

    """ Dataflow Table """
    pdf.add_page()
    for key, value in dataflow_tb.items():
        print_tables(pdf, key, value)
        pdf.add_page()

    write_best_cost_utilization(loop_nest, dataflow_tb, pdf)

    pdf.output(output_file, 'F')