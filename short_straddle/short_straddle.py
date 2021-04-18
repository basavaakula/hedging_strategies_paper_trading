#!/usr/bin/python3

import sys
sys.path.append("..")

from imports.packages import *

class SHORT_STRADDLE:
    def __init__(self,root)->None:
        self.first_run = True
        self.stop = False
        self.interval = 10.
        self.buy_pe_limit: List[float] = []
        self.sell_pe_limit: List[float] = []
        self.sell_ce_limit: List[float] = []
        self.buy_ce_limit: List[float] = []
        self.imp_strikes: List[float] = []
        self.imp_my_buy_price: List[float] = []
        self.nse_adapter = NC.OC_DATA()
        self.root = root
    def setup_gui(self,my_master: Frame)->None:
        #my_master.pack(anchor='sw',fill='both', expand=True)
        #my_master.grid(row=1,column=0,sticky='nsew')
        #my_master.geometry('800x600')
        #my_master.grid_rowconfigure(0, weight=0) 
        #my_master.grid_columnconfigure(0, weight=1) 
        #my_master.pack(fill='both')
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
        
        
        self.start_button: Button = tk.Button(top_frame,text='Trade',command=self.main_recursive,width=15,bg='green',fg='white',font=("TkDefaultFont", 10, "bold"))
        #self.start_button.pack(anchor=N, expand=False, side=LEFT)
        self.start_button.grid(row=row_idx,column=0,sticky='nsw',columnspan=2)#,padx=pdx,pady=pdy)
        self.start_button.configure(state='disabled')
        row_idx = row_idx + 1
        
        self.load_button: Button = tk.Button(top_frame,text='Load trade',command=self.load_file,width=15,bg='yellow',fg='black',font=("TkDefaultFont", 10, "bold"))
        self.load_button.grid(row=row_idx,column=0,sticky='nsw',columnspan=2)
        self.load_button.configure(state='normal')
        
        self.fig = Figure(figsize = (3, 3), dpi = 200) 
        #fig.subplots_adjust(left=0, right=1, top=1, bottom=0) 
        self.plot1 = self.fig.add_subplot(111)
        self.plot1.tick_params(axis='both', which='minor', labelsize=8)

        self.canvas = FigureCanvasTkAgg(self.fig,master = bot_frame)
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
        self.root.default_save_dir+self.combo_box_stock.get()+'_'+self.date_combo_box_stock.get()+'_'+date.today().strftime("%b-%d-%Y")+'.csv.lcs'
        if(not path.exists(save_name)):
            df_export: pd.DataFrame = pd.DataFrame()
            df_export['Strikes'] = (self.df['Strikes'].tolist())[0:-1]
            df_export['Buy_price'] = (self.df['My_price'].tolist())[0:-1]
            df_export['Qty'] = [(self.df['Qty'].tolist())[0]]*2
            df_export.to_csv(save_name)

    def load_file(self): 
        file = askopenfile(mode ='r', filetypes =[('CSV files', '*.lcs')],initialdir=self.root.default_save_dir)
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
    
    def import_iron_condor(self):
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
        self.strikes_away = float(self.vix_combo_box.get())
        self.start_button.configure(state='normal')
        self.import_button.configure(state='normal')
    def set_expiry_date(self,event):
        self.nse_adapter.set_stock(self.combo_box_stock.get())
        self.nse_adapter.get_expiry_dates()
        self.date_combo_box_stock['values'] = tuple(self.nse_adapter.expiry_dates)
        qtys = [x*int(self.root.indices_lot[self.combo_box_stock.get()]) for x in range(1,11)]
        self.qty_combo_box['values'] = qtys
        self.date_combo_box_stock.set(self.nse_adapter.expiry_dates[0])
        self.qty_combo_box.set(qtys[0])
        self.start_button.configure(state='normal')
    
    def main_recursive(self)->None:
        if(self.first_run):
            #self.start_button.configure(state='disabled')
            #self.combo_box_stock.configure(state='disabled')
            #self.date_combo_box_stock.configure(state='disabled')
            #self.qty_combo_box.configure(state='disabled')
            self.df_iron_condor()
            self.first_run = False
        self.curr_time = time.time()
        time_passed = int(self.curr_time-self.prev_time)
        if(time_passed>=self.interval):
            #self.refresh_data()
            self.df_iron_condor()
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
                df = self.df_iron_condor()
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

    
    def df_iron_condor(self):
        df: pd.DataFrame = pd.DataFrame()
        df_graph: pd.DataFrame = pd.DataFrame()
        
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
        
        curr_price = ce_data['underlyingValue'][0]
        #self.sh_window.title('Paper trading-->'+self.combo_box_stock.get()+' ('+str(curr_price)+' ) @--'+datetime.now().strftime("%H:%M:%S"))
        if(self.first_run):
            diff = [abs(x-curr_price) for x in strike_prices]
            self.min_pos = diff.index(min(diff))
            self.my_atm = strike_prices[self.min_pos]
            
        strike_idx = int(self.min_pos)
        if(len(self.imp_strikes)==0):
            ce_otm_data = ce_data.iloc[strike_idx]
            pe_otm_data = pe_data.iloc[strike_idx]
        else:
            ce_otm_data = ce_data.iloc[iron_condor_strikes[0]]
            pe_otm_data = pe_data.iloc[iron_condor_strikes[0]]
            
        sell_ce_idx = strike_idx
        sell_pe_idx = strike_idx
            
            

        
        pd_concat = pd.concat([ce_otm_data,pe_otm_data],axis=0)
        sell_buy_signs = [-1.,-1.]
        lot_list = [float(self.qty_combo_box.get())]*2
        qty_list = list(map(mul,lot_list,sell_buy_signs))
        ltp_list = list(map(float,pd_concat['lastPrice'].tolist()))
        if(self.first_run and len(self.imp_strikes)==0):
            self.my_buy_price = pd_concat['lastPrice'].tolist()
        
        net_points: List[float] = list(map(mul,sell_buy_signs,self.my_buy_price))
        net_points = list(map(lambda x: x*-1,net_points))
        tt = list(map(sub,ltp_list,self.my_buy_price))
        df['Strikes'] = pd_concat['strikePrice'].tolist() 
        df['Qty'] = qty_list
        df['My_price'] = list(map(float,self.my_buy_price))
        df['LTP'] = ltp_list
        df['P&L'] = list(map(mul,tt,qty_list))
        df['P&L'] =  df['P&L'].round(3)
        df['OI_change'] =  pd_concat['pchangeinOpenInterest'].tolist()
        df['OI_change'] = df['OI_change'].round(3)
        total_row = {'Strikes':' ','Qty':' ','My_price':str(round(sum(net_points),2)),'LTP':'Total ','P&L':df['P&L'].sum(),'OI_change': ' '}
        df = df.append(total_row,ignore_index=True)

        
        for i in range(len(strike_prices)):
            if(i>=sell_pe_idx):
                val = self.my_buy_price[1]
            else:
                val = self.my_buy_price[1]-abs(strike_prices[i]-strike_prices[sell_pe_idx])
            self.sell_pe_pl.append(val)
            
            if(i<=sell_ce_idx):
                val = self.my_buy_price[0]
            else:
                val = self.my_buy_price[0]-abs(strike_prices[i]-strike_prices[sell_ce_idx])
            self.sell_ce_pl.append(val)
        
        comb_pl = list(map(add,self.sell_ce_pl,self.sell_pe_pl)) 
        comb_pl = list(map(lambda x:x*float(self.qty_combo_box.get()),comb_pl))
        df_graph['sell_call'] = comb_pl

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
        self.plot1.plot(self.strike_prices,self.sell_pe_pl,'--',lw=.5,label='SELL PE ('\
        +str((self.df['Strikes'].tolist())[0])+'>'+str((self.df['P&L'].tolist())[0])+')')
        self.plot1.plot(self.strike_prices,self.sell_ce_pl,'--',lw=.5,label='SELL CE ('\
        +str((self.df['Strikes'].tolist())[1])+'>'+str((self.df['P&L'].tolist())[1])+')')
        self.plot1.legend()
        self.plot1.axvline(x=(self.pd_concat['strikePrice'].tolist())[0],linestyle='--',color='g',lw=.8)
        self.plot1.axvline(x=(self.pd_concat['strikePrice'].tolist())[1],linestyle='--',color='r',lw=.8)
        self.plot1.plot(self.curr_price,self.df['P&L'].iloc[0:-1].sum(),'D',markersize=2)
        #self.plot1.plot(self.curr_price,(self.df['P&L'].tolist())[0],'s',markersize=2)
        #self.plot1.plot(self.curr_price,(self.df['P&L'].tolist())[1],'s',markersize=2)
        #self.plot1.plot(self.curr_price,(self.df['P&L'].tolist())[2],'s',markersize=2)
        #self.plot1.plot(self.curr_price,(self.df['P&L'].tolist())[3],'s',markersize=2)
        self.plot1.text(1.0*min(self.strike_prices),.2*max(self.comb_pl),'max_profit ='+str(round(max(self.comb_pl),2)),color='green',fontsize='6')
        self.plot1.text(1.1*min(self.strike_prices),.5*max(self.comb_pl),'max_loss = '+str(round(min(self.comb_pl),2)),color='red',fontsize='6')
        clr = 'red'
        if(self.df['P&L'].iloc[0:-1].sum()>0):
            clr = 'green'
        self.plot1.text(1.01*self.curr_price,1.01*self.df['P&L'].iloc[0:-1].sum(),str(self.df['P&L'].iloc[0:-1].sum()),color=clr,fontsize='4')
        self.root.master_wd.title('Paper trading-->'+self.combo_box_stock.get()+' ('+str(self.curr_price)+' ) @--'+datetime.now().strftime("%H:%M:%S"))
        for l in self.fig.gca().lines:
            l.set_alpha(self.root.fig_alpha)
        self.canvas.draw()
        
if __name__ == '__main__':
    master_window: Tk = Tk()
    IRON_CONDOR(master_window)
    master_window.mainloop()
