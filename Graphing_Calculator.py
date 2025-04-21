from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider
from tkinter import*
import tkinter as tk
from tkinter import ttk
import numpy
from tkinter import messagebox as msg
class Plotter():
    def __init__(self,frame_curve):
        self.figure=Figure(figsize=(10,3),dpi=70)
        self.plot_1=self.figure.add_subplot(111)
        self.canv=FigureCanvasTkAgg(self.figure,master=frame_curve)
        self.canv.get_tk_widget().grid(row=0,column=0)
        self.plot_1.grid()
        self.lim=5
        self.x=None
        self.y=None
        self.gry_memory={}
        self.grx_memory={}
        self.mem_index=1
        self.mem_index_b=1
        self.equation={}
    def draw_curve(self,x,y,equation):
        self.gry_memory.update({self.mem_index:y})
        self.grx_memory.update({self.mem_index:x})
        self.equation.update({self.mem_index:equation})
        self.mem_index_b=self.mem_index
        self.mem_index+=1
        lim=self.lim
        self.x=x
        self.y=y
        self.plot_1.clear()
        self.plot_1.grid()
        self.plot_1.set_ylim(-lim,lim)
        self.plot_1.set_xlim(-lim,lim)
        self.plot_1.plot(x,y,color="black")
        self.canv.draw()
    def graph_zoom(self,event):
        if event.delta>0:
            self.lim/=1.2
            self.plot_1.set_ylim(-self.lim,self.lim)
            self.plot_1.set_xlim(-self.lim,self.lim)
            self.canv.draw()
        if event.delta<0:
            self.lim+=1
            self.plot_1.set_ylim(-self.lim,self.lim)
            self.plot_1.set_xlim(-self.lim,self.lim)
            self.canv.draw()
    def prev_gr(self):
        if self.mem_index_b>1:
            self.mem_index_b-=1
            self.plot_1.clear()
            self.plot_1.set_ylim(-self.lim,self.lim)
            self.plot_1.set_xlim(-self.lim,self.lim)
            self.plot_1.grid()
            self.plot_1.plot(self.grx_memory[self.mem_index_b],self.gry_memory[self.mem_index_b],label=self.equation[self.mem_index_b])
            self.plot_1.legend()
            self.canv.draw()
        else:
            pass
    def next_gr(self):
        try:
            if self.mem_index_b<self.mem_index:
                self.mem_index_b+=1
                self.plot_1.clear()
                self.plot_1.set_ylim(-self.lim,self.lim)
                self.plot_1.set_xlim(-self.lim,self.lim)
                self.plot_1.grid()
                self.plot_1.plot(self.grx_memory[self.mem_index_b],self.gry_memory[self.mem_index_b],label=self.equation[self.mem_index_b])
                self.plot_1.legend()
                self.canv.draw()
            else:
                pass
        except:
            pass
    def clear_memory(self):
        self.gry_memory={}
        self.grx_memory={}
        self.mem_index=1
        self.mem_index_b=1
    def move_graph(self,event):
        pass
class Interface():
    def __init__(self,win,win_m,frame_curve,fr_curve_info,plotter):
        w=10
        h=1
        self.win_m=win_m
        self.win_m.bind("<MouseWheel>",lambda event:[plotter.graph_zoom(event)])
        self.frame_curve=frame_curve
        self.fr_curve_info=fr_curve_info
        self.win=win
        self.label=Label(frame_curve,text="",fg="red")
        self.label.grid(row=0,column=1)
        self.label_curve=Label(fr_curve_info,text="",fg="green")
        self.label_curve.grid(row=1,column=0)
        self.label_domain=Label(fr_curve_info,text="",fg="green")
        self.label_domain.grid(row=1,column=1)
        self.fn_curve=Label(fr_curve_info,text="",fg="green")
        self.fn_curve.grid(row=0,column=0)
        self.btn_next=ttk.Button(win_m,text="Next",style='Left1.TButton',command=lambda:[plotter.next_gr()])
        self.btn_prev=ttk.Button(win_m, text="Prev",style='Left1.TButton',command=lambda:[plotter.prev_gr()])
        label2=Label(win,text="f(x)=",font=("Ariel",25)).grid(row=2,column=0)
        self.btn_prev.place(relx=.15,rely=.20)
        self.btn_next.place(relx=.15,rely=.25)
    def display_info(self,err,eqn,domain_n,domain_p,roots):
        if err==None:
            self.label.grid_forget()
            self.label=Label(frame_curve,text="",fg="red")
            self.label.grid(row=0,column=1)
        if err==True:
            #self.label.config(text="Check expression or rewrite expression after pressing Ctrl+c")
            self.label.config(text="?",font="Ariel 20")
        self.label_curve.config(text="No. of times curve croses x-axis: "+str(roots),font=("Ariel",10))
        self.label_curve.grid(row=1,column=0)
        self.label_domain.config(text="in domain= ("+str(domain_n)+","+str(domain_p)+")",font=("Ariel",10))
        self.label_domain.grid(row=1,column=1)
        self.fn_curve.config(text="Showing Graph For f(x)= "+str(eqn),font=("Ariel",10))
        self.fn_curve.grid(row=0,column=0)
    def ask(self):
        ans=msg.askquestion("Exit","Exit?")
        if ans=='yes':
            self.win_m.withdraw()
            exit()
        else:
            pass
    def highlight(self):
        pass
class Process():
    def __init__(self,plotter,interface):
        self.interface=interface
        self.plotter=plotter
        self.prev_curve=[]
       # self.btn_1=Button(interface, text="test",bg="blue",fg="white",command=lambda:[plotter.draw_curve([-1,0,1,2],[-1,0,1,2])]).pack()
    def evaluation(self,eqn,domain_n,domain_p):
        x=numpy.arange(domain_n,domain_p,0.01)
        y=[]
        roots=0
        functions=['sin','cos','tan','log','exp','cosec','sec','cot']
        modified_functions={'sec':'1/numpy.cos','cosec':'1/numpy.sin','cot':'1/numpy.tan'}
        operators=['*','/','+','-','.']
        operator_=['*','/','.']
        equation=eqn
        try:
            err=None
            new_eqn=""
            j=0
            word=""
            edit_eqn=""
            for i in range(0,len(eqn)):
                if eqn[i]=='x':
                    if i!=0 and eqn[i-1].isdigit():
                        edit_eqn+="*x"
                    else:
                        edit_eqn+="x"
                elif eqn[i].isalpha():
                    if i!=0 and eqn[i-1].isdigit():
                        edit_eqn+="*"
                    edit_eqn+=str(eqn[i])
                else:
                    edit_eqn+=str(eqn[i])
            eqn=edit_eqn
            eqn_l=len(eqn)
            print(eqn)
            for i in range(0,eqn_l):
                if eqn[i]=='x' and j==i:
                    j+=1
                    if i!=0 and eqn[i-1].isdigit():
                        #print(eqn[i-1])
                        print("mult_with_digit")
                        new_eqn+="*"
                    else:
                        new_eqn+="a"
                        if i<eqn_l-1 and eqn[i+1]=='(' or eqn[i+1]=='x':
                            new_eqn+="*"
                    #self.interface.get_power()
                elif eqn[i].isalpha() and eqn[i]!='x' and j==i:
                    word=""
                    j=i
                    while (word not in functions or eqn[j].isalpha()) and j<eqn_l:
                        word+=str(eqn[j])
                        j=j+1
                    if word not in functions:
                        err=True
                        #msg.showwarning("Invalid expression","Couldn't identify function '"+str(word)+"'")
                        break
                    else:
                        err=None
                        print(word,end=" |")
                        print("")
                        if word=="exp":
                            if i!=0 and (eqn[i-1].isdigit() or eqn[i-1]=='x'):
                                new_eqn+="*"
                            new_eqn+="numpy."+word
                        elif word in modified_functions:
                                new_eqn+=str(modified_functions[word])
                        else:
                            if i!=0 and (eqn[i-1].isdigit() or eqn[i-1]=='x'):
                                new_eqn+="*"
                            else:
                                new_eqn+="numpy."+word
                        #word=math.inf
                elif eqn[i]=='^':
                    new_eqn+="**"
                    j+=1
                else:
                    if j!=i:
                        continue
                    else:
                        print(eqn[i])
                        new_eqn+=str(eqn[i])
                        j=j+1
            print(new_eqn)
            print(err)
        except Exception as e:
            print(e)
            #msg.showinfo("Invalid expression","Error")
            #err=True
            pass
        new_l=len(new_eqn)
        o_braces=0
        c_braces=0
        edit_len=new_l
        for i in range(0,new_l):
            if i<edit_len and new_eqn[i]=='(':
                if new_eqn[i+1] in operator_:
                    print(len(new_eqn))
                    rest_str=""
                    prev_str=""
                    for j in range(i+2,new_l):
                        rest_str+=str(new_eqn[j])
                    for j in range(0,i+1):
                        prev_str+=str(new_eqn[j])
                    new_eqn=prev_str+rest_str
                    edit_len=len(new_eqn)
                    print(len(new_eqn))
                    print("edited: "+new_eqn)
                o_braces+=1
            if i<edit_len and new_eqn[i]==')':
                if new_eqn[i-1] in operators:
                    print(len(new_eqn))
                    rest_str=""
                    prev_str=""
                    for j in range(i,new_l):
                        rest_str+=str(new_eqn[j])
                    for j in range(0,i-1):
                        prev_str+=str(new_eqn[j])
                    new_eqn=prev_str+rest_str
                    edit_len=len(new_eqn)
                c_braces=c_braces+1
        if new_eqn[edit_len-1] in operators:
            if new_eqn[edit_len-1]=='/' or new_eqn[edit_len-1]=='*':
                new_eqn=new_eqn+"1"
            else:
                new_eqn=new_eqn+"0"
        while o_braces>c_braces:
            new_eqn=new_eqn+")"
            c_braces=c_braces+1
        print(new_eqn)
        a=x[0]
        exp2="""global d
"""
        exp2=exp2+"d="+new_eqn
        exec(exp2)
        p=d
        for i in range(0,len(x)):
            a=x[i]
            exec(exp2)
            y.append(d)
            if -1<d<1 and p<0:
                if d>0:
                    roots+=1
                elif d==0:
                    roots+=1
            if -1<d<1 and p>0:
                if d<0:
                    roots+=1
                elif d==0:
                    roots+=1
            p=d
        if self.prev_curve==y:
            pass
        else:
            self.plotter.draw_curve(x,y,equation)
            self.interface.display_info(err=err,eqn=eqn,domain_p=domain_p,domain_n=domain_n,roots=roots)
            self.prev_curve=y

def main(process):
    t=inp.get().lower()
    if inp1.get().lower()!=t :
        inp1.set(t)
        if 'x' in t:
            print(domain_n.get(),domain_p.get())
            process.evaluation(t,domain_n.get(),domain_p.get())
win=Tk()
win.minsize(986,590)
#icon=PhotoImage(file=r"C:\Users\91788\Downloads\curve_icon.png")
#win.iconphoto(False,icon)
win.title("Graphing Calculator")
frame_curve=Frame(win,cursor="hand1")
frame_curve.place(relx=.23,rely=.0)
frame=Frame()
frame.pack(fill=BOTH,expand=True)
frame.place(in_=win,anchor="c",relx=.6,rely=.5,width=950,height=50)
fr_curve_info=Frame(win)
fr_curve_info.pack(fill=BOTH,expand=True)
fr_curve_info.place(in_=win,anchor="c",relx=.5,rely=.4,width=950,height=50)
plotter=Plotter(frame_curve)
app=Interface(frame,win,frame_curve,fr_curve_info,plotter)
process=Process(plotter,app)
inp=StringVar()
inp1=StringVar()
domain_n=IntVar()
domain_p=IntVar()
domain_n.set(-4)
domain_p.set(4)
Display=Entry(frame,font="Ariel 15",textvariable=inp)
Display.focus_set()
Display.grid(row=2,column=1,columnspan=170,ipadx=170,ipady=10)
spnbox_p=Spinbox(win,textvariable=domain_p,from_=1,to=10,state='readonly',command=main(process)).pack(side=RIGHT)
spnbox_n=Spinbox(win,textvariable=domain_n,from_=-10,to=0,state='readonly',command=main(process)).pack(side=RIGHT)
#btn_draw=Button(frame, text="PLOT GRAPH",bg="green",fg="white",command=lambda:[process.evaluation(inp.get())],activebackground="orange")
#btn_draw.grid(row=10,column=0)
win.bind("<Return>",lambda event:[process.evaluation(inp.get(),domain_n=domain_n.get(),domain_p=domain_p.get())])
win.bind("<Control-c>",lambda event:[plotter.clear_memory()])
win.bind("<Control-Up>",lambda event:[plotter.move_graph("U")])
win.bind("<Control-Down>",lambda event:[plotter.move_graph("D")])
win.bind("<Control-Left>",lambda event:[plotter.move_graph("L")])
win.bind("<Control-Right>",lambda event:[plotter.move_graph("R")])
win.bind_all("<Key>",lambda event:[main(process)])
win.protocol("WM_DELETE_WINDOW",lambda:[app.ask()])
#pr=Process()
#pr.evaluation("x*x+exp(x)+log(x-1)+sin(xxxx)-2*log(x)+(2x*(x")
#win.bind("<MouseWheel>",lambda event:[p.graph_zoom(event)])
win.mainloop()
#p.draw_curve([-1,0,1,2],[-1,0,1,2])

