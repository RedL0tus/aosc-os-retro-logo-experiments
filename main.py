#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

import logging

from math import ceil
from typing import List, Iterator, Tuple
from argparse import ArgumentParser

from drawSvg import Drawing, Circle, Path


SVG_OUTPUT: str = 'output.svg'


def generate_arc_path(radius: int, width: int, start_deg: int, end_deg: int, color: str) -> Path:
    half_width = ceil(width / 2)
    center_radius = radius + half_width
    ret = Path(stroke=color, stroke_width=width)
    ret.arc(0, 0, center_radius, start_deg, end_deg)
    ret.arc(0, 0, center_radius, end_deg, start_deg, cw=True, includeL=True)
    ret.Z()
    return ret


def generate_arcs(radius: int, start_deg: int, arc_deg: int, interval_deg: int, stroke_width: int, color: str) -> List[Path]:
    logger = logging.getLogger('generate_arcs')
    ret = []
    start_deg1 = start_deg % 360
    end_deg1 = (start_deg1 + arc_deg) % 360
    start_deg2 = (end_deg1 + interval_deg) % 360
    end_deg2 = (start_deg2 + arc_deg) % 360
    logger.info('ArcLine stroke width: {}'.format(stroke_width))
    logger.info('Generating ArcLine 1 at {}: {} to {}'.format(radius, start_deg1, end_deg1))
    logger.info('Generating ArcLine 2 at {}: {} to {}'.format(radius, start_deg2, end_deg2))
    ret.append(generate_arc_path(radius, stroke_width, start_deg1, end_deg1, color))
    ret.append(generate_arc_path(radius, stroke_width, start_deg2, end_deg2, color))
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
    parser = ArgumentParser()
    parser.add_argument('interval')
    parser.add_argument('num_arcs')
    parser.add_argument('-c', '--color', default='#DEDEDE')
    parser.add_argument('-s', '--start_radius', default=85)
    parser.add_argument('-e', '--end_radius', default = 185)
    parser.add_argument('-o', '--output', default=SVG_OUTPUT)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Saving SVG to {}'.format(args.output))
    generate(uniform_generator(int(args.start_radius), int(args.end_radius), int(args.interval), int(args.num_arcs), args.color)).saveSvg(args.output)
