import logging
from monitoringbyping.main import ReadConfig
from monitoringbyping.main import DataProcessing

#logging config
logging.basicConfig(level=logging.WARN) #change it to INFO for debugging
logger = logging.getLogger(__name__)
handler = logging.FileHandler('logs/log')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def exec_handler():
    read_files = ReadConfig(logger)
    mail_config = read_files.read_server_config()
    data_frame = read_files.read_user_input_config()
    process_data = DataProcessing(logger)
    os = process_data.determine_os()
    result = process_data.process_host(os,data_frame)
    if "IP: " in result: process_data.process_email(result,mail_config)

exec_handler()
