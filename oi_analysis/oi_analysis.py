#!/usr/bin/python3

import sys
import numpy as np
sys.path.append("..")

from imports.packages import *

class OI_ANALYSIS:
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
        top_frame.pack(anchor='nw',fill='y', expand=False, side=LEFT)
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
        self.date_combo_box_stock.bind('<<ComboboxSelected>>', self.event_chng_expiry_date)
        row_idx = row_idx + 1
        
        intvl_var_stock: StringVar = StringVar()
        intvl_var_stock.set(" ")
        lbl_intvl: Label = Label(top_frame,text='Refresh (seconds)',justify=LEFT,font=("TkDefaultFont", 10,"bold"))
        lbl_intvl.grid(row=row_idx,column=0,sticky='nsw',padx=pdx,pady=pdy)
        self.cbox_intvl = Combobox(top_frame,width=10,textvariable=intvl_var_stock) 
        self.cbox_intvl.grid(row=row_idx,column=1,sticky='nsw',padx=pdx,pady=pdy)
        self.cbox_intvl.configure(state='readonly')
        self.cbox_intvl['values'] = list(range(10, 600, 20))
        self.cbox_intvl.bind('<<ComboboxSelected>>', self.event_chng_intvl)
        row_idx = row_idx + 1
        
        
        #self.start_button: Button = tk.Button(top_frame,text='Fetch OI',command=self.main_recursive,width=15,bg='green',fg='white',font=("TkDefaultFont", 10, "bold"))
        self.start_button: Button = tk.Button(top_frame,text='Fetch OI',command=self.main_recursive,width=15,bg='green',fg='white',font=("TkDefaultFont", 10, "bold"))
        self.start_button.grid(row=row_idx,column=0,sticky='nsw',columnspan=2)#,padx=pdx,pady=pdy)
        self.start_button.configure(state='disabled')
        row_idx = row_idx + 1
        
        #fig = Figure(figsize = (3, 3), dpi = 200)
        fig,ax = plt.subplots(2)
        #fig.subplots_adjust(left=0, right=1, top=1, bottom=0) 
        self.plot1 = ax[0]
        self.plot1.tick_params(axis='both', which='minor', labelsize=8)
        self.plot2 = ax[1]
        self.plot2.tick_params(axis='both', which='minor', labelsize=8)
        
        
        self.canvas = FigureCanvasTkAgg(fig,master = bot_frame)
        #self.canvas.get_tk_widget().grid(row=1,column=1,sticky='nswe',padx=pdx,pady=pdy) 
        self.canvas.get_tk_widget().pack(fill='both',expand=True,side=TOP)
    
    def set_expiry_date(self,event):
        self.nse_adapter.set_stock(self.combo_box_stock.get())
        self.nse_adapter.get_expiry_dates()
        self.date_combo_box_stock['values'] = tuple(self.nse_adapter.expiry_dates)
        self.date_combo_box_stock.set('---')
    
    def event_chng_intvl(self,event):
        self.interval = int(self.cbox_intvl.get())
    
    def event_chng_expiry_date(self,event):
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
            self.plot_oi()
            self.first_run = False
        self.curr_time = time.time()
        time_passed = int(self.curr_time-self.prev_time)
        if(time_passed>=self.interval):
            #self.refresh_data()
            self.plot_oi()
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
                df = self.plot_oi()
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

    
    def plot_oi(self):
        #print('************* REFRESHING *****************')
        self.processed_df: pd.DataFrame = pd.DataFrame()
        
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
        self.processed_df['PCR'] = (pe_data['openInterest']/ce_data['openInterest']).round(3)
        self.processed_df['strikePrice'] = strike_prices
        width = .8*(strike_prices[1] - strike_prices[0])
        
        curr_price = ce_data['underlyingValue'][0]
        my_atm = int(curr_price)
       
        #self.draw_plot(ce_data,pe_data,strike_prices)
        self.plot1.clear()
        rects1 = self.plot1.bar(strike_prices, ce_data['openInterest'], width, label='OI',color='green',alpha=0.5)
        rects2 = self.plot1.bar(strike_prices, pe_data['openInterest'], width, label='OI',color='red',alpha=0.2)
        self.all_bars = [rects1,rects2]
        self.plot2.clear()
        rects1 = self.plot2.bar(strike_prices, ce_data['changeinOpenInterest'], width, label='OI',color='green',alpha=0.5)
        rects2 = self.plot2.bar(strike_prices, pe_data['changeinOpenInterest'], width, label='OI',color='red',alpha=0.2)
        self.all_bars2 = [rects1,rects2]

        #print(list(ce_data.columns))
        
        fsize = 10
        self.plot1.set_ylabel('Open Interest',fontsize = fsize)
        self.plot1.set_title('OI analysis--->'+datetime.now().strftime("%H:%M:%S"),fontsize = fsize)
        self.plot1.set_xticks(strike_prices)
        self.plot1.set_xticklabels(strike_prices,rotation=0)
        self.plot1.tick_params(axis='both', which='major', labelsize=fsize)
        self.plot1.locator_params(axis='x', nbins=10)
        self.plot1.axvline(x=my_atm,linestyle='--',color='g',lw=1.)

        self.plot2.set_ylabel('Change in OI',fontsize = fsize)
        self.plot2.set_xticks(strike_prices)
        self.plot2.set_xticklabels(strike_prices,rotation=0)
        self.plot2.tick_params(axis='both', which='major', labelsize=fsize)
        self.plot2.locator_params(axis='x', nbins=10)
        self.plot2.axvline(x=my_atm,linestyle='--',color='g',lw=1.)
        
        self.canvas.draw()
        self.canvas.mpl_connect("motion_notify_event", self.hover)



        self.annot = self.plot1.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="black", edgecolor="white", lw=2,alpha=0.1),
                    arrowprops=dict(arrowstyle="->"),fontsize=10)
        self.annot.set_visible(False)
        
        self.annot1 = self.plot2.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="black", edgecolor="white", lw=2,alpha=0.1),
                    arrowprops=dict(arrowstyle="->"),fontsize=10)
        self.annot1.set_visible(False)
        self.prev_time = time.time()

    def update_annot(self,bar):
        strike_price = bar.get_x()+bar.get_width()/2.
        x = bar.get_x()+bar.get_width()/2.
        y = bar.get_y()+bar.get_height()
        max_strike = (self.processed_df['strikePrice'].tolist())[-1]
        self.annot.xy = (max_strike,y)
        pcr = self.processed_df.loc[self.processed_df['strikePrice']==strike_price]
        pcr = (pcr['PCR'].tolist())[0]
        text = "{:.1f}\nPCR : {:.3f}".format(strike_price,pcr)
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)

    def update_annot1(self,bar):
        strike_price = bar.get_x()+bar.get_width()/2.
        x = bar.get_x()+bar.get_width()/2.
        y = bar.get_y()+bar.get_height()
        max_strike = (self.processed_df['strikePrice'].tolist())[-1]
        self.annot1.xy = (max_strike,y)
        pcr = self.processed_df.loc[self.processed_df['strikePrice']==strike_price]
        pcr = (pcr['PCR'].tolist())[0]
        text = "{:.1f}\nPCR : {:.3f}".format(strike_price,pcr)
        self.annot1.set_text(text)
        self.annot1.get_bbox_patch().set_alpha(0.4)

    def hover(self,event):
        vis = self.annot.get_visible()
        vis1 = self.annot1.get_visible()
        if event.inaxes == self.plot1:
            for bar_obj in self.all_bars:
                for bar in bar_obj:
                    cont, ind = bar.contains(event)
                    if cont:
                        self.update_annot(bar)
                        self.annot.set_visible(True)
                        self.canvas.draw_idle()
                        return
        if event.inaxes == self.plot2:
            for bar_obj in self.all_bars2:
                for bar in bar_obj:
                    cont, ind = bar.contains(event)
                    if cont:
                        self.update_annot1(bar)
                        self.annot1.set_visible(True)
                        self.canvas.draw_idle()
                        return
        if vis:
            self.annot.set_visible(False)
            self.canvas.draw_idle()
        if vis1:
            self.annot1.set_visible(False)
            self.canvas.draw_idle()
        
        
if __name__ == '__main__':
    master_window: Tk = Tk()
    IRON_FLY(master_window)
    master_window.mainloop()
