from app import app
from app.utils import logging_utils as lu
import logging
import config

logger = lu.Logger(__name__, cmd_level=logging.INFO, file_level=logging.INFO)

if __name__ == '__main__':
    logger.logger.info('---------- Application started ----------')
    app.run('0.0.0.0', port=config.PORT)
