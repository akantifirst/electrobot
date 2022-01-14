import ezdxf
from ezdxf import units, zoom
from ast import literal_eval as make_tuple
from common import csv_read
from common import get_datetime

# Define line and text styles
style_name = {'height': 3.5, 'color': 5, 'style': 'isocpeur'}
style_std = {'height': 2.5, 'color': 251, 'style': 'isocpeur'}
style_q = {'height': 4, 'color': 5, 'style': 'isocpeur'}
style_title1 = {'height': 1.45, 'color': 7, 'style': 'arial'}
style_title2 = {'height': 2.0, 'color': 7, 'style': 'arial'}
style_title3 = {'height': 2.5, 'color': 7, 'style': 'arial'}
style_title4 = {'height': 3.0, 'color': 7, 'style': 'arial'}
style_boldline = {'lineweight': 40, 'color': 7}
style_electro = {'lineweight': 40, 'color': 5}
style_thin = {'lineweight': 0, 'color': 7}


def get_insert_point(number):
    """Returns x, y coordinates."""
    x_feed = 101 + number * 46
    y_feed = 155
    return x_feed, y_feed


def gen_infobox(block, dx=0, dy=0) -> None:
    # Inner part of info box
    block.add_line((0 + dx, 91 + dy), (0 + dx, 115 + dy), dxfattribs=style_thin)  # vertical center
    block.add_line((21 + dx, 91 + dy), (-21 + dx, 91 + dy), dxfattribs=style_thin)  # horizontal under length
    block.add_line((21 + dx, 97 + dy), (-21 + dx, 97 + dy), dxfattribs=style_thin)  # horizontal under cable
    block.add_line((21 + dx, 103 + dy), (-21 + dx, 103 + dy), dxfattribs=style_thin)  # horizontal under phi
    block.add_line((21 + dx, 109 + dy), (-21 + dx, 109 + dy), dxfattribs=style_thin)  # horizontal under power
    block.add_line((21 + dx, 115 + dy), (-21 + dx, 115 + dy), dxfattribs=style_thin)  # horizontal under name

    # Outer part of info box
    block.add_lwpolyline(((-21 + dx, 85 + dy),
                          (-21 + dx, 123 + dy),
                          (21 + dx, 123 + dy),
                          (21 + dx, 85 + dy),
                          (-21 + dx, 85 + dy)),
                         dxfattribs=style_boldline)

    # Define some attributes for the block 'block'
    block.add_attdef('name', dxfattribs=style_name).set_pos((0 + dx, 117.25 + dy), align='CENTER')
    block.add_attdef('power', dxfattribs=style_std).set_pos((-19 + dx, 110.75 + dy), align='LEFT')
    block.add_attdef('g', dxfattribs=style_std).set_pos((2 + dx, 110.75 + dy), align='LEFT')
    block.add_attdef('phi', dxfattribs=style_std).set_pos((-19 + dx, 104.75 + dy), align='LEFT')
    block.add_attdef('voltage', dxfattribs=style_std).set_pos((2 + dx, 104.75 + dy), align='LEFT')
    block.add_attdef('cable', dxfattribs=style_std).set_pos((-19 + dx, 98.75 + dy), align='LEFT')
    block.add_attdef('section', dxfattribs=style_std).set_pos((2 + dx, 98.75 + dy), align='LEFT')
    block.add_attdef('length', dxfattribs=style_std).set_pos((-19 + dx, 92.75 + dy), align='LEFT')
    block.add_attdef('du', dxfattribs=style_std).set_pos((2 + dx, 92.75 + dy), align='LEFT')
    block.add_attdef('laying', dxfattribs=style_std).set_pos((0 + dx, 86.75 + dy), align='CENTER')


def gen_nb_ls(doc, name: str, dx=0, dy=0, arrow=True):
    # Create a block with the name 'NB_LS'
    nb_ls = doc.blocks.new(name=name)

    # Set millimeter as 'NB_LS' block units
    nb_ls.units = units.MM

    # Add DXF entities to the block 'NB_LS'.
    # Blue lines
    nb_ls.add_line((0, 19.5), (0, 0), dxfattribs=style_electro)  # point to contact
    nb_ls.add_line((0, 19.5), (-5, 28.5), dxfattribs=style_electro)  # contact
    nb_ls.add_line((-4.7, 22.7), (-2.5, 24), dxfattribs=style_electro)  # release
    nb_ls.add_line((0, 29), (0, 77.5), dxfattribs=style_electro)  # contact to feeder

    nb_ls.add_attdef('cb', dxfattribs=style_std).set_pos((2.8, 32), align='LEFT')
    nb_ls.add_attdef('cb_type', dxfattribs=style_std).set_pos((2.8, 26), align='LEFT')
    nb_ls.add_attdef('release', dxfattribs=style_std).set_pos((2.8, 20), align='LEFT')
    nb_ls.add_attdef('ib', dxfattribs=style_std).set_pos((2.8, 14), align='LEFT')
    nb_ls.add_attdef('q', dxfattribs=style_q).set_pos((-2.8, 13), align='RIGHT')

    # Define hatch arrows and points
    hatch = nb_ls.add_hatch(color=5)
    hatch.paths.add_polyline_path([(-6, 22), (-4.75, 23.45), (-4.12, 22.35)], is_closed=True)

    # Do not add circle and arrow for infoing feeder
    if arrow:
        hatch.paths.add_polyline_path([(-1, 0, -1), (1, 0, -1)], is_closed=True)
        hatch.paths.add_polyline_path([(0, 80), (-0.95, 77.25), (0.95, 77.25)], is_closed=True)

    gen_infobox(nb_ls, dx, dy)


def gen_title(doc):
    title = doc.blocks.new(name='TITLE')

    # Set millimeter as 'NB_LS' block units
    title.units = units.MM

    # Add DXF entities to the block 'TITLE'.
    # title.add_line((0, 0), (0, 30), dxfattribs=style_boldline)  # left vertical
    title.add_line((0, 30), (393, 30), dxfattribs=style_boldline)  # upper horizontal
    title.add_line((150, 30), (150, 0), dxfattribs=style_boldline)  # center left vertical
    title.add_line((243, 0), (243, 30), dxfattribs=style_boldline)  # center right vertical
    title.add_line((0, 24), (150, 24), dxfattribs=style_thin)
    title.add_line((0, 18), (150, 18), dxfattribs=style_thin)
    title.add_line((0, 12), (150, 12), dxfattribs=style_thin)
    title.add_line((0, 6), (393, 6), dxfattribs=style_thin)
    title.add_line((12, 0), (12, 30), dxfattribs=style_thin)
    title.add_line((30, 0), (30, 30), dxfattribs=style_thin)
    title.add_line((42, 0), (42, 30), dxfattribs=style_thin)
    title.add_line((243, 24), (393, 24), dxfattribs=style_thin)
    title.add_line((243, 12), (393, 12), dxfattribs=style_thin)
    title.add_line((263.5, 24), (263.5, 30), dxfattribs=style_thin)
    title.add_line((354, 24), (354, 30), dxfattribs=style_thin)
    title.add_line((374, 24), (374, 30), dxfattribs=style_thin)
    title.add_line((263.5, 0), (263.5, 12), dxfattribs=style_thin)
    title.add_line((311, 0), (311, 12), dxfattribs=style_thin)
    title.add_line((323, 0), (323, 12), dxfattribs=style_thin)
    title.add_line((335.5, 0), (335.5, 12), dxfattribs=style_thin)
    title.add_line((350.5, 0), (350.5, 12), dxfattribs=style_thin)
    title.add_line((366, 0), (366, 12), dxfattribs=style_thin)
    title.add_line((378, 0), (378, 12), dxfattribs=style_thin)

    # Draw main frame and bounding box
    title.add_lwpolyline(((0, 0), (0, 283), (393, 283), (393, 0), (0, 0)), dxfattribs=style_boldline)

    # add constant text entities
    title.add_text('Münsterplatz 11, 78462 Konstanz', dxfattribs=style_title1).set_pos((151.7, 15.1), align='LEFT')
    title.add_text('Tel / Fax: 07531-1302-0/33', dxfattribs=style_title1).set_pos((151.7, 12.7), align='LEFT')
    title.add_text('www.neher-butz-plus.de', dxfattribs=style_title1).set_pos((151.7, 10.25), align='LEFT')
    title.add_text('ib@neher-butz-plus.de', dxfattribs=style_title1).set_pos((151.7, 7.8), align='LEFT')
    title.add_text('Uhlandstr. 5, 89250 Senden', dxfattribs=style_title1).set_pos((241.3, 15.1), align='RIGHT')
    title.add_text('Tel / Fax: 07307-92110-0/99', dxfattribs=style_title1).set_pos((241.3, 12.7), align='RIGHT')
    title.add_text('www.neher-butz-plus.de', dxfattribs=style_title1).set_pos((241.3, 10.25), align='RIGHT')
    title.add_text('ulm@neher-butz-plus.de', dxfattribs=style_title1).set_pos((241.3, 7.8), align='RIGHT')
    title.add_text('Art der Änderung', dxfattribs=style_title2).set_pos((99.0, 26.0), align='CENTER')
    title.add_text('Name', dxfattribs=style_title2).set_pos((36.0, 26.0), align='CENTER')
    title.add_text('Datum', dxfattribs=style_title2).set_pos((21.0, 26.0), align='CENTER')
    title.add_text('Index', dxfattribs=style_title2).set_pos((6.0, 26.0), align='CENTER')
    title.add_text('Index', dxfattribs=style_title2).set_pos((317.0, 8.0), align='CENTER')
    title.add_text('Maßstab', dxfattribs=style_title2).set_pos((329.25, 8.0), align='CENTER')
    title.add_text('Datum', dxfattribs=style_title2).set_pos((343.0, 8.0), align='CENTER')
    title.add_text('Gezeichnet', dxfattribs=style_title2).set_pos((358.25, 8.0), align='CENTER')
    title.add_text('Geprüft', dxfattribs=style_title2).set_pos((372.0, 8.0), align='CENTER')
    title.add_text('Blatt / von', dxfattribs=style_title2).set_pos((385.5, 8.0), align='CENTER')
    title.add_text('Blattgröße', dxfattribs=style_title2).set_pos((364.0, 26.0), align='CENTER')
    title.add_text('-', dxfattribs=style_title4).set_pos((329.25, 1.5), align='CENTER')
    title.add_text('Planinhalt', dxfattribs=style_title2).set_pos((244.5, 20.0), align='LEFT')
    title.add_text('Projekt', dxfattribs=style_title2).set_pos((244.5, 26.0), align='LEFT')
    title.add_text('CAD-Datei', dxfattribs=style_title2).set_pos((244.5, 8.0), align='LEFT')
    title.add_text('Export Datei', dxfattribs=style_title2).set_pos((244.5, 2.0), align='LEFT')

    title.add_attdef('DRUECKDATUM', dxfattribs=style_title1).set_pos((196.5, 2.3), align='CENTER')
    title.add_attdef('BLATTGROESSE', dxfattribs=style_title3).set_pos((383.5, 25.75), align='CENTER')
    title.add_attdef('INDEX', dxfattribs=style_title4).set_pos((317.0, 1.5), align='CENTER')
    title.add_attdef('DATUM', dxfattribs=style_title2).set_pos((343.0, 2.0), align='CENTER')
    title.add_attdef('GEZEICHNET', dxfattribs=style_title2).set_pos((358.25, 2.0), align='CENTER')
    title.add_attdef('GEPRUEFT', dxfattribs=style_title2).set_pos((372.0, 2.0), align='CENTER')
    title.add_attdef('BLATT_VON', dxfattribs=style_title2).set_pos((385.5, 2.0), align='CENTER')
    title.add_attdef('PROJEKT', dxfattribs=style_title3).set_pos((308.75, 25.75), align='CENTER')
    title.add_attdef('PLANINHALT', dxfattribs=style_title3).set_pos((318.0, 18.0), align='CENTER')
    title.add_attdef('CAD_DATEI', dxfattribs=style_title2).set_pos((287.25, 8.0), align='CENTER')
    title.add_attdef('PDF_DATEI', dxfattribs=style_title2).set_pos((287.25, 2.3), align='CENTER')
    title.add_attdef('I1_AENDERUNG', dxfattribs=style_title2).set_pos((45.0, 20.0), align='LEFT')
    title.add_attdef('I1_DATUM', dxfattribs=style_title2).set_pos((21.0, 20.0), align='CENTER')
    title.add_attdef('I1_NAME', dxfattribs=style_title2).set_pos((36.0, 20.0), align='CENTER')
    title.add_attdef('INDEX1', dxfattribs=style_title2).set_pos((6.0, 20.0), align='CENTER')
    title.add_attdef('I2_AENDERUNG', dxfattribs=style_title2).set_pos((45.0, 14.0), align='LEFT')
    title.add_attdef('I2_DATUM', dxfattribs=style_title2).set_pos((21.0, 14.0), align='CENTER')
    title.add_attdef('I2_NAME', dxfattribs=style_title2).set_pos((36.0, 14.0), align='CENTER')
    title.add_attdef('INDEX2', dxfattribs=style_title2).set_pos((6.0, 14.0), align='CENTER')
    title.add_attdef('I3_AENDERUNG', dxfattribs=style_title2).set_pos((45.0, 8.0), align='LEFT')
    title.add_attdef('I3_DATUM', dxfattribs=style_title2).set_pos((21.0, 8.0), align='CENTER')
    title.add_attdef('I3_NAME', dxfattribs=style_title2).set_pos((36.0, 8.0), align='CENTER')
    title.add_attdef('INDEX3', dxfattribs=style_title2).set_pos((6.0, 8.0), align='CENTER')
    title.add_attdef('I4_DATUM', dxfattribs=style_title2).set_pos((21.0, 2.0), align='CENTER')
    title.add_attdef('I4_NAME', dxfattribs=style_title2).set_pos((36.0, 2.0), align='CENTER')
    title.add_attdef('INDEX4', dxfattribs=style_title2).set_pos((6.0, 2.0), align='CENTER')
    title.add_attdef('I4_AENDERUNG', dxfattribs=style_title2).set_pos((45.0, 2.0), align='LEFT')


def gen_logo(doc):
    # Load vector NB Logo coordinates
    data = csv_read(r'db/LOGO.csv')
    logo = doc.blocks.new(name='LOGO')

    green_hatch = logo.add_hatch(color=136)
    gray_hatch = logo.add_hatch(color=252)

    for number, row in enumerate(data):
        row = [make_tuple(e) for e in row]
        if number == 0:
            green_hatch.paths.add_polyline_path(row, is_closed=True)
        else:
            if number < 11:
                gray_hatch.paths.add_polyline_path(row, is_closed=True)
            else:
                gray_hatch.paths.add_polyline_path(row, is_closed=True, flags=ezdxf.const.BOUNDARY_PATH_OUTERMOST)


def cad_write(formatted_data, project_number, project_name, switchboard):
    # Create a new drawing in the DXF format of AutoCAD 2010
    doc = ezdxf.new('R2000', setup=True)

    # Set millimeter as document/modelspace units
    doc.units = units.MM

    # Add custom text style to the document
    doc.styles.new('isocpeur', dxfattribs={'font': 'ISOCPEUR.ttf'})
    doc.styles.new('arial', dxfattribs={'font': 'Arial.ttf'})

    # Add title, logo, and content to the drawing
    gen_title(doc)
    # Add outgoing feeders
    gen_nb_ls(doc, 'NB_LS', 0, 0, True)
    # Add ingoing feeder
    gen_nb_ls(doc, 'NB_EN', 0, -130, False)
    gen_logo(doc)

    # Define modelspace
    msp = doc.modelspace()
    zoom.extents(msp)

    msp.add_lwpolyline(((0, 0), (0, 297), (420, 297), (420, 0), (0, 0)), dxfattribs=style_thin)
    title_ref = msp.add_blockref('TITLE', (20, 7))

    if len(project_name) > 16:
        project_name_short = project_name[:13] + "..."
    else:
        project_name_short = project_name

    # Fill in title attributes
    title_ref.add_auto_attribs({'PROJEKT': f"{project_number} {project_name}",
                                'PLANINHALT': f"Schema Elektroverteilung {switchboard}",
                                'BLATTGROESSE': "A3+",
                                'CAD_DATEI': f"{project_number} {project_name_short} {switchboard}.dxf",
                                'PDF_DATEI': f"{project_number} {project_name_short} {switchboard}.pdf",
                                'INDEX': "0",
                                'DATUM': f"{get_datetime()[1]}",
                                'GEZEICHNET': "NB",
                                'GEPRUEFT': "--",
                                'BLATT_VON': "1 / 1",
                                'DRUECKDATUM': f"Drueckdatum: {' '.join(get_datetime())}"})

    # Insert logo
    scale = 1.32
    init_width, init_height = 23.49, 11.003
    init_x, init_y = 216.5, 23.5

    x = init_x - init_width * scale / 2
    y = init_y - init_height * scale / 2

    msp.add_blockref('LOGO', (x, y), dxfattribs={
        'xscale': scale,
        'yscale': scale})

    for number, value in enumerate(formatted_data):

        x_feed, y_feed = get_insert_point(number)
        # "Value" is a dict "item-key"
        value['q'] = "Q" + str(number + 1)
        if number < len(formatted_data) - 1:
            nb_ls_ref = msp.add_blockref('NB_LS', (x_feed, y_feed), dxfattribs={
                'xscale': 0.75,
                'yscale': 0.75})
            nb_ls_ref.add_auto_attribs(value)
        else:
            nb_en_ref = msp.add_blockref('NB_EN', (55, 96.875), dxfattribs={
                'xscale': 0.75,
                'yscale': 0.75})
            value['Q'] = "QX0"
            value['NAME'] = "EINSPEISUNG"
            value['DU'] = "dU=0%"
            nb_en_ref.add_auto_attribs(value)

    msp.add_line((55, 155), (x_feed - 16, 155), dxfattribs=style_electro)

    # Save the drawing.
    doc.saveas("output/template.dxf")
