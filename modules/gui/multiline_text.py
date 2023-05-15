import pygame as pg
import itertools

GLASS = (0,0,0,0)
BLACK = (0,0,0)

def flatten_list(nested_list):
    """
    Flattens a list of lists using itertools.chain.

    Args:
        nested_list: A list of lists to be flattened.

    Returns:
        A flattened list.
    """
    return list(itertools.chain.from_iterable(nested_list))

def CoolMultilineText(text, max_width, font):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if font.size(current_line + word)[0] < max_width:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "

    line = "".join([i + "\n" for i in lines])

    return font.render(line, True, "black")


def DivideCharacters(text,max_width,font,by_char=False):
    words = text.split()
    if by_char:
        words = list(text)

    lines = []
    current_line = ""

    for word in words:
        if font.size(current_line + word)[0] < max_width:
            current_line += word
        else:
            lines.append(current_line)
            current_line = word

    # Add the last line
    lines.append(current_line)

    return lines





def MultilineText(text, max_width, font,by_char=False):
    words = text.split()
    if by_char:
        words = list(text)

    lines = []
    current_line = ""

    for word in words:
        if font.size(current_line + word)[0] < max_width:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "

    # Add the last line
    lines.append(current_line)

    # Render each line as a separate surface
    surfaces = [font.render(line, True, BLACK) for line in lines]

    # Determine the height of the final surface
    height = sum([surface.get_height() for surface in surfaces])

    # Create the final surface and blit the lines onto it
    final_surface = pg.Surface((max_width, height)).convert_alpha()
    final_surface.fill(GLASS)

    y = 0
    for surface in surfaces:
        final_surface.blit(surface, (0, y))
        y += surface.get_height()

    return final_surface

def UltimateMultilineText(text, max_width, font,bg=None):
    if bg is None:
        bg = GLASS

    words = [
        DivideCharacters(i,max_width,font,True) for i in text.split()
    ]

    words = flatten_list(words)

    lines = []
    current_line = ""

    for word in words:
        if font.size(current_line + word)[0] < max_width:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "

    # Add the last line
    lines.append(current_line)

    # Render each line as a separate surface
    surfaces = [font.render(line, True, BLACK) for line in lines]

    # Determine the height of the final surface
    height = sum([surface.get_height() for surface in surfaces])

    # Create the final surface and blit the lines onto it
    final_surface = pg.Surface((max_width, height)).convert_alpha()
    final_surface.fill(bg)

    y = 0
    for surface in surfaces:
        final_surface.blit(surface, (max_width/2 - surface.get_width()/2, y))
        y += surface.get_height()

    return final_surface