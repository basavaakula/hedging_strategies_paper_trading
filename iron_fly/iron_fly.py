#!/usr/bin/python3

import sys
sys.path.append("..")

from imports.packages import *

class IRON_FLY:
    def __init__(self,root)->None:
        self.first_run = True
        self.stop = False
        self.interval = 10.
        self.imp_strikes: List[float] = []
        self.imp_my_buy_price: List[float] = []
        self.nse_adapter = NC.OC_DATA()
        self.root = root
    def setup_gui(self,my_master: Frame)->None:
        self.master_wd = my_master
        top_frame: Frame = Frame(my_master)
        top_frame.pack(anchor='nw',fill='y', expand=True, side=LEFT)
        bot_frame: Frame = Frame(my_master)
        bot_frame.pack(fill='both', expand=True, side=LEFT)
        pdx = 1
        pdy = 1
        
        row_idx = 0
        var_stock: StringVar = StringVar()
        var_stock.set(" ")
        lbl_stock: Label = Label(top_frame,text='Underlying',justify=LEFT,font=("TkDefaultFont", 10,"bold"))
        #lbl_stock.pack(anchor=N, expand=False, side=LEFT)
        lbl_stock.grid(row=row_idx,column=0,sticky='nw',padx=pdx,pady=pdy)
        self.combo_box_stock = Combobox(top_frame,width=10,textvariable=var_stock) 
        #self.combo_box_stock.pack(anchor=N, expand=False, side=LEFT)
        self.combo_box_stock.grid(row=row_idx,column=1,sticky='nw',padx=pdx,pady=pdy)
        self.combo_box_stock.configure(state='readonly')
        self.combo_box_stock['values'] = self.root.indices
        self.combo_box_stock.bind('<<ComboboxSelected>>', self.set_expiry_date)
        row_idx = row_idx + 1
        
        date_var_stock: StringVar = StringVar()
        date_var_stock.set(" ")
        lbl_exp_date_stock: Label = Label(top_frame,text='Expiry',justify=LEFT,font=("TkDefaultFont", 10,"bold"))
        lbl_exp_date_stock.grid(row=row_idx,column=0,sticky='nsw',padx=pdx,pady=pdy)
        #lbl_exp_date_stock.pack(anchor='nw',fill='y', expand=True, side=TOP)
        self.date_combo_box_stock = Combobox(top_frame,width=10,textvariable=date_var_stock) 
        self.date_combo_box_stock.grid(row=row_idx,column=1,sticky='nsw',padx=pdx,pady=pdy)
        #self.date_combo_box_stock.pack(anchor='nw',fill='y', expand=True, side=TOP)
        self.date_combo_box_stock.configure(state='readonly')
        self.date_combo_box_stock.bind('<<ComboboxSelected>>', self.get_strikes)
        row_idx = row_idx + 1
        
        var_lot_size: StringVar = StringVar()
        var_lot_size.set(" ")
        lbl_lot_size: Label = Label(top_frame,text='Qty',justify=LEFT,font=("TkDefaultFont", 10, "bold"))
        #lbl_lot_size.pack(anchor=N, expand=False, side=LEFT)
        lbl_lot_size.grid(row=row_idx,column=0,sticky='nsw',padx=pdx,pady=pdy)
        self.qty_combo_box = Combobox(top_frame,width=10,textvariable=var_lot_size) 
        #self.qty_combo_box.pack(anchor=N, expand=False, side=LEFT)
        self.qty_combo_box.configure(state='readonly')
        self.qty_combo_box.grid(row=row_idx,column=1,sticky='nsw',padx=pdx,pady=pdy)
        row_idx = row_idx + 1
        
        
        
        buy_pe_strike: StringVar = StringVar()
        buy_pe_strike.set(" ")
        lbl_buy_pe_strike: Label = Label(top_frame,text='BUY PE strike',justify=LEFT,font=("TkDefaultFont",\
            10,"bold"),fg='green')
        lbl_buy_pe_strike.grid(row=row_idx,column=0,sticky='nsw',padx=pdx,pady=pdy)
        self.cbox_buy_pe_strike = Combobox(top_frame,width=10,textvariable=buy_pe_strike) 
        self.cbox_buy_pe_strike.grid(row=row_idx,column=1,sticky='nsw',padx=pdx,pady=pdy)
        self.cbox_buy_pe_strike.configure(state='readonly')
        row_idx = row_idx + 1
        
        sell_strike: StringVar = StringVar()
        sell_strike.set(" ")
        lbl_sell_strike: Label = Label(top_frame,text='SELL strike',justify=LEFT,font=("TkDefaultFont", 10, "bold"),\
                fg='red')
        lbl_sell_strike.grid(row=row_idx,column=0,sticky='nsw',padx=pdx,pady=pdy)
        self.cbox_sell_strike = Combobox(top_frame,width=10,textvariable=sell_strike) 
        self.cbox_sell_strike.grid(row=row_idx,column=1,sticky='nsw',padx=pdx,pady=pdy)
        self.cbox_sell_strike.configure(state='readonly')
        self.cbox_sell_strike.bind('<<ComboboxSelected>>', self.get_strikes_change)
        row_idx = row_idx + 1
        
        buy_ce_strike: StringVar = StringVar()
        buy_ce_strike.set(" ")
        lbl_buy_ce_strike: Label = Label(top_frame,text='BUY CE strike',justify=LEFT,font=("TkDefaultFont", 10,\
                "bold"),fg='green' )
        lbl_buy_ce_strike.grid(row=row_idx,column=0,sticky='nsw',padx=pdx,pady=pdy)
        self.cbox_buy_ce_strike = Combobox(top_frame,width=10,textvariable=buy_ce_strike) 
        self.cbox_buy_ce_strike.grid(row=row_idx,column=1,sticky='nsw',padx=pdx,pady=pdy)
        self.cbox_buy_ce_strike.configure(state='readonly')
        row_idx = row_idx + 1
        
        lbl_safe_zone: Label = Label(top_frame,text='Premium received: ',justify=LEFT,font=("TkDefaultFont", 10,\
                "bold"))
        lbl_safe_zone.grid(row=row_idx,column=0,sticky='nsw',padx=pdx,pady=pdy)
        self.lbl_safe_zone1: Label = Label(top_frame,text=' ',justify=LEFT,font=("TkDefaultFont", 10,\
                "bold"),fg='green' )
        self.lbl_safe_zone1.grid(row=row_idx,column=1,sticky='nsw',padx=pdx,pady=pdy)
        row_idx = row_idx + 1
        
        self.start_button: Button = tk.Button(top_frame,text='Trade',command=self.main_recursive,width=15,bg='green',fg='white',font=("TkDefaultFont", 10, "bold"))
        #self.start_button.pack(anchor=N, expand=False, side=LEFT)
        self.start_button.grid(row=row_idx,column=0,sticky='nsw',columnspan=2)#,padx=pdx,pady=pdy)
        self.start_button.configure(state='disabled')
        row_idx = row_idx + 1
        
        self.import_button: Button = tk.Button(top_frame,text='Manual',command=self.import_iron_fly,width=15,bg='red',fg='white',font=("TkDefaultFont", 10, "bold"))
        #self.import_button.pack(anchor=N, expand=False, side=LEFT)
        self.import_button.grid(row=row_idx,column=0,sticky='nsw',columnspan=2)#,padx=pdx,pady=pdy)
        self.import_button.configure(state='disabled')
        row_idx = row_idx + 1
        
        self.load_button: Button = tk.Button(top_frame,text='Load trade',command=self.load_file,width=15,bg='yellow',fg='black',font=("TkDefaultFont", 10, "bold"))
        self.load_button.grid(row=row_idx,column=0,sticky='nsw',columnspan=2)
        self.load_button.configure(state='normal')
        
        fig = Figure(figsize = (3, 3), dpi = 200) 
        #fig.subplots_adjust(left=0, right=1, top=1, bottom=0) 
        self.plot1 = fig.add_subplot(111)
        self.plot1.tick_params(axis='both', which='minor', labelsize=8)

        self.canvas = FigureCanvasTkAgg(fig,master = bot_frame)
        #self.canvas.get_tk_widget().grid(row=1,column=1,sticky='nswe',padx=pdx,pady=pdy) 
        self.canvas.get_tk_widget().pack(fill='both',expand=True,side=TOP)
          
    def export_iron_condor(self):
        self.imp_strikes.clear()
        self.imp_my_buy_price.clear()
        for i in enumerate(self.imp_cbox):
            if(i[1].get()==""):
                break
            self.imp_strikes.append(float(i[1].get()))
            self.imp_my_buy_price.append(float(self.imp_tbox[i[0]].get('1.0',END)))
        df_export: pd.DataFrame = pd.DataFrame()
        df_export['Strikes'] = self.imp_strikes
        df_export['Buy_price'] = self.imp_my_buy_price
        save_name = self.combo_box_stock.get()+'-'+self.date_combo_box_stock.get()+'-'+datetime.now().strftime("%H:%M:%S")
        df_export.to_csv(save_name+'.csv')
        
        self.imp_wd.destroy() 
        self.import_button.configure(state='disabled')
    
    def save_current_data(self):
        save_name =\
        self.root.default_save_dir+self.combo_box_stock.get()+'_'+self.date_combo_box_stock.get()+'_'+date.today().strftime("%b-%d-%Y")+'.csv.ic'
        if(not path.exists(save_name)):
            df_export: pd.DataFrame = pd.DataFrame()
            df_export['Strikes'] = (self.df['Strikes'].tolist())
            df_export['Buy_price'] = (self.df['My_price'].tolist())
            df_export['Qty'] = [(self.df['Qty'].tolist())[0]]*4
            df_export.to_csv(save_name)

    def load_file(self): 
        file = askopenfile(mode ='r', filetypes =[('CSV files', '*.ic')],initialdir=self.root.default_save_dir)
        if file is not None:
            self.df_loaded: pd.DataFrame = pd.read_csv(file.name)
            self.imp_strikes = self.df_loaded['Strikes'].tolist()
            self.imp_my_buy_price = self.df_loaded['Buy_price'].tolist()
            qty = (self.df_loaded['Qty'].tolist())[0]
            name_split = (os.path.basename(file.name)).split('_')
            self.combo_box_stock.set(name_split[0])
            self.date_combo_box_stock.set(name_split[1])
            self.qty_combo_box.set(qty)
            self.nse_adapter.set_stock(self.combo_box_stock.get())
            self.main_recursive()
    
    def open_file(self): 
        file = askopenfile(mode ='r', filetypes =[('CSV files', '*.csv')]) 
        #if file is not None: 
        #    content = file.read() 
        #    print(content) 
        self.df_loaded: pd.DataFrame = pd.read_csv(file.name)
        self.imp_strikes = self.df_loaded['Strikes'].tolist()
        self.imp_my_buy_price = self.df_loaded['Buy_price'].tolist()
        self.imp_wd.destroy() 
        self.import_button.configure(state='disabled')
    
    def import_iron_fly(self):
        self.imp_wd: Tk = Tk()
        self.imp_wd.title('Paper trading')
        window_width: int = self.imp_wd.winfo_reqwidth()
        window_height: int = self.imp_wd.winfo_reqheight()
        position_right: int = int(self.imp_wd.winfo_screenwidth() / 2 - window_width / 2)
        position_down: int = int(self.imp_wd.winfo_screenheight() / 2 - window_height / 2)
        self.imp_wd.geometry("600x300+300+200")
        
        bot_frame: Frame = Frame(self.imp_wd,width=800, height=300)
        bot_frame.pack(anchor='nw', fill='both',expand=True, side=TOP)
        bot_frame.pack_propagate(0)
        
        json_data = self.nse_adapter.get_oc_data()
        match_date = self.date_combo_box_stock.get()
        strike_prices: List[float] = [data['strikePrice'] for data in json_data['records']['data'] \
                                   if (str(data['expiryDate']).lower() == str(match_date).lower())]
        

        self.imp_cbox: List[Combobox]    = []
        self.imp_tbox: List[tk.Text]    = []
        imp_vars: List[StringVar] = []
        imp_lbls: List[Label]     = []
        imp_lbls_txt: List[Label] = ['buy PUT','sell PUT','sell CALL','buy CALL']
        imp_lbls_color: List[Label] = ['green','red','red','green']
            
        row_idx = 0

        for i in enumerate(imp_lbls_txt):
            str_var = StringVar()
            str_var.set(' ')
            lbl: Label = Label(bot_frame,text=i[1],justify=LEFT,font=("TkDefaultFont", 10,"bold"),fg=imp_lbls_color[i[0]],width=20)
            lbl.grid(row=i[0],column=0,sticky='nswe')
            cb = Combobox(bot_frame,width=10,textvariable=str_var) 
            cb.grid(row=i[0],column=1,sticky='nswe')
            cb.configure(state='readonly')
            cb['values'] = strike_prices
            self.imp_cbox.append(cb)
            txt = tk.Text(bot_frame,width=10,bg='yellow',height=2)
            txt.grid(row=i[0],column=2,sticky='nswe')
            self.imp_tbox.append(txt)
            row_idx = i[0]+1
        
        ok_button: Button = tk.Button(bot_frame,text='OK!',command=self.export_iron_condor,width=20,bg='green',fg='white',font=("TkDefaultFont", 10, "bold"))
        ok_button.grid(row=row_idx,column=4,sticky='nswe')
        
        load_button: Button = tk.Button(bot_frame,text='Load',command=self.open_file,width=20,bg='green',fg='white',font=("TkDefaultFont", 10, "bold"))
        load_button.grid(row=row_idx+1,column=4,sticky='nswe')

        
    def set_VIX(self,event):
        self.vix_percentage = float(self.vix_combo_box.get())
        self.start_button.configure(state='normal')
        self.import_button.configure(state='normal')
    def set_expiry_date(self,event):
        self.nse_adapter.set_stock(self.combo_box_stock.get())
        self.nse_adapter.get_expiry_dates()
        self.date_combo_box_stock['values'] = tuple(self.nse_adapter.expiry_dates)
        #self.date_combo_box_stock.set(self.nse_adapter.expiry_dates[0])
        self.date_combo_box_stock.set('---')
        qtys = [x*int(self.root.indices_lot[self.combo_box_stock.get()]) for x in range(1,11)]
        self.qty_combo_box['values'] = qtys
        self.qty_combo_box.set(qtys[0])
    
    def get_strikes_change(self,event):
        json_data = self.nse_adapter.get_oc_data()
        end = time.time();
        #strr = "NSE response time (sec) : " + str(round(end-start,2)) + " ( " + str(self.nse_adapter.con_trial) + " hits)"
        #self.lbl_nse_con_time.config(text=strr)
        match_date = self.date_combo_box_stock.get()
        strike_prices: List[float] = [data['strikePrice'] for data in json_data['records']['data'] \
                                   if (str(data['expiryDate']).lower() == str(match_date).lower())]
        
        ce_values: List[dict] = [data['CE'] for data in json_data['records']['data'] \
                    if "CE" in data and (str(data['expiryDate'].lower()) == str(match_date.lower()))]
        pe_values: List[dict] = [data['PE'] for data in json_data['records']['data'] \
                    if "PE" in data and (str(data['expiryDate'].lower()) == str(match_date.lower()))]
         
        ce_data: pd.DataFrame = pd.DataFrame(ce_values)
        pe_data: pd.DataFrame = pd.DataFrame(pe_values)

        self.cbox_sell_strike['values'] = tuple(strike_prices)
        self.cbox_buy_pe_strike['values'] = tuple(strike_prices)
        self.cbox_buy_ce_strike['values'] = tuple(strike_prices)
        
        curr_price = ce_data['underlyingValue'][0]

        my_atm = int(self.cbox_sell_strike.get())
        print('******************* atm =%i'%my_atm)
        
        

        ce_premium = ce_data.loc[ce_data['strikePrice']==my_atm]
        pe_premium = (pe_data.loc[pe_data['strikePrice']==my_atm])
        ce_premium = (ce_premium['lastPrice'].tolist())[0]
        pe_premium = (pe_premium['lastPrice'].tolist())[0]

        comb_prem = ce_premium + pe_premium 

        buy_ce_strike = my_atm + comb_prem
        buy_pe_strike = my_atm - comb_prem

        buy_ce_strike = self.get_closest_strike(buy_ce_strike,strike_prices)
        buy_pe_strike = self.get_closest_strike(buy_pe_strike,strike_prices)
        
        self.cbox_buy_ce_strike.set(buy_ce_strike)
        self.cbox_buy_pe_strike.set(buy_pe_strike)
        self.lbl_safe_zone1.configure(text=str(round(comb_prem,2)))
        self.start_button.configure(state='normal')
    
    def get_strikes(self,event):
        json_data = self.nse_adapter.get_oc_data()
        end = time.time();
        #strr = "NSE response time (sec) : " + str(round(end-start,2)) + " ( " + str(self.nse_adapter.con_trial) + " hits)"
        #self.lbl_nse_con_time.config(text=strr)
        match_date = self.date_combo_box_stock.get()
        strike_prices: List[float] = [data['strikePrice'] for data in json_data['records']['data'] \
                                   if (str(data['expiryDate']).lower() == str(match_date).lower())]
        
        ce_values: List[dict] = [data['CE'] for data in json_data['records']['data'] \
                    if "CE" in data and (str(data['expiryDate'].lower()) == str(match_date.lower()))]
        pe_values: List[dict] = [data['PE'] for data in json_data['records']['data'] \
                    if "PE" in data and (str(data['expiryDate'].lower()) == str(match_date.lower()))]
         
        ce_data: pd.DataFrame = pd.DataFrame(ce_values)
        pe_data: pd.DataFrame = pd.DataFrame(pe_values)

        print('******** CE cols')
        print(list(ce_data.columns))
        print('******** PE cols')
        print(list(pe_data.columns))

        self.cbox_sell_strike['values'] = tuple(strike_prices)
        self.cbox_buy_pe_strike['values'] = tuple(strike_prices)
        self.cbox_buy_ce_strike['values'] = tuple(strike_prices)
        
        curr_price = ce_data['underlyingValue'][0]

        my_atm = self.get_closest_strike(curr_price,strike_prices)
        self.cbox_sell_strike.set(my_atm)
        
        

        ce_premium = ce_data.loc[ce_data['strikePrice']==my_atm]
        pe_premium = (pe_data.loc[pe_data['strikePrice']==my_atm])
        ce_premium = (ce_premium['lastPrice'].tolist())[0]
        pe_premium = (pe_premium['lastPrice'].tolist())[0]

        comb_prem = ce_premium + pe_premium 

        buy_ce_strike = my_atm + comb_prem
        buy_pe_strike = my_atm - comb_prem

        buy_ce_strike = self.get_closest_strike(buy_ce_strike,strike_prices)
        buy_pe_strike = self.get_closest_strike(buy_pe_strike,strike_prices)
        
        self.cbox_buy_ce_strike.set(buy_ce_strike)
        self.cbox_buy_pe_strike.set(buy_pe_strike)
        self.lbl_safe_zone1.configure(text=str(comb_prem))
        self.lbl_safe_zone1.configure(text=str(round(comb_prem,2)))
        self.start_button.configure(state='normal')


    def get_closest_strike(self,strike,strikes):
        diff = [abs(x-strike) for x in strikes]
        min_pos = diff.index(min(diff))
        return strikes[min_pos]
    
    def main_recursive(self)->None:
        if(self.first_run):
            #self.start_button.configure(state='disabled')
            #self.combo_box_stock.configure(state='disabled')
            #self.date_combo_box_stock.configure(state='disabled')
            #self.qty_combo_box.configure(state='disabled')
            self.df_iron_fly()
            self.first_run = False
        self.curr_time = time.time()
        time_passed = int(self.curr_time-self.prev_time)
        if(time_passed>=self.interval):
            #self.refresh_data()
            self.df_iron_fly()
        else:
            #self.sh_window.after((10 * 1000),self.main_recursive)
            self.master_wd.after((10 * 1000),self.main_recursive)
            return
        if(not self.stop):
            #self.sh_window.after((10 * 1000),self.main_recursive)
            self.master_wd.after((10 * 1000),self.main_recursive)
            return

    def refresh_data(self):
        for strat in enumerate(self.strategies):
            curr_sh = self.NBS[strat[0]]
            if(strat[1]=='IRON CONDOR'):
                df = self.df_iron_fly()
                pl_col_idx = (list(df.columns)).index('P&L')
                for col in enumerate(df.columns):
                    curr_sh.set_column_data(col[0],values=df[col[1]])
                for i in range(curr_sh.get_total_rows()):
                    if(float(curr_sh.get_cell_data(i,pl_col_idx))<=0.0):
                        curr_sh.highlight_cells(row=i, column=pl_col_idx, bg='red',fg='white')
                    if(float(curr_sh.get_cell_data(i,pl_col_idx))>0.0):
                        curr_sh.highlight_cells(row=i, column=pl_col_idx, bg='green',fg='white')
        self.prev_time = time.time()
        curr_sh.refresh()

    
    def df_iron_fly(self):
        df: pd.DataFrame = pd.DataFrame()
        
        self.buy_pe_pl: List[float] = []
        self.sell_pe_pl: List[float] = []
        self.sell_ce_pl: List[float] = []
        self.buy_ce_pl: List[float] = []
        
        start = time.time()
        json_data = self.nse_adapter.get_oc_data()
        end = time.time();
        #strr = "NSE response time (sec) : " + str(round(end-start,2)) + " ( " + str(self.nse_adapter.con_trial) + " hits)"
        #self.lbl_nse_con_time.config(text=strr)
        match_date = self.date_combo_box_stock.get()
        strike_prices: List[float] = [data['strikePrice'] for data in json_data['records']['data'] \
                                   if (str(data['expiryDate']).lower() == str(match_date).lower())]
        ce_values: List[dict] = [data['CE'] for data in json_data['records']['data'] \
                    if "CE" in data and (str(data['expiryDate'].lower()) == str(match_date.lower()))]
        pe_values: List[dict] = [data['PE'] for data in json_data['records']['data'] \
                    if "PE" in data and (str(data['expiryDate'].lower()) == str(match_date.lower()))]
         
        ce_data: pd.DataFrame = pd.DataFrame(ce_values)
        pe_data: pd.DataFrame = pd.DataFrame(pe_values)
       
        #print(list(ce_data.columns))
        
        pe_otm_data: pd.DataFrame = pd.DataFrame()
        ce_otm_data: pd.DataFrame = pd.DataFrame()

        df_call_buy: pd.DataFrame = pd.DataFrame() 

        strike_diff: List[float] = []
        
        
        curr_price = ce_data['underlyingValue'][0]
        #self.sh_window.title('Paper trading-->'+self.combo_box_stock.get()+' ('+str(curr_price)+' ) @--'+datetime.now().strftime("%H:%M:%S"))
        if(self.first_run):
            diff = [abs(x-curr_price) for x in strike_prices]
            min_pos = diff.index(min(diff))
            self.my_atm = strike_prices[min_pos]
            
        strike_diff = list(map(lambda x:x-self.my_atm,strike_prices))
        
        iron_condor_strikes: List[float] = []
        if(len(self.imp_strikes)==0):
            #search_strike = int(self.cbox_sell_strike.get())
            #diff = [abs(x-search_strike) for x in strike_prices]
            #min_pos = int(diff.index(min(diff)))
            #sell_pe_idx = min_pos
            #sell_ce_idx = min_pos

            #print('******************* OLD %i'%sell_pe_idx)
            #print(self.cbox_sell_strike.get())
            #print(ce_data['strikePrice'])

            sell_ce_idx = sell_pe_idx = (ce_data.index[ce_data['strikePrice']==int(self.cbox_sell_strike.get())].tolist())[0]
            buy_pe_idx = (pe_data.index[pe_data['strikePrice']==int(self.cbox_buy_pe_strike.get())].tolist())[0]
            buy_ce_idx = (ce_data.index[ce_data['strikePrice']==int(self.cbox_buy_ce_strike.get())].tolist())[0]

            iron_condor_strikes.append(buy_pe_idx)#buy_pe_strike
            iron_condor_strikes.append(sell_pe_idx)#sell_pe_strike

            pe_otm_data = pe_data.iloc[iron_condor_strikes] 
            
            iron_condor_strikes.clear()
            
            iron_condor_strikes.append(sell_ce_idx)#sell_ce_strike
            iron_condor_strikes.append(buy_ce_idx)#buy_ce_strike
            
            ce_otm_data = ce_data.iloc[iron_condor_strikes]
        else:
            iron_condor_strikes.append(strike_prices.index(self.imp_strikes[0]))
            iron_condor_strikes.append(strike_prices.index(self.imp_strikes[1]))
            pe_otm_data = pe_data.iloc[iron_condor_strikes] 
            buy_pe_idx = iron_condor_strikes[0]
            sell_pe_idx = iron_condor_strikes[1]
            
            iron_condor_strikes.clear()
            iron_condor_strikes.append(strike_prices.index(self.imp_strikes[2]))
            iron_condor_strikes.append(strike_prices.index(self.imp_strikes[3]))
            ce_otm_data = ce_data.iloc[iron_condor_strikes]
            
            sell_ce_idx = iron_condor_strikes[0]
            buy_ce_idx = iron_condor_strikes[1]
            
            self.my_buy_price = self.imp_my_buy_price
            

        
        pd_concat = pd.concat([pe_otm_data,ce_otm_data],axis=0)
        sell_buy_signs = [1.,-1.,-1.,1.]
        lot_list = [float(self.qty_combo_box.get())]*pd_concat.shape[0]
        qty_list = list(map(mul,lot_list,sell_buy_signs))
        ltp_list = list(map(float,pd_concat['lastPrice'].tolist()))
        bid_list = list(map(float,pd_concat['bidprice'].tolist()))
        if(self.first_run and len(self.imp_strikes)==0):
            self.my_buy_price = pd_concat['lastPrice'].tolist()
        
        net_points: List[float] = list(map(mul,sell_buy_signs,self.my_buy_price))
        net_points = list(map(lambda x: x*-1,net_points))
        curr_pl = list(map(sub,ltp_list,self.my_buy_price))
        mkt_pl = list(map(sub,bid_list,self.my_buy_price))
        df['Strikes'] = pd_concat['strikePrice'].tolist() 
        df['Qty'] = qty_list
        df['My_price'] = list(map(float,self.my_buy_price))
        df['LTP'] = ltp_list
        df['P&L'] = list(map(mul,curr_pl,qty_list))
        df['P&L'] =  df['P&L'].round(3)
        df['Market_P&L'] =  list(map(mul,mkt_pl,qty_list))
        df['OI_change'] =  pd_concat['pchangeinOpenInterest'].tolist()
        df['OI_change'] = df['OI_change'].round(3)
        df['ask_price'] = pd_concat['askPrice'].tolist()
        df['bid_price'] = pd_concat['bidprice'].tolist()
        
        for i in range(len(strike_prices)):
            if(i>=buy_pe_idx):
                val = -self.my_buy_price[0]
            else:
                val = abs(strike_prices[i]-strike_prices[buy_pe_idx])-self.my_buy_price[0]
            self.buy_pe_pl.append(val)
            
            if(i>=sell_pe_idx):
                val = self.my_buy_price[1]
            else:
                val = self.my_buy_price[1]-abs(strike_prices[i]-strike_prices[sell_pe_idx])
            self.sell_pe_pl.append(val)
            
            if(i<=sell_ce_idx):
                val = self.my_buy_price[2]
            else:
                val = self.my_buy_price[2]-abs(strike_prices[i]-strike_prices[sell_ce_idx])
            self.sell_ce_pl.append(val)
            
            if(i<=buy_ce_idx):
                val = -self.my_buy_price[3]
            else:
                val = abs(strike_prices[i]-strike_prices[buy_ce_idx])-self.my_buy_price[3]
            self.buy_ce_pl.append(val)
        
        
        comb_pl: List[float] = [0]*len(strike_prices)
        comb_pl = list(map(add,comb_pl,self.buy_pe_pl))
        comb_pl = list(map(add,comb_pl,self.sell_pe_pl))
        comb_pl = list(map(add,comb_pl,self.sell_ce_pl))
        comb_pl = list(map(add,comb_pl,self.buy_ce_pl))
        comb_pl = list(map(lambda x:x*float(self.qty_combo_box.get()),comb_pl))

        self.strike_prices = strike_prices
        self.pd_concat = pd_concat
        self.curr_price = curr_price
        self.comb_pl = comb_pl
        self.df = df
        self.draw_plot()
        self.save_current_data()
        self.prev_time = time.time()
        #return df
        
    def draw_plot(self):
        self.plot1.clear()
        self.plot1.plot(self.strike_prices,self.comb_pl,'-b',lw=.8)
        self.plot1.plot(self.strike_prices,self.buy_pe_pl,'--',lw=.5,label='BUY PE ('\
        +str((self.df['Strikes'].tolist())[0])+'>'+str((self.df['P&L'].tolist())[0])+')')
        self.plot1.plot(self.strike_prices,self.sell_pe_pl,'--',lw=.5,label='SELL PE ('\
        +str((self.df['Strikes'].tolist())[1])+'>'+str((self.df['P&L'].tolist())[1])+')')
        self.plot1.plot(self.strike_prices,self.sell_ce_pl,'--',lw=.5,label='SELL CE ('\
        +str((self.df['Strikes'].tolist())[2])+'>'+str((self.df['P&L'].tolist())[2])+')')
        self.plot1.plot(self.strike_prices,self.buy_ce_pl,'--',lw=.5,label='BUY CE ('\
        +str((self.df['Strikes'].tolist())[3])+'>'+str((self.df['P&L'].tolist())[3])+')')
        self.plot1.legend()
        self.plot1.axvline(x=(self.pd_concat['strikePrice'].tolist())[0],linestyle='--',color='g',lw=.8)
        self.plot1.axvline(x=(self.pd_concat['strikePrice'].tolist())[1],linestyle='--',color='r',lw=.8)
        self.plot1.axvline(x=(self.pd_concat['strikePrice'].tolist())[2],linestyle='--',color='r',lw=.8)
        self.plot1.axvline(x=(self.pd_concat['strikePrice'].tolist())[3],linestyle='--',color='g',lw=.8)
        self.plot1.plot(self.curr_price,self.df['P&L'].iloc[0:-1].sum(),'D',markersize=2)
        self.plot1.plot(self.curr_price,self.df['Market_P&L'].iloc[0:-1].sum(),'s',markersize=2)
        #self.plot1.plot(self.curr_price,(self.df['P&L'].tolist())[0],'s',markersize=2)
        #self.plot1.plot(self.curr_price,(self.df['P&L'].tolist())[1],'s',markersize=2)
        #self.plot1.plot(self.curr_price,(self.df['P&L'].tolist())[2],'s',markersize=2)
        #self.plot1.plot(self.curr_price,(self.df['P&L'].tolist())[3],'s',markersize=2)
        self.plot1.text(1.0*min(self.strike_prices),.2*max(self.comb_pl),'max_profit ='+str(round(max(self.comb_pl),2)),color='green',fontsize='6')
        self.plot1.text(1.1*min(self.strike_prices),.5*max(self.comb_pl),'max_loss = '+str(round(min(self.comb_pl),2)),color='red',fontsize='6')
        clr = 'red'
        if(self.df['P&L'].iloc[0:-1].sum()>0):
            clr = 'green'
        self.plot1.text(1.01*self.curr_price,1.01*self.df['P&L'].iloc[0:-1].sum(),str(self.df['P&L'].sum()),color=clr,fontsize='4')
        #self.plot1.text(1.01*self.curr_price,1.01*self.df['Market_P&L'].iloc[0:-1].sum(),str(self.df['Market_P&L'].iloc[0:-1].sum()),color=clr,fontsize='4')
        self.root.master_wd.title('Paper trading-->'+self.combo_box_stock.get()+' ('+str(self.curr_price)+' ) @--'+datetime.now().strftime("%H:%M:%S"))
        self.canvas.draw()
        
if __name__ == '__main__':
    master_window: Tk = Tk()
    IRON_FLY(master_window)
    master_window.mainloop()
