from . import writer as w
from . import constants as c
from ..verbose.utils import undo_arch_info_capacity_scale


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
