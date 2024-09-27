"""Command line interface."""


class CLI:
    """The command line interface (CLI) that the user will interact with."""

    def display_banner(self) -> None:
        """Display the ASCII banner and lightning bolt logo for the application.

        :return: the banner to std out
        """
        banner = """
        
        __________________________    .____    .__       .__     __         .__                
    \____    /\__    ___/  _  \   |    |   |__| ____ |  |___/  |_  ____ |__| ____    ____  
      /     /   |    | /  /_\  \  |    |   |  |/ ___\|  |  \   __\/    \|  |/    \  / ___\ 
     /     /_   |    |/    |    \ |    |___|  / /_/  >   Y  \  | |   |  \  |   |  \/ /_/  >
    /_______ \  |____|\____|__  / |_______ \__\___  /|___|  /__| |___|  /__|___|  /\___  / 
            \/                \/          \/ /_____/      \/          \/        \//_____/  
                                                   ,/
                                                 ,'/
                                               ,' /
                                             ,'  /_____,
                                           .'____    ,'    
                                                /  ,'
                                               / ,'
                                              /,'
                                             /'"""
        print(banner)

    def display_instructions(self) -> None:
        """Display the instructions for the application.

        :return: the instructions to use the application to std out
        """
        instructions = """
        ZTA Lightning is a tool used to check if your network security Zero Trust Architecture (ZTA) is in compliance
        with certain ZTA principles.
        To use this tool, please have the url and credentials ready to access your network appliance responsible for AAA and NMS.
        HTTPS and JWT must be enabled on your appliance for this tool to authenticate.
        The tool will examine devices on the network based on data provided by the appliance and provide an excel report
        of the compliance results.
        """
        print(instructions)
