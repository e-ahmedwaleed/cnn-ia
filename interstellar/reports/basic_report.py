import reports.writer as w
import reports.constants as c

from verbose.utils import undo_arch_info_capacity_scale


def intro_page(title, body, arch_info):
    pdf = w.PDF()
    pdf.alias_nb_pages()

    """ Title """
    pdf.add_page()
    pdf.set_font('Arial', 'B', c.H1)
    pdf.cell(0, 10, title, 1, 0, 'C')
    pdf.ln(c.INTER_MID_NEW_LINE)
    arch_info = undo_arch_info_capacity_scale(arch_info)
    mem_levels = arch_info['mem_levels']

    # Introduction
    w.introduction(body, pdf)

    ## Memory Architecture
    w.to_mem_arch(arch_info, pdf)

    ## Glossary
    w.glossary(mem_levels, pdf)
    pdf.ln(c.MEDIUM_NEW_LINE)

    return pdf


def generate_basic(map_config, costs, para_index, schedules, arch_info, network_info, schedule_info,
                   output_file="basic_output.pdf"):
    title = "Analyzer Report {Loop Blocking}"
    body = "This report generated by Convolutional Neural Network Inference Analyzer (CNN-IA) " \
           "to summarize the analysis needed to reach the optimal loop blocking in a restricted " \
           "schedule space for " + network_info['layer_name'] + "."

    pdf = intro_page(title, body, arch_info)

    """ Map Configurations """
    pdf.add_page()
    pdf.set_font('Arial', 'B', c.H1)
    pdf.cell(100, 10, "Map Configuration", 1, 1, 'C')
    pdf.ln(c.MEDIUM_NEW_LINE)

    ## loop blocking
    pdf.cell(66, 10, "Loop Blocking (factors):", "B", 0, 'L')
    colored_1 = w.write_loops(map_config.loop_blockings, pdf, list(schedule_info.values())[0])

    ## loop partitioning
    pdf.set_font('Arial', 'B', c.H1)
    pdf.cell(69, 10, "Loop Partitioning (units): ", "B", 0, 'L')
    colored_2 = w.write_loops(map_config.loop_partitionings, pdf, list(schedule_info.values())[0])

    ## loop ordering
    pdf.set_font('Arial', 'B', c.H1)
    pdf.cell(100, 10, "Loop Ordering (from the innermost): ", "B", 0, 'L')
    colored_3 = w.write_loops(map_config.loop_orders, pdf, list(schedule_info.values())[0])
    pdf.set_font('Arial', 'B', c.H4)
    pdf.ln(c.MEDIUM_NEW_LINE)
    if colored_1 or colored_2 or colored_3:
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 5, "(Hinted schedule configurations are in green)", 0, 0, 'R')
        pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', c.H1)

    """ Schedule """
    pdf.add_page()
    pdf.cell(100, 10, "Schedule", 1, 0, 'C')
    pdf.set_font('Arial', '', c.H4)
    pdf.cell(70, 10, "  [b: blocking factor, p: partitioning unit]")
    pdf.ln(c.INTER_MID_NEW_LINE)
    schedule_color = w.write_schedule(schedules, pdf, list(schedule_info.values())[1])
    pdf.set_font('Arial', 'B', c.H4)
    if schedule_color:
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 5, "(Hinted loop unrollments are in green)", 0, 0, 'R')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(c.MEDIUM_NEW_LINE)
    pdf.set_font('Arial', 'B', c.H1)

    """ Cost """
    pdf.cell(100, 10, "Cost", 1, 1, 'C')
    pdf.ln(c.MEDIUM_NEW_LINE)
    pdf.set_font('Arial', 'B', c.H2)
    w.write_cost_levels(costs, para_index, pdf)

    pdf.output(output_file, 'F')
