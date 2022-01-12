import math
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import ezdxf
from ezdxf.addons.drawing import Properties, RenderContext, Frontend
from ezdxf.addons.drawing.backend import prepare_string_for_rendering
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.properties import LayoutProperties
from ezdxf.addons.drawing.config import Configuration
from ezdxf.math import Matrix44

# TODO:
#   resolve font scaling problem


class CustomBackend(MatplotlibBackend):
    def __init__(
            self,
            ax: plt.Axes,
            text_size_scale: float = 1,
            *,
            adjust_figure: bool = True,
            font: FontProperties = FontProperties(),
    ):
        self._text_size_scale = text_size_scale
        super().__init__(ax, adjust_figure=adjust_figure, font=font, use_text_cache=False)

    def draw_text(
            self,
            text: str,
            transform: Matrix44,
            properties: Properties,
            cap_height: float,
    ):
        if not text.strip():
            return  # no point rendering empty strings
        font_properties = self.get_font_properties(properties.font)
        assert self.current_entity is not None
        text = prepare_string_for_rendering(text, self.current_entity.dxftype())
        scale = self._text_renderer.get_scale(cap_height, font_properties)
        text_transform = Matrix44.scale(scale) @ transform
        x, y, _, _ = text_transform.get_row(3)
        scale = math.sqrt(sum(i * i for i in text_transform.get_row(0)))
        self.ax.text(
            x, y, text.replace('$', '\\$'),
            color=properties.color, size=1.161 * scale * self._text_size_scale, in_layout=True,
            fontproperties=font_properties, transform_rotates_text=True, zorder=self._get_z()
        )


def generate_pdf(input_dxf, output_pdf):
    config = Configuration.defaults()
    try:
        doc = ezdxf.readfile(input_dxf)
        layout = doc.modelspace()
        ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = '#FFFFFF'
        fig: plt.Figure = plt.figure(frameon=False)
        ax: plt.Axes = fig.add_axes((0, 0, 1, 1))
        ax.margins(0, 0)
        ctx = RenderContext(layout.doc)
        layout_properties = LayoutProperties.from_layout(layout)

        out = CustomBackend(ax)
        Frontend(ctx, out,
                 config=config.with_changes(
                     lineweight_scaling=1.5,
                     min_lineweight=0.2)).draw_layout(
                layout,
                finalize=True,
                layout_properties=layout_properties,
                )
        fig.savefig(
            output_pdf, dpi=72, facecolor=ax.get_facecolor()
        )
        plt.close(fig)
    except IOError:
        print("File system related error")
