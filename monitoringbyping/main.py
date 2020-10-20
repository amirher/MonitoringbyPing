from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from email.mime.text import MIMEText
import pandas as pd
import subprocess
import smtplib
import json
import csv
import sys
import os



class ReadConfig:

    '''
        Pre-check: The class will contain function to check all the pre-reqs and make
        sure the environment is ready to go and all config files exists.
    '''


    def __init__(self,logger = None):
        self.logger = logger
        if self.logger: self.logger.name = 'ReadConfig'
        path = os.getcwd()
        self.config_file_location = os.path.join(path,"monitoringbyping","email_config.json")
        self.user_input_file_location = os.path.join(path,"monitoringbyping","host_info.csv")
        self._config_data = None
        self._user_data = None


    def read_server_config(self):
        try:
            with open(self.config_file_location) as json_file:
                data = json.load(json_file)
            self._config_data = data['server_config'][0]
            return self._config_data
        except:
            if self.logger: self.logger.error('Unable to open the config file located at {0}'.format(self.config_file_location))
            sys.exit()


    def read_user_input_config(self):
        try:
            df = pd.read_csv(self.user_input_file_location)
            self._user_data = df
            return df
        except:
            if self.logger: self.logger.error('Unable to open the config file located at {0}'.format(self.config_file_location))
            sys.exit()


class DataProcessing:


    ''' The following class contains all the methods that will define the core component of the program.
        The program will execute in the following stages:
        a) Determine OS
        b) Read csv content and ping one ip or hostname at a time
        c) Based on the result from option b, send an email or move to the next record
    '''

    def __init__(self,logger=None):
        self.logger = logger
        if self.logger: self.logger.name = 'DataProcessingClass'


    def determine_os(self):
        '''
            The following function will determine what OS the device is running and what command to use
        '''
        os = ("Unknown","ping -c1 -w2 ")
        if sys.platform.find("linux") != -1:
            os=("Linux","ping -c1 -w2 ")
        elif sys.platform.find("darwin") != -1:
            os=("Mac","ping -t5 ")
        elif sys.platform.find("win") != -1 or sys.platform.find("Windows") != -1:
            os=("Windows","ping -n 5 ")
        if self.logger: self.logger.info("Found OS:- {0}/Ping command:- {1}".format(os[0],os[1]))
        return os


    def process_host(self,os,df):
        '''
            The following function will perform ping operations on the ip addresses passed in the file
        '''
        result_str = "<b> Following device(s) are not responding to the ping </b><br><br>"
        for idx in df.index:
            if self.logger: self.logger.info('Pinging: {0}'.format(df["IP"][idx]))
            current_ip = df["IP"][idx]
            status,ans = subprocess.getstatusoutput(os[1]+current_ip)
            if status != 0 or "host unreachable." in ans:
                result_str += "<p> IP: "+df["IP"][idx]+"  "+df["DEVICE"][idx]+"</p>"
        return result_str


    def process_email(self,data,mail_config):
        '''
            The following function will email based on the config, if data exists.
        '''
        try:
            server = smtplib.SMTP(mail_config['server'], mail_config['smtp_port'])#office 365.
            msg = MIMEMultipart()
            msg['Subject'] = mail_config['subject']
            html_body= MIMEText(data, 'html')
            msg.attach(html_body)
            server.ehlo()
            server.starttls()
            server.login(mail_config['username'], mail_config['password'])
            server.sendmail(mail_config['email_from'], mail_config['email_to'],msg.as_string())
        except Exception as e:
            if self.logger: self.logger.error("Error Sending Email. Error Descrition: {0}".format(e))
            print(e)
        finally:
            server.quit()
