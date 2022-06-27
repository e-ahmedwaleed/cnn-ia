# pip install fpdf
from fpdf import FPDF

from verbose.utils import identify_loops_in_list_of_lists

"""
font_sizes used : header_font for Header
                  10 for header of the first rows
                  elements_font for values in the table
"""
header_font = 16
row_font_header = 10
elements_font = 8

"""
line spaces used is : 5, 10, 20
"""
small_new_line = 5
meduim_new_line = 10
large_new_line = 20

"""
margins used is : 30 for width
                  8 for height
"""
width_margin = 30
height_margin = 8


def write_loops(values, pdf):
    loops = ["MEM", "FX", "FY", "OX", "OY", "OC", "IC", "ON"]  # write names of the seven loops
    pdf.set_font('Arial', 'B', row_font_header)

    # write first row headers
    pdf.cell(width_margin, height_margin, loops[0], align='C')
    for cell_index in range(0, len(values[0])):
        pdf.cell(width_margin, height_margin, "L" + str(cell_index), align='C')
    pdf.ln(small_new_line)

    # write the type of loop (FX,FY..etc) with its values
    for block_index, block in enumerate(values):
        pdf.set_font('Arial', 'B', row_font_header)  # for headers
        pdf.cell(width_margin, height_margin, loops[block_index + 1], align='C')
        pdf.set_font('Arial', '', elements_font)  # for values
        for cell in block:
            pdf.cell(width_margin, height_margin, str(cell), align='C')
        pdf.ln(small_new_line)
    pdf.ln(meduim_new_line)
    pdf.set_font('Arial', 'B', header_font)  # reset


# convert the loop into for statement
def schedule_details(loop):
    return "for ( " + loop[0] + ", " + str(int(loop[1])) + "b" + ", " + str(int(loop[2])) + "p )"


def generate_basic(map_config, costs, para_index, schedules=0):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', header_font)
    """ Map Configurations """

    pdf.cell(100, 10, "Map Configuration", 1, 0, 'C')
    pdf.ln(large_new_line)

    # loop blocking

    pdf.cell(50, 10, "Loop Blocking : ", "B", 0, 'L')
    pdf.ln(large_new_line)
    write_loops(map_config.loop_blockings, pdf)

    # loop partitioning

    pdf.cell(50, 10, "Loop Partitioning : ", "B", 0, 'L')
    pdf.ln(large_new_line)
    write_loops(map_config.loop_partitionings, pdf)

    # loop ordering

    pdf.cell(50, 10, "Loop Ordering : ", "B", 0, 'L')
    pdf.ln(large_new_line)
    write_loops(map_config.loop_orders, pdf)

    """ Cost Of Each Level """

    pdf.cell(100, 10, "Cost", 1, 0, 'C')
    pdf.ln(large_new_line)

    #  write first row headers
    pdf.set_font('Arial', 'B', row_font_header)  # for headers
    pdf.cell(width_margin, height_margin, "MEM: ", align='L')
    for cell_index in range(0, len(costs) - 1):
        pdf.cell(width_margin, height_margin, "L" + str(cell_index), align='C')
        if cell_index in para_index:
            pdf.cell(width_margin, height_margin, "L" + str(cell_index) + "-PARA", align='C')
    pdf.cell(width_margin, height_margin, "TOTAL", align='C')
    pdf.ln(small_new_line)

    # write the values of energy
    pdf.cell(width_margin, height_margin, "ENERGY: ", align='L')
    pdf.set_font('Arial', '', elements_font)  # for values
    for cell in costs:
        pdf.cell(width_margin, height_margin, str(cell), align='C')

    pdf.cell(width_margin, height_margin, str(sum(costs)), align='C')  # TOTAL
    pdf.set_font('Arial', 'B', header_font)  # reset
    pdf.ln(large_new_line)

    """ Schedule """

    pdf.cell(100, 10, "Schedule", 1, 0, 'C')
    pdf.ln(large_new_line)

    for schedule_index in range(0, len(schedules[0])):
        schedules[0][schedule_index].reverse()
        pdf.set_font('Arial', 'B', row_font_header)  # row header
        pdf.cell(width_margin, height_margin, "MEM - L" + str(schedule_index) + ": ", align='L')
        pdf.set_font('Arial', 'B', row_font_header)  # for values
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

    pdf.output('report_generation/basic_output.pdf', 'F')
