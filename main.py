#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

import logging

from math import ceil
from typing import List, Iterator, Tuple

from drawSvg import Drawing, Circle, ArcLine

SVG_OUTPUT: str = 'output.svg'

def generate_arcs(radius: int, start_deg: int, arc_deg: int, interval_deg: int, stroke_width: int, color: str) -> List[ArcLine]:
    logger = logging.getLogger('generate_arcs')
    ret = []
    common_args = {
        'stroke': color,
        'stroke_width': stroke_width,
        'fill': '#00000000',
    }
    start_deg1 = start_deg % 360
    end_deg1 = (start_deg1 + arc_deg) % 360
    start_deg2 = (end_deg1 + interval_deg) % 360
    end_deg2 = (start_deg2 + arc_deg) % 360
    logger.info('ArcLine stroke width: {}'.format(stroke_width))
    logger.info('Generating ArcLine 1 at {}: {} to {}'.format(radius, start_deg1, end_deg1))
    logger.info('Generating ArcLine 2 at {}: {} to {}'.format(radius, start_deg2, end_deg2))
    ret.append(ArcLine(0, 0, radius, start_deg1, end_deg1, **common_args))
    ret.append(ArcLine(0, 0, radius, start_deg2, end_deg2, **common_args))
    return ret;


def generate(arcs: Iterator[Tuple[int, int, int, int, int, str]]) -> Drawing:
    logger = logging.getLogger('generate')
    ret = Drawing(512, 512, origin='center')
    # Add background
    ret.append(Circle(0, 0, 256, fill='#000000FF'))

    # Arcs
    for (r, s, a, i, w, c) in arcs:
        logger.info('Generating arc at {}'.format(r))
        for arc in generate_arcs(r, s, a, i, w, c):
            ret.append(arc)

    return ret;


def uniform_generator(start_radius: int, end_radius: int, interval: int, num_arcs: int, color: str) -> Iterator[Tuple[int, int, int, int, int, str]]:
    total_width = end_radius - start_radius
    interval_width = interval * (num_arcs - 1)
    arc_width = ceil((total_width - interval_width) / num_arcs)
    half_width = arc_width // 2
    for i in range(start_radius + half_width, end_radius + half_width, arc_width + interval):
        yield (int(i), 155, 120, 60, arc_width, color)
    return None

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Saving SVG to {}'.format(SVG_OUTPUT))
    generate(uniform_generator(85, 185, 0, 3, '#DEDEDEFF')).saveSvg(SVG_OUTPUT)
