
def __start_application__():
    from App import GameResources as resources
    from App import Routines as routines
    from App.Objects.externalConfigs import ExternalConfigs
    from time import sleep

    config = ExternalConfigs()
    resources.startup()  # creates the image folders and organizes the environment to launch the application
    success = True
    if success:
        while True:
            sleep(config.DefaultDelay)
            resources.game_navigation()
    else:
        routines.save_logs('Application closed')
    # end application
