import ezdxf
from ezdxf import units


def get_insert_point(number):
    """Returns x, y coordinates."""
    x = 52 + number * 46
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


def gen_title(doc, style_thin, style_boldline, style_title1):
    title = doc.blocks.new(name='TITLE')

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

    # add constant text entities
    title.add_text('Index', dxfattribs=style_title1).set_pos((2, 104.75), align='MIDDLE CENTER')


def cad_write(formatted_data):
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
    # style_title = {'height': 2, 'color': 5, 'style': 'arial'}
    style_boldline = {'lineweight': 50, 'color': 7}
    style_electro = {'lineweight': 50, 'color': 5}
    style_thin = {'lineweight': 0, 'color': 5}

    gen_nb_ls(doc, style_electro, style_thin, style_boldline, style_name, style_std, style_q)

    # define modelspace
    msp = doc.modelspace()

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

        blockref = msp.add_blockref('NB_LS', point)
        blockref.add_auto_attribs(values)

    # Save the drawing.
    doc.saveas("output/template.dxf")
