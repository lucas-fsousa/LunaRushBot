def search_for_rgb(rgb, to_click=True, start_x=0, start_y=0):
    """
    Do a search for a specific RGB color on the main screen and if found,
    the mouse cursor is moved to the meeting point. Returns boolean true for found and false for not found
    :param rgb: represents the RED - GREEN - BLUE color standard
    :type rgb: tuple
    :param to_click: checks whether to click on the item when locating it
    :type to_click: bool
    :param start_x: X start position to start searches
    :type start_x: int
    :param start_y: Y start position to start searches
    :type start_y: int
    :return: returns boolean true if found and false for not found
    :rtype: bool
    """
    from App import Routines as routines
    from App.Objects.externalConfigs import ExternalConfigs
    success = False
    try:
        r, g, b = rgb
        config = ExternalConfigs()
        for _try in range(0, config.Attempts, 1):
            if routines.get_position_by_color((r, g, b), start_x, start_y):
                success = True
                if to_click:
                    routines.click()
                break
    except Exception as ex:
        routines.save_logs(f'Oops, something went wrong {ex}', 'find search_for_rgb')
    finally:
        return success


# noinspection PyMethodMayBeStatic
class Find:
    def __init__(self):
        self.BossCardBattleNoAvailable = 'images/5_boss_card_battle_no_available/'
        self.BossCardBattleAvailable = 'images/4_boss_card_battle_available/'
        self.MetamaskConnectBtn = 'images/1_metamask_connect/'
        self.ScreenFightResult = 'images/8_fight_result/'
        self.HeroEnergyOnIcon = 'images/10_hero_energy_on/'
        self.ScreenBossFight = 'images/9_fight_screen/'
        self.SignMetamaskBtn = 'images/2_sign_metamask/'
        self.BossHuntAvatar = 'images/3_hunt_boss/'
        self.StartFightBtn = 'images/7_start_fight_btn/'
        self.HeroesList = 'images/6_hero_list/'
        self.RemoveHero = 'images/11_remove_hero/'
        self.AfkBtn = 'images/12_afk_btn/'

    def search_for_image(self, images_path, to_click=True, confidence=0.9, return_xy=True):
        """
        Search for a user-specified image on the main computer screen
        :param images_path: references a path that contains a list of images
        :type images_path: str
        :param return_xy: checks if the return should be coordinate (x, y) or boxed with (x, y, width, height)
        :type return_xy: bool
        :param to_click: checks if it is necessary to click the item when locating
        :type to_click: bool
        :param confidence: how confident should you be to accept the result
        :type confidence: float
        :return: returns a tuple containing the X and Y value of the location where the image was found or None for not
        found
        :rtype: tuple
        """
        from pyautogui import moveTo, center
        from App import Routines as routines
        from App.Objects.externalConfigs import ExternalConfigs

        coord = None
        config = ExternalConfigs()
        try:
            for _try in range(0, config.Attempts, 1):
                path = images_path
                coord = routines.locate_single_image(path, confidence, return_xy=return_xy)
                if coord is not None:
                    if to_click:
                        if return_xy:
                            x, y = coord
                            moveTo(x, y, config.MouseDelay)
                            routines.click()
                        else:
                            x, y = center(coord)
                            moveTo(x, y, config.MouseDelay)
                            routines.click()
                    break
        except Exception as ex:
            routines.save_logs(f'Oops, something went wrong {ex}', 'find search_for_image')
        finally:
            return coord

    def search_for_all_images(self, images_path, confidence=0.9):
        """
        Search for a user-specified image on the main computer screen
        :param images_path: references a path that contains a list of images
        :type images_path: str
        :param confidence: how confident should you be to accept the result
        :type confidence: float
        :return: returns a list containing the group of X and Y value of the location where the image
         was found or None for not
        :rtype: list
        """
        from App import Routines as routines
        from pyautogui import center
        all_coord = []
        try:
            list_box = routines.locate_all_images(images_path, confidence)
            if list_box.__len__() > 0:
                for coord in list_box:
                    x, y = center(coord)
                    all_coord.append((x, y))
        except Exception as ex:
            routines.save_logs(f'Oops, something went wrong {ex}', 'find search for all images')
        finally:
            return all_coord

    def locate_next(self, image_path, increment_x=0, increment_y=0, decrement_x=0, decrement_y=0):
        """
            reads the screen and finds the next image from the point where the mouse cursor is
            :param image_path: address of the folder where the image is located
            :type image_path: str
            :param increment_x: increments the value of X where the mouse cursor is to change its position if necessary
            :type increment_x: int
            :param increment_y: increments the value of Y where the mouse cursor is to change its position if necessary
            :type increment_y: int
            :param decrement_x: decrements the value of X where the mouse cursor is to change its position if necessary
            :type decrement_x: int
            :param decrement_y: decrements the value of Y where the mouse cursor is to change its position if necessary
            :type decrement_y: int
            :return: returns a tuple containing the frame of the image (x, y, width, height)
            :rtype: tuple
        """
        from App import Routines as routines
        from pyautogui import position, size, moveTo
        from App.Objects.externalConfigs import ExternalConfigs

        config = ExternalConfigs()
        x, y = position()
        if increment_x > 0:
            x += increment_x

        if increment_y > 0:
            y += increment_y

        if decrement_x > 0:
            x -= decrement_x

        if decrement_y > 0:
            y -= decrement_y

        moveTo(x, y, config.MouseDelay)
        x, y = position()
        width, height = size()
        width -= x
        height -= y
        return routines.locate_single_image(image_path, region=(x, y, width, height), return_xy=False)
