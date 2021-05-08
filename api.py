import os
import json

import responder

from color_palette_generation import ColorPaletteGenerator


env = os.environ
DEBUG = env['DEBUG'] in ['1', 'True', 'true']

api = responder.API(debug=DEBUG)
generator = ColorPaletteGenerator()


@api.route("/")
async def generate(req, resp):
    body = await req.text
    color_palettes = generator.generate(
        json.loads(body).get('main')
    )
    resp.content = json.dumps(color_palettes)


if __name__ == "__main__":
    api.run()
