from os import path, mkdir
from App.Objects.externalConfigs import ExternalConfigs
from App import Cache as cache
from App.Find import Find
import random
from App import Routines as routines
from pyautogui import keyDown, keyUp, press, scroll, position, moveTo, password
from time import sleep, time
from App.Objects.globalsVar import GlobalVar

gv = GlobalVar()


def reset_page():  # refresh browser page
    """
    responsible for applying a common page reset (Ctrl+f5)
    :return: None
    """
    routines.save_logs('updating current page...')
    routines.get_center_screen()
    keyDown("ctrl")
    press(["f5", "f5"])
    keyDown("f5")
    keyUp("f5")
    keyUp("Ctrl")
    sleep(10)
    keyDown("ctrl")
    keyUp("Ctrl")


def startup():
    config = ExternalConfigs()

    if not path.exists('logs'):
        mkdir('logs')

    # reset logs on start
    if config.ResetLogsOnStart:
        file = open(r'logs/application.log', "w")
        file.write("")
        file.close()

    # check if the folders already exist on the system
    if not path.exists('cache'):
        mkdir('cache')

    if not path.exists('images'):
        mkdir('images')

    if not path.exists('images/1_metamask_connect'):
        mkdir('images/1_metamask_connect')

    if not path.exists('images/2_sign_metamask'):
        mkdir('images/2_sign_metamask')

    if not path.exists('images/3_hunt_boss'):
        mkdir('images/3_hunt_boss')

    if not path.exists('images/4_boss_card_battle_available'):
        mkdir('images/4_boss_card_battle_available')

    if not path.exists('images/5_boss_card_battle_no_available'):
        mkdir('images/5_boss_card_battle_no_available')

    if not path.exists('images/6_hero_list'):
        mkdir('images/6_hero_list')

    if not path.exists('images/7_start_fight_btn'):
        mkdir('images/7_start_fight_btn')

    if not path.exists('images/8_fight_result'):
        mkdir('images/8_fight_result')

    if not path.exists('images/9_fight_screen'):
        mkdir('images/9_fight_screen')

    if not path.exists('images/10_hero_energy_on'):
        mkdir('images/10_hero_energy_on')

    if not path.exists('images/11_remove_hero'):
        mkdir('images/11_remove_hero')

    if not path.exists('images/12_afk_btn'):
        mkdir('images/12_afk_btn')

    return True


def initialize_connect_game():
    config = ExternalConfigs()
    find = Find()
    routines.save_logs('starting login process')
    if find.search_for_image(find.MetamaskConnectBtn):
        sleep(config.DefaultDelay)

        timeout = time().__add__(config.Timeout)
        while timeout > time():
            if find.search_for_image(find.SignMetamaskBtn):
                return True
            sleep(1)
    return False


def get_random_of_xy(x, y):
    """
    generates a "random" value for the X and for the Y and returns both values slightly
    modified to avoid detection by ant-bots
    :param x: X's position relative to the screen
    :type x: int
    :param y: Y position relative to screen
    :type y: int
    :return: returns a tuple with new values of X and Y
    :rtype: tuple
    """
    new_x = random.randint(0, 10)
    new_y = random.randint(0, 10)

    if new_x < 5:
        x = x - new_x
    else:
        x = x + new_x

    if new_y < 5:
        y = y - new_y
    else:
        y = y + new_y

    return x, y


def identify_page():
    config = ExternalConfigs()
    find = Find()
    # check current screen
    routines.save_logs('identifying current game screen')
    while True:

        if find.search_for_image(find.MetamaskConnectBtn, to_click=False) is not None:
            routines.save_logs('localized game connection page')
            return 'start_game_page'

        elif find.search_for_image(find.BossHuntAvatar, to_click=False) is not None:
            routines.save_logs('game homepage located')
            return 'game_home_page'

        # elif find.search_for_image(find.ScreenBossFight, to_click=False) is not None:
        #     routines.save_logs('boss fight screen located')
        #     return 'screen_boss_fight'

        elif find.search_for_image(find.BossCardBattleAvailable, to_click=False) is not None:  # AVAILABLE PT 1
            routines.save_logs('boss selection screen located')
            return 'screen_boss_cards'

        elif find.search_for_image(find.BossCardBattleNoAvailable, to_click=False) is not None:  # AVAILABLE P T
            routines.save_logs('boss selection screen located')
            return 'screen_boss_cards'

        elif find.search_for_image(find.StartFightBtn, to_click=False) is not None:
            routines.save_logs('hero selection screen located')
            return 'screen_heroes'
        else:
            routines.save_logs('no known pages were found. Trying again.')
            reset_page()
            sleep(config.ConnectionScreen)


def game_navigation():
    find = Find()
    config = ExternalConfigs()
    success = True
    next_page = None
    safe_reset_game_page = time().__add__(config.SafeResetGamePage)
    try:
        while success and safe_reset_game_page > time():
            if next_page is None:
                next_page = identify_page()
                sleep(config.TransitionDelay)

            routines.save_logs('waiting for response from target screen')
            if next_page == 'start_game_page':
                if not initialize_connect_game():
                    success = False
                next_page = 'game_home_page'
                sleep(config.TransitionDelay)

            if success:
                if next_page == 'game_home_page':
                    routines.save_logs('entering the boss hunt module')
                    if find.search_for_image(find.BossHuntAvatar) is None:
                        success = False
                    next_page = 'screen_boss_cards'
                    sleep(config.TransitionDelay)

            if success:
                if next_page == 'screen_boss_cards':
                    timeout = time().__add__(config.Timeout * 3)
                    _next = False
                    routines.save_logs('looking for a boss fight card that is available')
                    while not _next and timeout > time():
                        if find.search_for_image(find.BossCardBattleAvailable):
                            _next = True
                        else:
                            # get the screen location position
                            x, y = find.search_for_image(find.BossCardBattleNoAvailable, to_click=False)
                            if x is not None and y is not None:
                                moveTo(x, y, config.MouseDelay)
                                sleep(1)
                                scroll(500)
                                sleep(1)
                    if _next:
                        routines.save_logs('boss battle card located')
                        next_page = 'screen_heroes'
                        sleep(config.TransitionDelay)
                    else:
                        continue

            if success:
                if next_page == 'screen_heroes':
                    success = hero_screen_management()
                    if success:
                        next_page = 'screen_boss_fight'
                    else:
                        next_page = None
                    sleep(config.TransitionDelay)

            if success:
                if next_page == 'screen_boss_fight':
                    success = monitor_boss_fight_screen()
                    sleep(config.DefaultDelay / 2)
                    if success:
                        # there are two possible screens at this point, the card screen and the hero screen.
                        if find.search_for_image(find.StartFightBtn, to_click=False) is not None:
                            next_page = 'screen_heroes'
                        else:
                            next_page = None
                    sleep(config.TransitionDelay)
        sleep(config.ConnectionScreen)
    except Exception as ex:
        routines.save_logs(f'an error occurred during the main navigation of the game > {ex}', 'game_navigation')
    finally:
        return success


def assemble_fighting_team():
    find = Find()
    success = False
    ready_to_fight = False
    config = ExternalConfigs()
    try:
        if gv.Ready:
            routines.save_logs('a fully formed team was identified. ')
            success = True
            gv.Ready = False
            ready_to_fight = True
        else:
            hero_list = find.search_for_image(find.HeroesList)
            if hero_list is None:
                return success

            # ensures that the amount of heroes to start a battle is within the standards
            if config.MinHeroToStartBattle > 3 or config.MinHeroToStartBattle < 1:
                config.MinHeroToStartBattle = 1

            if find.search_for_image(find.AfkBtn) is not None:
                routines.save_logs('Located afk button. Resetting screen location')
                return success

            # will remove all heroes that are out of energy
            routines.save_logs('removing heroes')
            timeout = time().__add__(config.Timeout + 5)
            while find.search_for_image(find.RemoveHero) is not None and timeout > time():
                x, y = position()
                moveTo(x, y - 70, config.MouseDelay)
                sleep(0.5)
                routines.click()
                sleep(config.DefaultDelay)

            if find.search_for_image(find.AfkBtn) is not None:
                routines.save_logs('Located afk button. Resetting screen location')
                return success

            list_x, list_y = hero_list
            moveTo(list_x, list_y + 60, config.MouseDelay)
            count_scroll = 0
            count_heroes_selected = 0
            timeout = time().__add__(300)
            routines.save_logs('trying to locate a hero with energy')

            while timeout > time():
                if find.search_for_image(find.HeroEnergyOnIcon) is not None:
                    count_heroes_selected += 1
                    routines.save_logs('hero added in the team')
                else:
                    # scrolls the hero list to search for possible fresh heroes
                    sleep(config.DefaultDelay)
                    routines.scroll_page((list_x, list_y + 380), duration=1.8, reverse=True, clicks=220)
                    count_scroll += 1
                    sleep(2)

                    if count_scroll < 4:
                        continue

                # checks for inactivity btn
                if find.search_for_image(find.AfkBtn):
                    routines.save_logs('Located afk button. Resetting screen location')
                    return success  # False

                sleep(config.DefaultDelay)
                if count_heroes_selected == 3 or count_scroll > 3:
                    coord = find.search_for_image(find.RemoveHero, return_xy=False)
                    sleep(config.DefaultDelay)

                    # will fetch all heroes added to the team and confirm that the filling was done correctly
                    sec_timeout = time().__add__(config.Timeout)
                    confirm_selected = 0
                    while sec_timeout > time():
                        if coord is not None:
                            confirm_selected += 1
                            x = coord[0] + coord[2]
                            y = coord[1]
                            moveTo(x, y)
                        else:
                            break
                        coord = find.locate_next(find.RemoveHero, decrement_y=5)
                        sleep(0.5)

                    if count_heroes_selected == confirm_selected:
                        if count_heroes_selected >= config.MinHeroToStartBattle:
                            routines.save_logs('Team formed successfully!')
                            ready_to_fight = True

                    if not ready_to_fight:
                        if count_heroes_selected >= config.MinHeroToStartBattle:
                            routines.save_logs('Team formed successfully!')
                            ready_to_fight = True

                if ready_to_fight:
                    break
        sleep(config.DefaultDelay / 2)
        if ready_to_fight:
            find.search_for_image(find.StartFightBtn)
            sleep(config.DefaultDelay)
            pos = position()
            moveTo(pos.x, pos.y - 50, config.MouseDelay)
            routines.click()
            sleep(2)

            if find.search_for_image(find.AfkBtn) is not None:
                gv.Ready = True

            else:
                if find.search_for_image(find.StartFightBtn, to_click=False) is None:
                    routines.save_logs('starting battle')

                    success = True
                else:
                    routines.save_logs('Battle start information is inconsistent.')
        else:
            routines.save_logs('The team has no resources to start a battle')
    except Exception as ex:
        routines.save_logs(f'crash when trying to start reading heroes in the list - {ex}', 'assemble team')
    finally:
        return success


def monitor_boss_fight_screen():
    find = Find()
    config = ExternalConfigs()
    success = False
    routines.save_logs('monitoring boss fight screen')
    routines.save_logs('waiting for the boss fight to end')
    try:
        # will wait until the boss fight is over
        max_time_on_screen = time().__add__(600)  # maximum time to wait on current screen
        while max_time_on_screen > time():
            if find.search_for_image(find.ScreenFightResult) is not None:
                routines.save_logs('collecting battle results')
                sleep(config.DefaultDelay)

                timeout = time().__add__(config.Timeout / 2)
                while timeout > time():
                    if find.search_for_image(find.ScreenFightResult) is not None:
                        sleep(2)
                success = True
            if success:
                break
    except Exception as ex:
        routines.save_logs(f'failed to monitor boss fight screen - {ex}', 'monitor boss fight screen')
    finally:
        return success


def hero_screen_management():
    routines.save_logs('monitoring heroes screen')
    _next = assemble_fighting_team()

    if gv.Ready:  # checks if the error variable was triggered
        routines.save_logs('Due to inactivity the system is looking for the current screen again')
        return None
    return _next
