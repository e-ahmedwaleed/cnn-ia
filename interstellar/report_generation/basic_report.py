# pip install fpdf
from fpdf import FPDF
from datetime import date
from verbose.utils import identify_loops_in_list_of_lists

"""
font_sizes used : 16 for h1
                  14 for h2
                  12 for h3
                  10 for h4
                  8 for h4
"""
h1 = 16
h2 = 14
h3 = 12
h4 = 10
h5 = 8

"""
line spaces used  : 5, 10, 20
"""
small_new_line = 5
meduim_new_line = 10
large_new_line = 20

"""
margins used  : 30 for width
                  8 for height
"""
width_margin = 30
height_margin = 8


def write_loops(values, pdf):
    loops = ["MEM", "FX", "FY", "OX", "OY", "OC", "IC", "ON"]  # write names of the seven loops
    pdf.set_font('Arial', 'B', h4)
    pdf.ln(meduim_new_line)
    # write first row headers
    pdf.cell(width_margin, height_margin, loops[0], align='C')
    for cell_index in range(0, len(values[0])):
        pdf.cell(width_margin, height_margin, "L" + str(cell_index), align='C')
    pdf.ln(small_new_line)

    # write the type of loop (FX,FY..etc) with its values
    for block_index, block in enumerate(values):
        pdf.set_font('Arial', 'B', h4)  # for headers
        pdf.cell(width_margin, height_margin, loops[block_index + 1], align='C')
        pdf.set_font('Arial', '', h4)  # for values
        for cell in block:
            pdf.cell(width_margin, height_margin, str(cell), align='C')
        pdf.ln(small_new_line)
    pdf.ln(small_new_line)
    pdf.set_font('Arial', 'B', h1)  # reset


def write_cost_levels(costs, para_index, pdf):
    #  write first row headers
    pdf.set_font('Arial', 'B', h3)  # for headers
    pdf.cell(width_margin, height_margin, "MEM ", align='L')
    pdf.cell(width_margin, height_margin, "ENERGY (PJ) ", align='L')
    pdf.ln(small_new_line)
    pdf.set_font('Arial', '', h4)  # for headers
    for cell_index in range(0, len(costs) - 1):
        pdf.cell(width_margin, height_margin, "L" + str(cell_index), align='L')
        pdf.cell(width_margin, height_margin, str(costs[cell_index]), align='L')
        pdf.ln(small_new_line)
        if cell_index in para_index:
            pdf.cell(width_margin, height_margin, "L" + str(cell_index) + "-PARA", align='L')
            pdf.cell(width_margin, height_margin, str(costs[cell_index]), align='L')
            pdf.ln(small_new_line)
    pdf.cell(width_margin, height_margin, "TOTAL", align='L')
    pdf.cell(width_margin, height_margin, str(sum(costs)), align='L')
    pdf.ln(small_new_line)
    pdf.set_font('Arial', 'B', h1)  # reset
    pdf.ln(large_new_line)


def write_schedule(schedules, pdf):
    for schedule_index in range(0, len(schedules[0])):
        schedules[0][schedule_index].reverse()
        pdf.set_font('Arial', 'B', h4)  # row header
        pdf.cell(width_margin, height_margin, "MEM - L" + str(schedule_index) + ": ", align='L')
        pdf.set_font('Arial', 'B', h4)  # for values
        pdf.ln(small_new_line)
        taps = 0
        for loop in schedules[0][schedule_index]:
            if loop:
                taps += 10
                loop_string = schedule_details(loop)  # write the for statement
                pdf.cell(width_margin + taps, height_margin, loop_string, align='C')
                pdf.ln(small_new_line)
        if schedules[1][schedule_index]:
            # write the unrolled loops
            loop_string = identify_loops_in_list_of_lists(schedules[1][schedule_index])
            pdf.cell(width_margin + taps, height_margin, "spatially unrolled loops: " + loop_string + '\n', align='C')
        pdf.ln(meduim_new_line)


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', h4)
        # project name at the left of header
        self.cell(30, 10, 'CNN-EIA', 0, 0, 'L')
        # the current date
        self.cell(0, 10, str(date.today()), 0, 0, 'R')
        if self.page_no() != 1:
            self.line(10, 20, 200, 20)
        self.ln(meduim_new_line)
        self.ln(small_new_line)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def glossary_element(arr, header, pdf):
    pdf.set_font('Arial', '', h3)
    pdf.cell(10, 10, " - ", align="R")
    body = header + " : ( "
    for cell_index in range(0, len(arr)):
        body = body + arr[cell_index]
        if cell_index != len(arr) - 1:
            body = body + ", "
    body = body + " )"
    pdf.cell(50, 10, body, 0, 0, align='L')
    pdf.ln(small_new_line)


# glossary definitions
def glossary(levels, pdf):
    loops = ["MEM", "FX", "FY", "OX", "OY", "OC", "IC", "ON"]  # write names of the seven loops
    pdf.set_font('Arial', 'B', h2)
    pdf.cell(0, 10, "Glossary  : ", 0, 0, 'L')
    pdf.ln(meduim_new_line)
    cache_list = []
    for index in range(0, len(levels)):
        cache_list.append("L" + str(index))
    glossary_element(cache_list, "Cache Levels", pdf)
    pdf.set_font('Arial', '', h4)
    pdf.cell(10, 10, " ", align="R")
    pdf.cell(50, 10, "The smallest index the nearest to CPU.", align='L')
    pdf.ln(meduim_new_line)
    glossary_element(loops, "Loop Names", pdf)
    pdf.set_font('Arial', 'B', h1)


# Introduction
def introduction(body, pdf):
    pdf.set_font('Arial', 'B', h1)
    pdf.cell(100, 10, "Introduction : ", 0, 1, 'L')
    pdf.set_font('Arial', '', h2)
    pdf.multi_cell(0, height_margin, body, 0, 1, "L")


# convert the loop into for statement
def schedule_details(loop):
    return "for ( " + loop[0] + ", " + str(int(loop[1])) + "b" + ", " + str(int(loop[2])) + "p )"


def to_json(json, pdf):
    pdf.set_font('Arial', '', h3)
    pdf.cell(10, 5, "{ ", 0, 0, 'L')
    pdf.ln(small_new_line)
    for key, value in json.items():
        pdf.cell(50, 5, key + " : ", 0, 0, 'L')
        pdf.multi_cell(100, 5, str(value), 0, 0, 'L')
    pdf.cell(10, 5, " }", 0, 1, 'L')
    pdf.ln(small_new_line)


def input_shape(arch_info, network_info, schedule_info, pdf):
    pdf.set_font('Arial', 'B', h2)
    pdf.cell(0, 10, "Memory Architecture  : ", 0, 1, 'L')
    to_json(arch_info, pdf)
    pdf.set_font('Arial', 'B', h2)
    pdf.cell(0, 10, "Layer Architecture  : ", 0, 1, 'L')
    to_json(network_info, pdf)
    pdf.set_font('Arial', 'B', h2)
    pdf.cell(0, 10, "Schedule Architecture  : ", 0, 1, 'L')
    to_json(schedule_info, pdf)


def generate_basic(map_config, costs, para_index, schedules, arch_info, network_info, schedule_info):
    print(arch_info)
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', h1)
    # header of report
    """ Side Note: Name of Model """
    pdf.cell(0, 10, "{Loop Blocking} Analyzer Report", 1, 0, 'C')
    pdf.ln(large_new_line)

    """ Introduction """
    body = """This report generated by CNN-EIA. The goal of this report is analysing the loop blocking of the given Machine Learning Model. The analysis was done on these inputs : """
    introduction(body, pdf)
    """
        Input Shape : The input from program
    """
    input_shape(arch_info, network_info, schedule_info, pdf)

    """ Glossary"""

    """  
        explanation of memory caches and layer parameters
    """
    glossary(map_config.loop_blockings[0], pdf)
    pdf.ln(meduim_new_line)

    """
        Output 
    """
    pdf.set_font('Arial', 'B', h1)
    pdf.cell(0, 10, "Analysis Output  : ", 0, 0, 'L')

    """ 
        Map Configurations
    """
    pdf.ln(meduim_new_line)
    pdf.cell(100, 10, "Map Configuration", 1, 1, 'C')
    pdf.ln(meduim_new_line)

    # loop blocking

    pdf.cell(50, 10, "Loop Blocking ( factors ): ", "B", 0, 'L')
    write_loops(map_config.loop_blockings, pdf)
    pdf.set_font('Arial', '', h2)
    pdf.cell(width_margin, height_margin, "The factors of each loop for each cache.", align="L")
    pdf.ln(large_new_line)

    # loop partitioning
    pdf.set_font('Arial', 'B', h1)
    pdf.cell(50, 10, "Loop Partitioning ( units ): ", "B", 0, 'L')
    write_loops(map_config.loop_partitionings, pdf)
    pdf.set_font('Arial', '', h2)
    pdf.cell(width_margin, height_margin, "Take the processing elements from parallel memories.", align="L")
    pdf.ln(large_new_line)

    # loop ordering
    pdf.set_font('Arial', 'B', h1)
    pdf.cell(50, 10, "Loop Ordering : ", "B", 0, 'L')
    write_loops(map_config.loop_orders, pdf)
    pdf.set_font('Arial', '', h2)
    pdf.cell(width_margin, height_margin, "The order on each cache.", align="L")
    pdf.ln(large_new_line)
    pdf.set_font('Arial', 'B', h1)

    """ 
        Schedule 
    """

    pdf.cell(100, 10, "Schedule", 1, 1, 'C')
    pdf.ln(meduim_new_line)
    pdf.set_font('Arial', 'B', h2)
    pdf.cell(100, 10, "The Best format for schedule found is : ")
    pdf.ln(meduim_new_line)
    write_schedule(schedules, pdf)

    """ 
        Cost Of Each Level 
    """

    pdf.cell(100, 10, "Cost", 1, 1, 'C')
    pdf.ln(meduim_new_line)
    write_cost_levels(costs, para_index, pdf)

    pdf.output('report_generation/basic_output.pdf', 'F')
