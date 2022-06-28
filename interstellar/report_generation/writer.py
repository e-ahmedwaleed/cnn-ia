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


def write_loops(values, schedule_info, pdf):
    pdf.set_font('Arial', 'B', c.h4)
    pdf.ln(c.meduim_new_line)
    make_table(c.loops, values, pdf, schedule_info)
    pdf.set_font('Arial', 'B', c.h1)  # reset


def write_cost_levels(costs, para_index, pdf):
    num_para = 0
    #  write first row headers
    pdf.set_font('Arial', 'B', c.h3)  # for headers
    pdf.cell(c.width_margin, c.height_margin, "MEM ", align='L')
    pdf.cell(c.width_margin, c.height_margin, "ENERGY (PJ) ", align='L')
    pdf.ln(c.inter_small_new_line)
    pdf.set_font('Arial', '', c.h4)  # for headers
    for cell_index in range(0, len(costs) - 1):
        s_checked = ""
        not_checked = 0
        if costs[cell_index + num_para] == 0:
            s_checked = "NOT_CHECKED"
            not_checked = cell_index
        else:
            s_checked = str(costs[cell_index + num_para])
        if s_checked != "NOT_CHECKED":
            pdf.cell(c.width_margin, c.height_margin, "L" + str(cell_index), align='L')
            pdf.cell(c.width_margin, c.height_margin, s_checked, align='L')
            pdf.ln(c.inter_small_new_line)
        if cell_index in para_index:
            num_para = num_para + 1
            pdf.cell(c.width_margin, c.height_margin, "L" + str(cell_index) + "-PARA", align='L')
            pdf.cell(c.width_margin, c.height_margin, str(costs[cell_index + num_para]), align='L')
            pdf.ln(c.inter_small_new_line)
    pdf.cell(c.width_margin, c.height_margin, "TOTAL", align='L')
    pdf.cell(c.width_margin, c.height_margin, str(sum(costs)), align='L')
    pdf.ln(c.meduim_new_line)
    if s_checked == "NOT_CHECKED":
        pdf.set_font('Arial', 'B', c.h3)
        pdf.cell(c.width_margin, c.height_margin, "- L"+str(not_checked) +
                 " memory was not checked for invalid underutilized.", align='L')

    pdf.ln(c.large_new_line)


def write_schedule(schedules,  partitioning_loops, pdf):
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
                if partitioning_loops and loop[0] in partitioning_loops:
                    pdf.set_text_color(0, 128, 0)
                loop_string = schedule_details(loop)  # write the for statement
                pdf.cell(c.width_margin + taps, c.height_margin, loop_string, align='C')
                pdf.set_text_color(0, 0, 0)
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
    pdf.cell(30, 10, "Glossary  : ", "B", 0, 'L')
    pdf.ln(c.meduim_new_line)
    cache_list = []
    for index in range(0, levels):
        cache_list.append("L" + str(index))
    glossary_element(cache_list, "Memory Levels", pdf)
    pdf.set_font('Arial', '', c.h4)
    pdf.cell(10, 10, " ", align="R")
    pdf.cell(50, 10, "The smallest index the nearest to CPU.", align='L')
    pdf.ln(c.meduim_new_line)
    glossary_element(c.loops, "Loop Notations", pdf)
    pdf.ln(c.meduim_new_line)
    notations = ['FILTER WIDTH', "FILTER HEIGHT", "OUTPUT WIDTH", "OUTPUT HEIGHT",
                 "OUTPUT CHANNEL", "INPUT CHANNEL", "BATCH"]
    write_key_value(c.loops, notations, pdf)
    pdf.set_font('Arial', 'B', c.h1)


# Introduction
def introduction(body, pdf):
    pdf.set_font('Arial', '', c.h2)
    pdf.multi_cell(0, c.height_margin, body, 0, 1, "L")
    pdf.ln(c.small_new_line)


# convert the loop into for statement
def schedule_details(loop):
    return "for ( " + loop[0] + ", " + str(int(loop[1])) + "b" + ", " + str(int(loop[2])) + "p )"


def convert_dash_names_to_capital_names(names):
    temp = []
    for name in names:
        name = name.replace('_', ' ')
        name = name.capitalize()
        temp.append(name)
    return temp


def make_table(rows, columns, pdf, schedule_hint=0):
    pdf.set_font('Arial', 'B', c.h4)  # for headers
    # write the first row ( L0,L1,..)
    pdf.cell(10, 10)
    pdf.cell(c.width_margin, c.height_margin, " ", align='C')
    for cell_index in range(0, len(columns[0])):
        pdf.cell(c.width_margin, c.height_margin, "L" + str(cell_index), align='C')
    pdf.ln(c.inter_small_new_line)
    #  write the rows with its values (X => 1,5,...)
    for block_index, block in enumerate(columns):
        pdf.cell(10, 10)
        pdf.set_font('Arial', 'B', c.h4)
        pdf.cell(c.width_margin, c.height_margin, rows[block_index], align='L')
        pdf.set_font('Arial', '', c.h4)
        # (Hinted schedule configurations are in green)
        if schedule_hint != 0:
            if block_index in schedule_hint.keys():
                for cell_index in range(0, len(block)):
                    if type(schedule_hint[block_index][cell_index]) is list:
                        if block[cell_index] in schedule_hint[block_index][cell_index]:
                            pdf.set_font('Arial', 'B', c.h4)
                            pdf.set_text_color(0, 128, 0)
                            pdf.cell(c.width_margin, c.height_margin, str(int(block[cell_index])), align='C')
                            pdf.set_text_color(0, 0, 0)
                            pdf.set_font('Arial', '', c.h4)
                        else:
                            pdf.cell(c.width_margin, c.height_margin, str(int(block[cell_index])), align='C')
                    else:
                        pdf.cell(c.width_margin, c.height_margin, str(int(block[cell_index])), align='C')
            else:
                for cell in block:
                    pdf.cell(c.width_margin, c.height_margin, str(int(cell)), align='C')
        else:
            for cell in block:
                pdf.cell(c.width_margin, c.height_margin, str(int(cell)), align='C')
        pdf.ln(c.inter_small_new_line)
    pdf.ln(c.small_new_line)


def write_key_value(keys, values, pdf):
    for key in range(0, len(keys)):
        pdf.cell(25, 10)
        pdf.set_font('Arial', 'B', c.h4)  # for headers
        pdf.cell(60, 5, str(keys[key]), align="L")
        pdf.set_font('Arial', '', c.h4)  # for values
        pdf.cell(25, 10)
        pdf.cell(20, 5, " :     " + str(values[key]), align="L")
        pdf.ln(c.inter_small_new_line)


def to_mem_arch(arch, pdf):
    mem_list = {}
    status_list = {}
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
        if type(value) is list and len(value) == arch['mem_levels']:
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
    # write cahces
    make_table(rows_mem, list(mem_list.values()), pdf)

    # write status as a key : value
    write_key_value(rows_status, list(status_list.values()), pdf)


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
    pdf.cell(55, 10, "Memory Architecture  : ", "B", 1, 'L')
    to_mem_arch(arch_info, pdf)
    pdf.set_font('Arial', 'B', c.h1)
    # pdf.cell(0, 10, "Layer Architecture  : ", 0, 1, 'L')
    # to_json(network_info, pdf)
    # if schedule_info is not None:
    #     pdf.set_font('Arial', 'B', c.h2)
    #     pdf.cell(0, 10, "Schedule Architecture  : ", 0, 1, 'L')
    #     to_json(schedule_info, pdf)
