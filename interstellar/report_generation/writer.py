# pip install fpdf
from fpdf import FPDF
from datetime import date
from verbose.utils import identify_loops_in_list_of_lists
import report_generation.constants as c


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', c.h4)
        # project name at the left of header
        self.cell(30, 10, 'CNN-EIA', 0, 0, 'L')
        # the current date
        self.cell(0, 10, str(date.today()), 0, 0, 'R')
        if self.page_no() != 1:
            self.line(10, 20, 200, 20)
        self.ln(c.meduim_new_line)
        self.ln(c.small_new_line)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def write_loops(values, pdf):
    loops = ["MEM", "FX", "FY", "OX", "OY", "OC", "IC", "ON"]  # write names of the seven loops
    pdf.set_font('Arial', 'B', c.h4)
    pdf.ln(c.meduim_new_line)
    # write first row headers
    pdf.cell(c.width_margin, c.height_margin, loops[0], align='C')
    for cell_index in range(0, len(values[0])):
        pdf.cell(c.width_margin, c.height_margin, "L" + str(cell_index), align='C')
    pdf.ln(c.small_new_line)

    # write the type of loop (FX,FY..etc) with its values
    for block_index, block in enumerate(values):
        pdf.set_font('Arial', 'B', c.h4)  # for headers
        pdf.cell(c.width_margin, c.height_margin, loops[block_index + 1], align='C')
        pdf.set_font('Arial', '', c.h4)  # for values
        for cell in block:
            pdf.cell(c.width_margin, c.height_margin, str(int(cell)), align='C')
        pdf.ln(c.small_new_line)
    pdf.ln(c.small_new_line)
    pdf.set_font('Arial', 'B', c.h1)  # reset


def write_cost_levels(costs, para_index, pdf):
    num_para = 0
    #  write first row headers
    pdf.set_font('Arial', 'B', c.h3)  # for headers
    pdf.cell(c.width_margin, c.height_margin, "MEM ", align='L')
    pdf.cell(c.width_margin, c.height_margin, "ENERGY (PJ) ", align='L')
    pdf.ln(c.small_new_line)
    pdf.set_font('Arial', '', c.h4)  # for headers
    for cell_index in range(0, len(costs) - 1):
        pdf.cell(c.width_margin, c.height_margin, "L" + str(cell_index), align='L')
        s = ""
        if costs[cell_index + num_para] == 0:
            s = "NOT_CHECKED"
        else:
            s = str(costs[cell_index + num_para])
        pdf.cell(c.width_margin, c.height_margin, s, align='L')
        pdf.ln(c.small_new_line)
        if cell_index in para_index:
            num_para = num_para + 1
            pdf.cell(c.width_margin, c.height_margin, "L" + str(cell_index) + "-PARA", align='L')
            pdf.cell(c.width_margin, c.height_margin, str(costs[cell_index + num_para]), align='L')
            pdf.ln(c.small_new_line)
    pdf.cell(c.width_margin, c.height_margin, "TOTAL", align='L')
    pdf.cell(c.width_margin, c.height_margin, str(sum(costs)), align='L')
    pdf.ln(c.small_new_line)
    pdf.set_font('Arial', 'B', c.h1)  # reset
    pdf.ln(c.large_new_line)


def write_schedule(schedules, pdf):
    for schedule_index in reversed(range(0, len(schedules[0]))):
        schedules[0][schedule_index].reverse()
        pdf.set_font('Arial', 'B', c.h4)  # row header
        pdf.cell(c.width_margin, c.height_margin, "MEM - L" + str(schedule_index) + ": ", align='L')
        pdf.set_font('Arial', 'B', c.h4)  # for values
        pdf.ln(c.small_new_line)
        taps = 0
        for loop in schedules[0][schedule_index]:
            if loop:
                taps += 10
                loop_string = schedule_details(loop)  # write the for statement
                pdf.cell(c.width_margin + taps, c.height_margin, loop_string, align='C')
                pdf.ln(c.small_new_line)
        if schedules[1][schedule_index]:
            # write the unrolled loops
            loop_string = identify_loops_in_list_of_lists(schedules[1][schedule_index])
            pdf.cell(c.width_margin + taps, c.height_margin, "spatially unrolled loops: " + loop_string + '\n',
                     align='C')
        pdf.ln(c.meduim_new_line)


def glossary_element(arr, header, pdf):
    pdf.set_font('Arial', '', c.h3)
    pdf.cell(10, 10, " - ", align="R")
    body = header + " : ( "
    for cell_index in range(0, len(arr)):
        body = body + arr[cell_index]
        if cell_index != len(arr) - 1:
            body = body + ", "
    body = body + " )"
    pdf.cell(50, 10, body, 0, 0, align='L')
    pdf.ln(c.small_new_line)


# glossary definitions
def glossary(levels, pdf):
    pdf.set_font('Arial', 'B', c.h2)
    pdf.cell(0, 10, "Glossary  : ", 0, 0, 'L')
    pdf.ln(c.meduim_new_line)
    cache_list = []
    for index in range(0, levels):
        cache_list.append("L" + str(index))
    glossary_element(cache_list, "Cache Levels", pdf)
    pdf.set_font('Arial', '', c.h4)
    pdf.cell(10, 10, " ", align="R")
    pdf.cell(50, 10, "The smallest index the nearest to CPU.", align='L')
    pdf.ln(c.meduim_new_line)
    glossary_element(c.loops, "Loop Names", pdf)
    pdf.set_font('Arial', 'B', c.h1)


# Introduction
def introduction(body, pdf):
    pdf.set_font('Arial', 'B', c.h1)
    pdf.cell(100, 10, "Introduction : ", 0, 1, 'L')
    pdf.set_font('Arial', '', c.h2)
    pdf.multi_cell(0, c.height_margin, body, 0, 1, "L")


# convert the loop into for statement
def schedule_details(loop):
    return "for ( " + loop[0] + ", " + str(int(loop[1])) + "b" + ", " + str(int(loop[2])) + "p )"


def to_json(json, pdf):
    pdf.set_font('Arial', '', c.h3)
    pdf.cell(10, 5, "{ ", 0, 0, 'L')
    pdf.ln(c.small_new_line)
    for key, value in json.items():
        pdf.cell(50, 5, key + " : ", 0, 0, 'L')
        pdf.multi_cell(100, 5, str(value), 0, 0, 'L')
    pdf.cell(10, 5, " }", 0, 1, 'L')
    pdf.ln(c.small_new_line)


def input_shape(pdf, arch_info, network_info, schedule_info=None):
    pdf.set_font('Arial', 'B', c.h2)
    pdf.cell(0, 10, "Memory Architecture  : ", 0, 1, 'L')
    to_json(arch_info, pdf)
    pdf.set_font('Arial', 'B', c.h2)
    pdf.cell(0, 10, "Layer Architecture  : ", 0, 1, 'L')
    to_json(network_info, pdf)
    if schedule_info is not None:
        pdf.set_font('Arial', 'B', c.h2)
        pdf.cell(0, 10, "Schedule Architecture  : ", 0, 1, 'L')
        to_json(schedule_info, pdf)
