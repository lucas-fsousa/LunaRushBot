
def save_logs(message, method_name=''):
    """
    :param message: Detailed message to display in console and log file - type[string / fstring]
    :type message: str
    :param method_name: Name of the method where the log save routine is being called
    :type method_name: str
    """
    from datetime import datetime as dt

    str_message = f'{dt.now().date()} - {dt.now().time().replace(microsecond=0)} - '
    if method_name != '':
        str_message += f'ERROR IN {method_name} - DETAILS: {message}'
    else:
        str_message += f'INFORMATION - DETAILS: {message}'

    file = open('logs/application.log', 'a')
    file.write(f'{str_message}\n')
    file.close()
    print(f'{str_message}')


def locate_all_images(path_images, confidence=0.8):
    from pyautogui import locateAllOnScreen
    from time import time
    from os import listdir

    all_coord = []
    try:
        list_images = listdir(path_images)
        if list_images.__len__() < 1:
            save_logs('no images were found to read in the source folder')
        else:
            for image in list_images:
                img = path_images + image
                start = time()
                end = time().__add__(3)
                while start < end:
                    boxes = locateAllOnScreen(img, confidence=confidence)
                    for box in boxes:
                        all_coord.append(box)
                    start = time()
                continue
    except Exception as ex:
        save_logs(f'{ex}', 'locate all images')
    finally:
        return all_coord


def locate_single_image(path_images, confidence=0.9, region=None, return_xy=True):
    """
    :param path_images: path where the images are located
    :type path_images: str
    :param return_xy: key for return type, if true, return X and Y coordinates,
    if false, return image region (x, y, width, height)
    :type return_xy: bool
    :param region: screen region to search for the informed image
    :type region: tuple
    :param confidence: how confident the bot must be to identify the image as real [min: 0.1 / max: 1]
    :type confidence: float
    :return: point x, point y
    :rtype: tuple
    """
    from pyautogui import locateOnScreen, center
    from time import time
    from os import listdir

    coordinates = None
    try:
        list_images = listdir(path_images)
        if list_images.__len__() < 1:
            save_logs('no images were found to read in the source folder')
            return coordinates

        for image in list_images:
            img = path_images + image
            start = time()
            end = time().__add__(2)
            while start < end:
                coordinates = locateOnScreen(img, confidence=confidence, region=region)
                if coordinates is not None:
                    if return_xy:
                        coordinates = center(coordinates)
                    return coordinates
                start = time()
            continue
    except Exception as ex:
        save_logs(f'{ex}', 'locate single image')


# hover over center of home screen
def get_center_screen():
    """
    :return: Check main screen size and move mouse pointer to center
    :rtype: None
    """
    from pyautogui import moveTo, size
    moveTo((size().width / 2), (size().height / 2))


# generic instruction to find an RGB color pattern that matches input values
def get_position_by_color(rgb, start_pos_x, start_pos_y, end_width=0, end_height=0):
    """
    The method reads the screen pixel by pixel until it finds the given RGB hue.
    it is necessary to inform the starting point X and Y for the reading to be carried out.
    If there is a limitation for the search, you can use the optional parameters end_width and end_height
    to define how far the search will be performed.

    :param rgb: rgb color tone
    :type rgb: tuple
    :param start_pos_x: represents the width of the screen in pixels where the color reading will start
    :type start_pos_x: int
    :param start_pos_y: represents the height of the screen in pixels where the color reading will start
    :type start_pos_y: int
    :param end_width: optional parameter that represents up to what point of the width the color reading will be
    performed
    :type end_width: int
    :param end_height: optional parameter that represents up to what point the color reading will be performed
    :type end_height: int
    :return: the return is the movement of the mouse to the point where the RGB color was located
    :rtype: None
    """
    from App.Objects.externalConfigs import ExternalConfigs
    from pyautogui import moveTo, screenshot

    success = False
    config = ExternalConfigs()
    try:
        sc = screenshot()
        wid, hei = sc.size
        r, g, b = rgb
        if end_width > 0 and end_height > 0:
            wid = start_pos_x + end_width
            hei = start_pos_y + end_height
        else:
            wid = wid - 70  # ignore 65px at end screen width
            hei = hei - 70  # ignore 65px at end screen height
        for x in range(start_pos_x, wid, 1):
            for y in range(start_pos_y, hei, 1):
                r_temp, g_temp, b_temp = sc.getpixel((x, y))
                if r == r_temp and g == g_temp and b == b_temp:
                    moveTo(x, y, config.MouseDelay)
                    success = True
                    break
            if success:
                break
    except Exception as ex:
        save_logs(f'unexpected error while fetching image: {ex}', 'get_position_of_color')
        get_center_screen()
    finally:
        return success


def click(return_only=False):
    """
    Action to use the mouse click instruction for both left mouse click and inverted mouse click for right mouse click
    :param return_only: if true it will only return the string referring to the click / left or right button
    :type return_only: bool
    :return: returns a string with current/left or right click button
    :rtype: str
    """
    from App.Objects.externalConfigs import ExternalConfigs
    from pyautogui import click, rightClick

    config = ExternalConfigs()

    button = 'left'
    try:
        if config.InvertedMouse:
            button = 'right'

        if not return_only:
            if config.InvertedMouse:
                rightClick()
            else:
                click()
    except Exception as ex:
        save_logs(f'fails while trying to click > {ex}', 'click')
    finally:
        return button


def scroll_page(xy, clicks=100, reverse=False, duration=1):
    """
    :param xy: x,y position where the mouse should be moved
    :type xy: tuple
    :param clicks: scroll size
    :type clicks: int
    :param reverse: defines whether the scroll will be standard or inverted [up > down] or [down > up]
    :type reverse: bool
    :param duration: scroll duration
    :type duration: float
    :return: None
    """
    from pyautogui import drag, moveTo
    from App.Objects.externalConfigs import ExternalConfigs

    config = ExternalConfigs()
    try:
        x, y = xy
        moveTo(x, y, config.MouseDelay)
        if not reverse:
            drag(None, clicks, duration, button=click(return_only=True))
        else:
            drag(None, -clicks, duration, button=click(return_only=True))
    except Exception as ex:
        save_logs(f'failed while trying to scroll the page > {ex}', 'scroll_page')


def compare_images(img01, img02):
    import cv2

    orb = cv2.ORB_create()
    kpa, desc_a = orb.detectAndCompute(img01, None)
    kpb, desc_b = orb.detectAndCompute(img02, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc_a, desc_b)
    regions_equals = [i for i in matches if i.distance < 50]
    if len(matches) == 0:
        return 0
    return len(regions_equals) / len(matches)


def move_to_by_percent(perc_x, perc_y):
    from pyautogui import moveTo, size, position

    x, y = position()
    w, h = size()  # get the screen size

    # calculate to get percentage of current screen size
    if perc_x != 0:
        perc_x = w * perc_x / 100
        x += perc_x
    else:
        x -= perc_x

    if perc_y != 0:
        perc_y = h * perc_y / 100
        y += perc_y
    else:
        y -= perc_y

    #
    if x < 0:
        x = 1
    elif x > w:
        x = w - 100

    if y < 0:
        y = 1
    elif y > h:
        y = h - 100

    # moves the mouse cursor to the indicated position
    moveTo(x, y)
