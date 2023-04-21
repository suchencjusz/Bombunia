from utils import get_config
from bombunia import Bombunia

import time

cfg = get_config()




if __name__ == "__main__":
    b = Bombunia(
        username=cfg['vulcan']['username'],
        password=cfg['vulcan']['password'],
        cookies={},
        school_url=cfg['vulcan']['school_url'],
    )
    
    b.init_session()
    

    time.sleep(50)
