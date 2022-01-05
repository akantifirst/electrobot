import ezdxf
from ezdxf import units, zoom
from ast import literal_eval as make_tuple
from common import csv_read


def get_insert_point(number):
    """Returns x, y coordinates."""
    x = 55 + number * 46
    y = 110
    return x, y


def gen_nb_ls(doc, style_electro, style_thin, style_boldline, style_name, style_std, style_q):
    # Create a block with the name 'NB_LS'
    nb_ls = doc.blocks.new(name='NB_LS')

    # Set millimeter as 'NB_LS' block units
    nb_ls.units = units.MM

    # Add DXF entities to the block 'NB_LS'.
    # The default base point (= insertion point) of the block is (0, 0).
    nb_ls.add_line((0, 19.5), (0, 0), dxfattribs=style_electro)  # point to contact
    nb_ls.add_line((0, 19.5), (-5, 28.5), dxfattribs=style_electro)  # contact
    nb_ls.add_line((-4.7, 22.7), (-2.5, 24), dxfattribs=style_electro)  # release
    nb_ls.add_line((0, 29), (0, 77.5), dxfattribs=style_electro)  # contact to feeder
    nb_ls.add_line((21, 85), (-21, 85), dxfattribs=style_boldline)  # horizontal under laying
    nb_ls.add_line((21, 91), (-21, 91), dxfattribs=style_thin)  # horizontal under length
    nb_ls.add_line((21, 97), (-21, 97), dxfattribs=style_thin)  # horizontal under cable
    nb_ls.add_line((21, 103), (-21, 103), dxfattribs=style_thin)  # horizontal under phi
    nb_ls.add_line((21, 109), (-21, 109), dxfattribs=style_thin)  # horizontal under power
    nb_ls.add_line((21, 115), (-21, 115), dxfattribs=style_thin)  # horizontal under name
    nb_ls.add_line((21, 123), (-21, 123), dxfattribs=style_boldline)  # horizontal on name
    nb_ls.add_line((-21, 85), (-21, 123), dxfattribs=style_boldline)  # vertical left
    nb_ls.add_line((0, 91), (0, 115), dxfattribs=style_thin)  # vertical center
    nb_ls.add_line((21, 85), (21, 123), dxfattribs=style_boldline)  # vertical right

    # Define hatch arrows and points
    hatch = nb_ls.add_hatch(color=5)
    hatch.paths.add_polyline_path([(-6, 22), (-4.75, 23.45), (-4.12, 22.35)], is_closed=True)
    hatch.paths.add_polyline_path([(0, 80), (-0.95, 77.25), (0.95, 77.25)], is_closed=True)
    hatch.paths.add_polyline_path([(-1, 0, -1), (1, 0, -1)], is_closed=True)

    # Define some attributes for the block 'NB_LS'
    nb_ls.add_attdef('NAME', dxfattribs=style_name).set_pos((0, 117.25), align='CENTER')
    nb_ls.add_attdef('POWER', dxfattribs=style_std).set_pos((-19, 110.75), align='LEFT')
    nb_ls.add_attdef('G', dxfattribs=style_std).set_pos((2, 110.75), align='LEFT')
    nb_ls.add_attdef('PHI', dxfattribs=style_std).set_pos((-19, 104.75), align='LEFT')
    nb_ls.add_attdef('VOLTAGE', dxfattribs=style_std).set_pos((2, 104.75), align='LEFT')
    nb_ls.add_attdef('CABLE', dxfattribs=style_std).set_pos((-19, 98.75), align='LEFT')
    nb_ls.add_attdef('SECTION', dxfattribs=style_std).set_pos((2, 98.75), align='LEFT')
    nb_ls.add_attdef('LENGTH', dxfattribs=style_std).set_pos((-19, 92.75), align='LEFT')
    nb_ls.add_attdef('DU', dxfattribs=style_std).set_pos((2, 92.75), align='LEFT')
    nb_ls.add_attdef('LAYING', dxfattribs=style_std).set_pos((0, 86.75), align='CENTER')
    nb_ls.add_attdef('CB', dxfattribs=style_std).set_pos((2.8, 32), align='LEFT')
    nb_ls.add_attdef('CB_TYPE', dxfattribs=style_std).set_pos((2.8, 26), align='LEFT')
    nb_ls.add_attdef('RELEASE', dxfattribs=style_std).set_pos((2.8, 20), align='LEFT')
    nb_ls.add_attdef('IB', dxfattribs=style_std).set_pos((2.8, 14), align='LEFT')
    nb_ls.add_attdef('Q', dxfattribs=style_q).set_pos((-2.8, 13), align='RIGHT')


def gen_title(doc, style_thin, style_boldline, style_title1, style_title2, style_title3, style_title4):
    title = doc.blocks.new(name='TITLE')
    gen_logo(title)
    # Set millimeter as 'NB_LS' block units
    title.units = units.MM

    # Add DXF entities to the block 'TITLE'.
    # The default base point (= insertion point) of the block is (0, 0).
    title.add_line((0, 0), (0, 30), dxfattribs=style_boldline)  # left vertical
    title.add_line((0, 30), (393, 30), dxfattribs=style_boldline)  # upper horizontal
    title.add_line((150, 30), (150, 6), dxfattribs=style_boldline)  # center left vertical
    title.add_line((150, 6), (243, 6), dxfattribs=style_boldline)  # center horizontal
    title.add_line((243, 6), (243, 30), dxfattribs=style_boldline)  # center right vertical
    title.add_line((0, 24), (150, 24), dxfattribs=style_thin)
    title.add_line((0, 18), (150, 18), dxfattribs=style_thin)
    title.add_line((0, 12), (150, 12), dxfattribs=style_thin)
    title.add_line((0, 6), (150, 6), dxfattribs=style_thin)
    title.add_line((12, 0), (12, 30), dxfattribs=style_thin)
    title.add_line((24, 0), (24, 30), dxfattribs=style_thin)
    title.add_line((36, 0), (36, 30), dxfattribs=style_thin)
    title.add_line((150, 0), (150, 6), dxfattribs=style_thin)
    title.add_line((243, 0), (243, 6), dxfattribs=style_thin)
    title.add_line((243, 24), (393, 24), dxfattribs=style_thin)
    title.add_line((243, 12), (393, 12), dxfattribs=style_thin)
    title.add_line((243, 6), (393, 6), dxfattribs=style_thin)
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

    # Draw main frame
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
    title.add_text('Art der Änderung', dxfattribs=style_title2).set_pos((93.0, 26.0), align='CENTER')
    title.add_text('Name', dxfattribs=style_title2).set_pos((30.0, 26.0), align='CENTER')
    title.add_text('Datum', dxfattribs=style_title2).set_pos((18.0, 26.0), align='CENTER')
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
    title.add_text('Dateiname', dxfattribs=style_title2).set_pos((196.5, 2.3), align='CENTER')

    title.add_attdef('PlANCODIERUNG', dxfattribs=style_title2).set_pos((244.5, 8.0), align='LEFT')
    title.add_attdef('DATEINAME', dxfattribs=style_title2).set_pos((244.5, 2.0), align='LEFT')
    title.add_attdef('BLATTGROESSE', dxfattribs=style_title3).set_pos((383.5, 25.75), align='CENTER')
    title.add_attdef('INDEX', dxfattribs=style_title4).set_pos((317.0, 1.5), align='CENTER')
    title.add_attdef('DATUM', dxfattribs=style_title2).set_pos((343.0, 2.0), align='CENTER')
    title.add_attdef('GEZEICHNET', dxfattribs=style_title2).set_pos((358.25, 2.0), align='CENTER')
    title.add_attdef('GEPRUEFT', dxfattribs=style_title2).set_pos((372.0, 2.0), align='CENTER')
    title.add_attdef('BLATT_VON', dxfattribs=style_title2).set_pos((385.5, 2.0), align='CENTER')
    title.add_attdef('PROJEKT', dxfattribs=style_title3).set_pos((308.75, 25.75), align='CENTER')
    title.add_attdef('PLANINHALT', dxfattribs=style_title3).set_pos((318.0, 18.0), align='CENTER')
    title.add_attdef('MODELNAME', dxfattribs=style_title2).set_pos((287.25, 8.0), align='CENTER')
    title.add_attdef('DATEINAME', dxfattribs=style_title2).set_pos((287.25, 2.3), align='CENTER')
    title.add_attdef('I1_AENDERUNG', dxfattribs=style_title2).set_pos((39.0, 20.0), align='LEFT')
    title.add_attdef('I1_DATUM', dxfattribs=style_title2).set_pos((18.0, 20.0), align='CENTER')
    title.add_attdef('I1_NAME', dxfattribs=style_title2).set_pos((30.0, 20.0), align='CENTER')
    title.add_attdef('INDEX1', dxfattribs=style_title2).set_pos((6.0, 20.0), align='CENTER')
    title.add_attdef('I2_AENDERUNG', dxfattribs=style_title2).set_pos((39.0, 14.0), align='LEFT')
    title.add_attdef('I2_DATUM', dxfattribs=style_title2).set_pos((18.0, 14.0), align='CENTER')
    title.add_attdef('I2_NAME', dxfattribs=style_title2).set_pos((30.0, 14.0), align='CENTER')
    title.add_attdef('INDEX2', dxfattribs=style_title2).set_pos((6.0, 14.0), align='CENTER')
    title.add_attdef('I3_AENDERUNG', dxfattribs=style_title2).set_pos((39.0, 8.0), align='LEFT')
    title.add_attdef('I3_DATUM', dxfattribs=style_title2).set_pos((18.0, 8.0), align='CENTER')
    title.add_attdef('I3_NAME', dxfattribs=style_title2).set_pos((30.0, 8.0), align='CENTER')
    title.add_attdef('INDEX3', dxfattribs=style_title2).set_pos((6.0, 8.0), align='CENTER')
    title.add_attdef('I4_DATUM', dxfattribs=style_title2).set_pos((18.0, 2.0), align='CENTER')
    title.add_attdef('I4_NAME', dxfattribs=style_title2).set_pos((30.0, 2.0), align='CENTER')
    title.add_attdef('INDEX4', dxfattribs=style_title2).set_pos((6.0, 2.0), align='CENTER')
    title.add_attdef('I4_AENDERUNG', dxfattribs=style_title2).set_pos((39.0, 2.0), align='LEFT')


def gen_logo(msp):
    # Load vector NB Logo coordinates
    data = csv_read(r'db/LOGO.csv')

    green_hatch = msp.add_hatch(color=136)
    gray_hatch = msp.add_hatch(color=252)

    for number, row in enumerate(data):
        print(number, row)
        row = [make_tuple(e) for e in row]
        print(number, row)
        if number == 0:
            green_hatch.paths.add_polyline_path(row, is_closed=True)
        else:
            if number < 11:
                gray_hatch.paths.add_polyline_path(row, is_closed=True)
            else:
                gray_hatch.paths.add_polyline_path(row, is_closed=True, flags=ezdxf.const.BOUNDARY_PATH_OUTERMOST)


def cad_write(formatted_data, project_info):
    # Create a new drawing in the DXF format of AutoCAD 2010
    doc = ezdxf.new('R2000', setup=True)

    # Set millimeter as document/modelspace units
    doc.units = units.MM

    # Add custom text style to the document
    doc.styles.new('isocpeur', dxfattribs={'font': 'ISOCPEUR.ttf'})
    doc.styles.new('arial', dxfattribs={'font': 'Arial.ttf'})

    # Define line and text styles
    style_name = {'height': 3.5, 'color': 5, 'style': 'isocpeur'}
    style_std = {'height': 2.5, 'color': 251, 'style': 'isocpeur'}
    style_q = {'height': 4, 'color': 5, 'style': 'isocpeur'}
    style_title1 = {'height': 1.45, 'color': 7, 'style': 'arial'}
    style_title2 = {'height': 2.0, 'color': 7, 'style': 'arial'}
    style_title3 = {'height': 2.5, 'color': 7, 'style': 'arial'}
    style_title4 = {'height': 3.0, 'color': 7, 'style': 'arial'}
    style_boldline = {'lineweight': 40, 'color': 7}
    style_electro = {'lineweight': 50, 'color': 5}
    style_thin = {'lineweight': 0, 'color': 7}
    gen_title(doc, style_thin, style_boldline, style_title1, style_title2, style_title3, style_title4)
    gen_nb_ls(doc, style_electro, style_thin, style_boldline, style_name, style_std, style_q)

    # define modelspace
    msp = doc.modelspace()
    zoom.extents(msp)

    msp.add_lwpolyline(((0, 0), (0, 297), (420, 297), (420, 0)))
    blockref1 = msp.add_blockref('TITLE', (20, 7))
    blockref1.add_auto_attribs({'PROJEKT': project_info})
    for number, value in enumerate(formatted_data):
        # values is a dict with the attribute tag as item-key and
        # the attribute text content as item-value.
        name, power, g, phi, voltage, cable, section, length, du, laying, cb, cb_type, release, ib = value
        point = get_insert_point(number)
        values = {
            'NAME': name,
            'POWER': power,
            'G': g,
            'PHI': phi,
            'VOLTAGE': voltage,
            'CABLE': cable,
            'SECTION': section,
            'LENGTH': length,
            'DU': du,
            'LAYING': laying,
            'CB': cb,
            'CB_TYPE': cb_type,
            'RELEASE': release,
            'IB': ib,
            'Q': "Q" + str(number + 1),
        }

        blockref = msp.add_blockref('NB_LS', point, dxfattribs={
                                    'xscale': 0.75,
                                    'yscale': 0.75})
        blockref.add_auto_attribs(values)

    # Save the drawing.
    doc.saveas("output/template.dxf")
