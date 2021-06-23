import colorsys

import numpy as np


def hex_to_rgb(hex_):
    hex_ = hex_.lstrip('#')
    hlen = len(hex_)
    return tuple(int(
        hex_[i:i+int(hlen/3)], 16
    ) for i in range(0, hlen, int(hlen/3)))


def rgb_to_hex(rgb):
    def fill_zero(val):
        return f'0{val}' if len(val) < 4 else val
    return'#{}{}{}'.format(*[fill_zero(hex(c)) for c in rgb]).replace(
        '0x', ''
    )


def rgb_to_hsv(rgb):
    max_rgb = 255.0
    r, g, b = tuple(rgb)
    return colorsys.rgb_to_hsv(
        r / max_rgb,
        g / max_rgb,
        b / max_rgb
    )


def hsv_to_rgb(hsv):
    max_rgb = 255
    raw_rgb = np.array(colorsys.hsv_to_rgb(*hsv)).astype(int)
    return tuple(max_rgb * raw_rgb)


def hex_to_hsv(hex):
    return rgb_to_hsv(hex_to_rgb(hex))


def hsv_to_hex(hsv):
    return rgb_to_hex(hsv_to_rgb(hsv))


class ColorPaletteGenerator:

    def __init__(self):
        self._hue_unit = 1.0 / 24

    def _adjust_hue(self, h):
        int_part = h // 1
        return h - int_part

    def _rotate_hue(self, hsv, val):
        return (
            self._adjust_hue(hsv[0] + val),
            hsv[1],
            hsv[2]
        )

    def _generate_opponent(self, hsv):
        return [
            hsv_to_hex(self._rotate_hue(
                hsv,
                n * self._hue_unit
            )) for n in [
                0,
                8, 9, 10,
                14, 15, 16
            ]
        ]

    def _generate_tetrad(self, hsv):
        return [
            hsv_to_hex(self._rotate_hue(
                hsv,
                n * self._hue_unit
            )) for n in [
                0,
                6,
                12,
                18
            ]
        ]

    def _generate_analogy(self, hsv):
        return [
            hsv_to_hex(self._rotate_hue(
                hsv,
                n * self._hue_unit
            )) for n in [
                0, 1, 2, 22, 23
            ]
        ]

    def _generate_split_complementary(self, hsv):
        return [
            hsv_to_hex(self._rotate_hue(
                hsv,
                n * self._hue_unit
            )) for n in [
                0,
                11,
                13
            ]
        ]

    def _generate_pentad(self, hsv):
        return [
            hsv_to_hex(self._rotate_hue(
                hsv,
                h
            )) for h in [
                0,
                0.2,
                0.4,
                0.6,
                0.8
            ]
        ]

    def _generate_intermediate(self, hsv):
        return [
            hsv_to_hex(self._rotate_hue(
                hsv,
                n * self._hue_unit
            )) for n in [
                0,
                6,
                18
            ]
        ]

    def _generate_triad(self, hsv):
        return [
            hsv_to_hex(self._rotate_hue(
                hsv,
                n * self._hue_unit
            )) for n in [
                0,
                8,
                16
            ]
        ]

    def _generate_hexad(self, hsv):
        return [
            hsv_to_hex(self._rotate_hue(
                hsv,
                n * self._hue_unit
            )) for n in [
                0,
                4,
                8,
                12,
                16,
                20
            ]
        ]

    def _generate_dyad(self, hsv):
        return [
            hsv_to_hex(self._rotate_hue(
                hsv,
                n * self._hue_unit
            )) for n in [
                0,
                12
            ]
        ]

    def generate(self, color_code):
        hsv = rgb_to_hsv(hex_to_rgb(color_code))
        return dict(
            opponent=self._generate_opponent(hsv),
            tetrad=self._generate_tetrad(hsv),
            analogy=self._generate_analogy(hsv),
            split_complementary=self._generate_split_complementary(hsv),
            pentad=self._generate_pentad(hsv),
            intermidiate=self._generate_intermediate(hsv),
            triad=self._generate_triad(hsv),
            hexad=self._generate_hexad(hsv),
            dyad=self._generate_dyad(hsv)
        )
