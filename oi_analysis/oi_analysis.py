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
        self.cbox_expiry_date = Combobox(top_frame,width=10,textvariable=date_var_stock) 
        self.cbox_expiry_date.grid(row=row_idx,column=1,sticky='nsw',padx=pdx,pady=pdy)
        #self.cbox_expiry_date.pack(anchor='nw',fill='y', expand=True, side=TOP)
        self.cbox_expiry_date.configure(state='readonly')
        self.cbox_expiry_date.bind('<<ComboboxSelected>>', self.event_chng_expiry_date)
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
        #self.start_button.grid(row=row_idx,column=0,sticky='nsw',columnspan=2)#,padx=pdx,pady=pdy)
        #self.start_button.configure(state='disabled')
        #row_idx = row_idx + 1
        
        fig,ax = plt.subplots(2)
        self.plot1 = ax[0]
        self.plot1.tick_params(axis='both', which='minor', labelsize=8)
        self.plot2 = ax[1]
        self.plot2.tick_params(axis='both', which='minor', labelsize=8)
        
        
        self.canvas = FigureCanvasTkAgg(fig,master = bot_frame)
        self.canvas.get_tk_widget().pack(fill='both',expand=True,side=TOP)
    
    def set_expiry_date(self,event):
        self.nse_adapter.set_stock(self.combo_box_stock.get())
        self.nse_adapter.get_expiry_dates()
        self.cbox_expiry_date['values'] = tuple(self.nse_adapter.expiry_dates)
        self.cbox_expiry_date.set('---')
        self.plot1.clear()
        self.plot2.clear()
        self.canvas.draw()
    
    def event_chng_intvl(self,event):
        self.interval = int(self.cbox_intvl.get())
    
    def event_chng_expiry_date(self,event):
        self.nse_adapter.set_expiry(self.cbox_expiry_date.get())
        if(self.first_run):
            self.main_recursive()
            self.cbox_intvl.set(30)
            self.interval = 30
        else:
            self.plot_oi()

    def get_closest_strike(self,strike,strikes):
        diff = [abs(x-strike) for x in strikes]
        min_pos = diff.index(min(diff))
        return strikes[min_pos]
    
    def main_recursive(self)->None:
        if(self.first_run):
            self.plot_oi()
            self.first_run = False
        self.curr_time = time.time()
        time_passed = int(self.curr_time-self.prev_time)
        if(time_passed>=self.interval):
            self.plot_oi()
        else:
            self.master_wd.after((10 * 1000),self.main_recursive)
            return
        if(not self.stop):
            self.master_wd.after((10 * 1000),self.main_recursive)
            return

    
    def plot_oi(self):
        if(self.cbox_expiry_date.get()=='---'):
            return
        self.processed_df: pd.DataFrame = pd.DataFrame()
        self.nse_adapter.get_oc_data() 
        self.processed_df['PCR'] = (self.nse_adapter.pe_data['openInterest']/self.nse_adapter.ce_data['openInterest']).round(3)
        self.processed_df['strikePrice'] = self.nse_adapter.strike_prices
        width = .8*(self.nse_adapter.strike_prices[1] - self.nse_adapter.strike_prices[0])
       
        self.plot1.clear()
        rects1 = self.plot1.bar(self.nse_adapter.strike_prices, self.nse_adapter.ce_data['openInterest'], width, label='OI',color='green',alpha=0.5)
        rects2 = self.plot1.bar(self.nse_adapter.strike_prices, self.nse_adapter.pe_data['openInterest'], width, label='OI',color='red',alpha=0.2)
        self.all_bars = [rects1,rects2]
        self.plot2.clear()
        rects1 = self.plot2.bar(self.nse_adapter.strike_prices, self.nse_adapter.ce_data['changeinOpenInterest'], width, label='OI',color='green',alpha=0.5)
        rects2 = self.plot2.bar(self.nse_adapter.strike_prices, self.nse_adapter.pe_data['changeinOpenInterest'], width, label='OI',color='red',alpha=0.2)
        self.all_bars2 = [rects1,rects2]

        
        fsize = 10
        self.plot1.set_ylabel('Open Interest',fontsize = fsize)
        self.plot1.set_title('OI analysis--->'+datetime.now().strftime("%H:%M:%S"),fontsize = fsize)
        self.plot1.set_xticks(self.nse_adapter.strike_prices)
        self.plot1.set_xticklabels(self.nse_adapter.strike_prices,rotation=0)
        self.plot1.tick_params(axis='both', which='major', labelsize=fsize)
        self.plot1.locator_params(axis='x', nbins=10)
        self.plot1.axvline(x=self.nse_adapter.atm,linestyle='--',color='g',lw=1.)

        self.plot2.set_ylabel('Change in OI',fontsize = fsize)
        self.plot2.set_xticks(self.nse_adapter.strike_prices)
        self.plot2.set_xticklabels(self.nse_adapter.strike_prices,rotation=0)
        self.plot2.tick_params(axis='both', which='major', labelsize=fsize)
        self.plot2.locator_params(axis='x', nbins=10)
        self.plot2.axvline(x=self.nse_adapter.atm,linestyle='--',color='g',lw=1.)
        
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
