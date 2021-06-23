import os
import json

import responder

from color_palette_generation import ColorPaletteGenerator
from color_extraction import ColorExtractor


env = os.environ
DEBUG = env['DEBUG'] in ['1', 'True', 'true']
ALGO = env.get('ALGO', 'kmeans')

cur_dir = os.path.dirname(__file__)
with open(os.path.join(cur_dir, 'color_extractor.json')) as fp:
    CONFIG = json.load(fp)

api = responder.API(debug=DEBUG)
generator = ColorPaletteGenerator()


@api.route("/")
async def generate(req, resp):
    body = await req.text
    color_palettes = generator.generate(
        json.loads(body).get('main')
    )
    resp.content = json.dumps(color_palettes)


@api.route("/colormaps")
async def colormaps(req, resp):
    cmaps = dict()

    cmaps['Perceptually Uniform Sequential'] = [
        'viridis', 'plasma', 'inferno', 'magma', 'cividis']

    cmaps['Sequential'] = [
        'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
        'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
        'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

    cmaps['Sequential (2)'] = [
        'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
        'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
        'hot', 'afmhot', 'gist_heat', 'copper']

    cmaps['Diverging'] = [
        'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
        'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

    cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']

    cmaps['Qualitative'] = ['Pastel1', 'Pastel2', 'Paired', 'Accent',
                            'Dark2', 'Set1', 'Set2', 'Set3',
                            'tab10', 'tab20', 'tab20b', 'tab20c']

    cmaps['Miscellaneous'] = [
        'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
        'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
        'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
        'gist_ncar']

    resp.content = json.dumps(cmaps)


@api.route("/colormap")
async def colormap(req, resp):
    body = await req.text
    data = json.loads(body)
    extractor = ColorExtractor(
        n_colors=data.get('colors'), algo=ALGO, **CONFIG[ALGO]
    )
    color_palette = extractor.extract(
        data.get('colormap')
    )
    resp.content = json.dumps(color_palette)


if __name__ == "__main__":
    api.run()
