import pytest,os
import pandas as pd
from monitoringbyping.main import ReadConfig
from monitoringbyping.main import DataProcessing

#check if the json config file is available
def test_config_file():
    path = os.getcwd()
    email_config = os.path.join(path,"monitoringbyping","email_config.json")
    assert os.path.exists(email_config) == 1

@pytest.fixture
def mbp():
    return ReadConfig()

@pytest.fixture
def dp():
    return DataProcessing()

#check all the primary parameters needed for the email
def test_json_config_data(mbp):
    config_data = mbp.read_server_config()
    assert config_data["username"] != None
    assert config_data["password"] != None
    assert config_data["server"] != None
    assert config_data["smtp_port"] != None
    assert config_data["email_from"] != None
    assert config_data["email_to"] != None

#check for user input file
def test_user_input_file():
    path = os.getcwd()
    ip_info = os.path.join(path,"monitoringbyping","host_info.csv")
    assert os.path.exists(ip_info) == 1

#check for user csv content
def test_user_input_content(mbp):
    data = mbp.read_user_input_config()
    assert data.shape[1] == 2

#check for the current OS
def test_os(dp):
    assert dp.determine_os()[0] in ['Mac','Linux','Windows','Unknown']

#check the host
def test_process_host(dp):
    fail_data = {"IP":["127.0.0.2"], "DEVICE": ["jamserver"]}
    pass_data = {"IP":["127.0.0.1"], "DEVICE": ["local"]}
    assert dp.process_host(dp.determine_os(),pd.DataFrame(fail_data)).find("IP:") != -1
    assert dp.process_host(dp.determine_os(),pd.DataFrame(pass_data)).find("IP:") == -1
