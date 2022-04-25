DEBUG = False

if not DEBUG:
    from App import Main as main
    main.__start_application__()

else:
    print("START DEBUG")
    from App import Routines as routines
    from App.Find import Find
    from App.Objects.externalConfigs import ExternalConfigs
    from App import GameResources as resources
    config = ExternalConfigs()
    from pyautogui import moveTo

    from time import sleep
    find = Find()
    sleep(5)
    resources.assemble_fighting_team()


    print('END DEBUG')
