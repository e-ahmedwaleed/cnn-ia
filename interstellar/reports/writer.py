from fpdf import FPDF
from datetime import date
from . import constants as c
from ..verbose.utils import identify_loops_in_list_of_lists


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', c.H4)
        # project name at the left of header
        self.cell(30, 10, 'CNN-IA', 0, 0, 'L')
        # the current date
        self.cell(0, 10, str(date.today()), 0, 0, 'R')
        if self.page_no() != 1:
            self.line(10, 20, 200, 20)
        self.ln(c.MEDIUM_NEW_LINE)
        self.ln(c.SMALL_NEW_LINE)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def write_schedule(schedules, pdf, partitioning_loops=None):
    colored = False
    for schedule_index in reversed(range(0, len(schedules[0]))):
        schedules[0][schedule_index].reverse()
        pdf.set_font('Arial', 'B', c.H4)  # row header
        pdf.cell(c.WIDTH_MARGIN, c.HEIGHT_MARGIN, "MEM - L" + str(schedule_index) + ": ", align='L')
        pdf.set_font('Arial', 'B', c.H4)  # for values
        pdf.ln(c.SMALL_NEW_LINE)
        taps = 0
        for loop in schedules[0][schedule_index]:
            if loop:
                taps += 10
                loop_string = schedule_details(loop)  # write the for statement
                # color the spatially unrolled loops based on schedule partitioning
                if partitioning_loops and schedules[1][schedule_index] and loop[0] in partitioning_loops:
                    colored = True
                    pdf.set_text_color(0, 128, 0)
                pdf.cell(c.WIDTH_MARGIN + taps, c.HEIGHT_MARGIN, loop_string, align='C')
                pdf.set_text_color(0, 0, 0)
                pdf.ln(c.SMALL_NEW_LINE)
        if schedules[1][schedule_index]:
            # write the unrolled loops
            loop_string = identify_loops_in_list_of_lists(schedules[1][schedule_index])
            pdf.cell(5, 10)
            pdf.cell(c.WIDTH_MARGIN, c.HEIGHT_MARGIN, "spatially unrolled loops: " + loop_string + '\n',
                     align='c')
            pdf.ln(c.SMALL_NEW_LINE)
        pdf.ln(c.SMALL_NEW_LINE)
        pdf.set_font('Arial', 'B', c.H1)  # for values
    return colored


def glossary_element(arr, header, pdf):
    pdf.set_font('Arial', '', c.H3)
    pdf.cell(10, 10, " - ", align="R")
    body = header + " : ( "
    for cell_index in range(0, len(arr)):
        body = body + arr[cell_index]
        if cell_index != len(arr) - 1:
            body = body + ", "
    body = body + " )"
    pdf.cell(50, 10, body, 0, 0, align='L')
    pdf.ln(c.SMALL_NEW_LINE)


# glossary definitions
def glossary(levels, pdf):
    pdf.set_font('Arial', 'B', c.H2)
    pdf.cell(25, 10, "Glossary:", "B", 0, 'L')
    pdf.ln(c.MEDIUM_NEW_LINE)
    cache_list = []
    for index in range(0, levels):
        cache_list.append("L" + str(index))
    glossary_element(cache_list, "Memory Levels", pdf)
    pdf.set_font('Arial', '', c.H4)
    pdf.cell(10, 10, " ", align="R")
    pdf.cell(50, 10, "The smallest index the nearest to CPU.", align='L')
    pdf.ln(c.MEDIUM_NEW_LINE)
    glossary_element(c.LOOPS, "Loop Notations", pdf)
    pdf.ln(c.MEDIUM_NEW_LINE)
    notations = ['FILTER WIDTH', "FILTER HEIGHT", "OUTPUT WIDTH", "OUTPUT HEIGHT",
                 "OUTPUT CHANNEL", "INPUT CHANNEL", "BATCH"]
    write_key_value(c.LOOPS, notations, pdf, 10, True)
    pdf.set_font('Arial', 'B', c.H1)


# Introduction
def introduction(body, pdf):
    pdf.set_font('Arial', '', c.H2)
    pdf.multi_cell(0, c.HEIGHT_MARGIN, body, 0, 0)
    pdf.ln(c.SMALL_NEW_LINE)


# convert the loop into for statement
def schedule_details(loop):
    return "for ( " + loop[0] + ", " + str(int(loop[1])) + "b" + ", " + str(int(loop[2])) + "p )"


def convert_dash_names_to_capital_names(names):
    temp = []
    for name in names:
        name = name.replace('_', ' ')
        name = name.capitalize().replace("mac", "MAC")
        temp.append(name)
    return temp


def int_or_float(pdf, row_title, write):
    int_presented = ["Capacity", "Parallel count", "Parallel mode", "FX", "FY", "OX", "OY", "OC", "IC", "ON"]
    if row_title in int_presented:
        pdf.cell(c.WIDTH_MARGIN, c.HEIGHT_MARGIN, str(int(write)), align='C')
    else:
        pdf.cell(c.WIDTH_MARGIN, c.HEIGHT_MARGIN, str(float(write)), align='C')


def write_loops(values, pdf, schedule_info=None):
    pdf.set_font('Arial', 'B', c.H4)
    pdf.ln(c.MEDIUM_NEW_LINE)
    colored = make_table(c.LOOPS, values, pdf, schedule_info)
    pdf.set_font('Arial', 'B', c.H1)  # reset
    return colored


def make_table(rows, columns, pdf, schedule_hint=None):
    pdf.set_font('Arial', 'B', c.H4)  # for headers
    # write the first row ( L0,L1,..)
    pdf.cell(10, 10)
    pdf.cell(c.WIDTH_MARGIN, c.HEIGHT_MARGIN, " ", align='C')
    colored = False
    for cell_index in range(0, len(columns[0])):
        pdf.cell(c.WIDTH_MARGIN, c.HEIGHT_MARGIN, "L" + str(cell_index), align='C')
    pdf.ln(c.INTER_SMALL_NEW_LINE)
    #  write the rows with its values (X => 1,5,...)
    for block_index, block in enumerate(columns):
        pdf.cell(10, 10)
        pdf.set_font('Arial', 'B', c.H4)
        pdf.cell(c.WIDTH_MARGIN, c.HEIGHT_MARGIN, rows[block_index], align='L')
        pdf.set_font('Arial', '', c.H4)
        # (Hinted schedule configurations are in green)
        if schedule_hint is not None:
            if block_index in schedule_hint.keys():
                for cell_index in range(0, len(block)):
                    if type(schedule_hint[block_index][cell_index]) is list:
                        if block[cell_index] in schedule_hint[block_index][cell_index]:
                            colored = True
                            pdf.set_font('Arial', 'B', c.H4)
                            pdf.set_text_color(0, 128, 0)
                            int_or_float(pdf, rows[block_index], block[cell_index])
                            pdf.set_text_color(0, 0, 0)
                            pdf.set_font('Arial', '', c.H4)
                        else:
                            int_or_float(pdf, rows[block_index], block[cell_index])
                    else:
                        int_or_float(pdf, rows[block_index], block[cell_index])
            else:
                for cell in block:
                    int_or_float(pdf, rows[block_index], cell)
        else:
            for cell in block:
                int_or_float(pdf, rows[block_index], cell)
        pdf.ln(c.INTER_SMALL_NEW_LINE)
    pdf.ln(c.SMALL_NEW_LINE)
    return colored


def write_key_value(keys, values, pdf, margin=60, tap=False):
    for key in range(0, len(keys)):
        if tap:
            pdf.cell(14.8, 10)
        pdf.cell(10, 10)
        pdf.set_font('Arial', 'B', c.H4)  # for headers
        pdf.cell(margin, 5, str(keys[key]), align="L")
        pdf.set_font('Arial', '', c.H4)  # for values

        pdf.cell(20, 5, "     :  " + str(values[key]), align="L")
        pdf.ln(c.INTER_SMALL_NEW_LINE)


def to_mem_arch(arch, pdf):
    pdf.set_font('Arial', 'B', c.H2)
    pdf.cell(52, 10, "Memory Architecture:", "B", 1, 'L')
    mem_list = {}
    status_list = {}
    mem_levels = arch['mem_levels']
    # put parallel cost for specific parallel mode
    temp_para_cost = []
    parallel_cost = arch['parallel_cost']
    for val in arch['parallel_mode']:
        if val != 0:
            temp_para_cost.append(parallel_cost[0])
        else:
            temp_para_cost.append(0)
    arch['parallel_cost'] = temp_para_cost

    # fill mem_list
    for key, value in arch.items():
        if type(value) is list and len(value) == mem_levels:
            mem_list[key] = value
    if "memory_partitions" in mem_list:
        del mem_list['memory_partitions']

    # fill status_list
    status_list['precision'] = arch['precision']
    status_list['minimum_utilization'] = str(arch['utilization_threshold'] * 100) + "%"
    status_list['outputs_can_be_buffered_by_mac'] = arch['mac_capacity']
    status_list['replication_to_improve_utilization'] = arch['replication']
    # convert to title
    rows_status = convert_dash_names_to_capital_names(list(status_list.keys()))
    rows_mem = convert_dash_names_to_capital_names(list(mem_list.keys()))

    # write caches
    make_table(rows_mem, list(mem_list.values()), pdf)

    pdf.line(20, 74 + (c.HEIGHT_MARGIN * (len(mem_list) + 1)), (c.WIDTH_MARGIN * (mem_levels + 1)) + 20,
             74 + (c.HEIGHT_MARGIN * (len(mem_list) + 1)))
    # write status as a key : value
    write_key_value(rows_status, list(status_list.values()), pdf, 60)
    pdf.set_font('Arial', 'B', c.H1)
