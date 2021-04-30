#!/usr/bin/python3

from imports.packages import *
from iron_condor import iron_condor as IC
from iron_fly import iron_fly as IF
from oi_analysis import oi_analysis as OI
from oi_history import oi_history as OIH
from oi_live import oi_live as OIL
from oi_chart_hist import oi_chart_hist as OCH
from option_chain import option_chain as OC
from diag_calender_spread import diag_calender_spread as DCS
from long_calender_spread import long_calender_spread as LCS
from long_straddle import long_straddle as LS
from short_straddle import short_straddle as SS
from short_strangle import short_strangle as SST
from my_trades import my_trades as MT


class PAPER_TRADING:
    def __init__(self,wd:Tk)->None:
        wd.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.indices: List[str] = ['NIFTY','BANKNIFTY','ICICIBANK','DRREDDY','RELIANCE','ASHOKLEY','TATAMOTORS','SBIN']
        self.indices_lot: dict[str,str]={'NIFTY':'75','BANKNIFTY':'25','ICICIBANK':'1375','DRREDDY':'125','RELIANCE':'250','ASHOKLEY':'9000','TATAMOTORS':'5700', \
                                         'SBIN':'3000'}
        self.fig_alpha = .3
        self.default_save_dir = '/home/abasava/MEGA/Personal_docs/paper_trade_journals/'
        self.ic  = IC.IRON_CONDOR(self)
        self.iff  = IF.IRON_FLY(self)
        self.oia  = OI.OI_ANALYSIS(self)
        self.oc  = OC.OCHAIN(self)
        self.och  = OCH.OI_CH_HIST(self)
        self.oih  = OIH.OI_HISTORY(self)
        self.oil  = OIL.OI_LIVE(self)
        self.dcs = DCS.DIAG_CALEN_SPREAD(self)
        self.lcs = LCS.LONG_CALEN_SPREAD(self)
        self.ls = LS.LONG_STRADDLE(self)
        self.ss = SS.SHORT_STRADDLE(self)
        self.sst = SST.SHORT_STRANGLE(self)
        self.mt = MT.MY_TRADES(self)
        self.strategies =\
                {'option_chain':self.oc,'oi_charts_hist':self.och,'iron_condor':self.ic,'diag_calender_spread':self.dcs,'long_calender_spread':self.lcs,\
                'long_straddle':self.ls,'short_straddle':self.ss,'short_strangle':self.sst,'iron_fly':self.iff,'oi_charts':self.oia,\
                'oi_history':self.oih,'TRADES':self.mt,'oi_live':self.oil}
        self.setup_interface(wd)
        for strat in enumerate(self.strategies.keys()):
            self.strategies[strat[1]].setup_gui(self.NBF[strat[0]])
    def on_closing(self):
        self.master_wd.destroy()
    def set_active_strategy_tab(self,event)->None:
        active_strat = self.cb_strategy.get()
        #for i in range(len(self.strategies)):
        for strat in enumerate(self.strategies.keys()):
            if strat[1] != active_strat:
                self.NB.tab(strat[0],state='disabled')
            else:
                self.NB.tab(strat[0],state='normal')
                self.NB.select(strat[0])
    def setup_interface(self,wd:Tk)->None:
        self.master_wd: Tk = wd
        self.master_wd.title('Paper trading')
        window_width: int = self.master_wd.winfo_reqwidth()
        window_height: int = self.master_wd.winfo_reqheight()
        position_right: int = int(self.master_wd.winfo_screenwidth() / 2 - window_width / 2)
        position_down: int = int(self.master_wd.winfo_screenheight() / 2 - window_height / 2)
        self.master_wd.geometry("1000x800+300+100")
        self.master_wd.grid_rowconfigure(0, weight=0)
        self.master_wd.grid_columnconfigure(0, weight=1)
        #self.master_wd.resizable(0,0)
        
        top_frame: Frame = Frame(self.master_wd)
        #top_frame.grid(row=0,column=0,sticky='nsew')
        top_frame.pack(fill='x', expand=False, side=TOP)
        bot_frame: Frame = Frame(self.master_wd)
        #bot_frame.grid(row=1,column=0,sticky='nsew')
        bot_frame.pack(fill='both', expand=True, side=TOP)
        
        pdx = 5
        pdy = 5
        #var_stock: StringVar = StringVar()
        #var_stock.set(" ")
        #lbl_stock: Label = Label(top_frame,text='Underlying',justify=LEFT,font=("TkDefaultFont", 10,"bold"),width=10)
        #lbl_stock.grid(row=0,column=0,sticky='nw',padx=pdx,pady=pdy)
        #self.combo_box_stock = Combobox(top_frame,width=10,textvariable=var_stock) 
        #self.combo_box_stock.grid(row=0,column=1,sticky='nw',padx=pdx,pady=pdy)
        #self.combo_box_stock.configure(state='readonly')
        ##self.combo_box_stock['values'] = self.indices
        ##self.combo_box_stock.bind('<<ComboboxSelected>>', self.set_expiry_date)
        
        var_strat: StringVar = StringVar()
        var_strat.set(" ")
        lbl_strat: Label = Label(top_frame,text='Strategy',justify=LEFT,font=("TkDefaultFont", 10,"bold"),width=10)
        lbl_strat.grid(row=0,column=2,sticky='nw',padx=pdx,pady=pdy)
        self.cb_strategy = Combobox(top_frame,width=30,textvariable=var_strat) 
        self.cb_strategy.grid(row=0,column=3,sticky='nw',padx=pdx,pady=pdy)
        self.cb_strategy.configure(state='readonly')
        self.cb_strategy['values'] = list(self.strategies.keys())
        self.cb_strategy.bind('<<ComboboxSelected>>', self.set_active_strategy_tab)

        
        self.NB: Notebook = Notebook(bot_frame)
        self.NB.pack(anchor='n',fill="both", expand=True)
        self.NBF: List[Frame] = []
        
        for strat in enumerate(self.strategies.keys()):
            self.NBF.append(Frame(self.NB))
            self.NB.add(self.NBF[-1],text=strat[1])
            self.NB.tab(strat[0],state='disabled')
        
        #self.ic.setup_gui(self.NBF[0])


if __name__ == '__main__':
    master_window: Tk = Tk()
    PAPER_TRADING(master_window)
    master_window.mainloop()
