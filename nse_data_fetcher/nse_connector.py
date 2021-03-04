#!/usr/bin/python3

import requests

class OC_DATA():
    def __init__(self)->None:
        self.symb = " "
        self.url_oc = 'https://www.nseindia.com/option-chain'
        self.hdr: Dict[str, str] = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                                (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36','accept-language':'en-US,en;q=0.9'}
        self.con_trial = 1
    def set_stock(self,symb):
        self.symb = symb
    
    def get_oc_data(self):
        #self.con_trial = 0
        self.connect_to_nse()
        self.response = self.session.get(self.url,headers=self.hdr,timeout=100,cookies=self.cookies)
        return self.response.json()
    
    def connect_to_nse(self):
        self.con_trial = self.con_trial + 1
        if(self.symb=='NIFTY' or self.symb=='BANKNIFTY'):
            self.url = 'https://www.nseindia.com/api/option-chain-indices?symbol='+self.symb
        else:
            self.url = 'https://www.nseindia.com/api/option-chain-equities?symbol='+self.symb
        try:
            self.session.close()
        except:
            pass
        self.session = requests.Session()
        try:
            request = self.session.get(self.url_oc, headers=self.hdr, timeout=100)
            self.cookies = dict(request.cookies)
        except:
            print("************* reconnecting to NSE *************")
            self.connect_to_nse()
            return
    
    def get_expiry_dates(self):
        #self.con_trial = 0
        self.connect_to_nse()
        self.response = self.session.get(self.url,headers=self.hdr,timeout=100,cookies=self.cookies)
        try:
            json_data = self.response.json()
            self.expiry_dates: List = []
            self.expiry_dates = json_data['records']['expiryDates']
        except:
            self.connect_to_nse()
