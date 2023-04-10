from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import base64
from PIL import Image
import threading
import sys
import requests
from io import BytesIO
import urllib.request



class MyApplication:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("900x500")
        self.window.title("IMAGE DOWNLOADER")
        logo = tk.PhotoImage(file="ICON.ico")
        logo = logo.subsample(2)
        self.window.iconphoto(True,logo)
        
        ##counters
        self.infocount = 1

        # Create the two frames

        self.right_frame = tk.Frame(self.window, width=400, height=300, bg="gray")
        self.right_frame.pack(side='right',fill="both",expand=True)

        left_frame_width = self.window.winfo_width() - self.right_frame.winfo_width()
        self.left_frame = tk.Frame(self.window, width=left_frame_width, height=300, bg="white")
        self.left_frame.pack(side="left", fill="both", expand=True)

        

        
        # Add widgets to the left frame
        self.left_label = tk.Label(self.left_frame, text="IMAGE DOWNLOADER", font=("Arial", 20))
        self.left_label.pack(pady=10, padx=10, anchor='n')
        
    
        self.middle_frame = tk.Frame(self.left_frame, bg="white")
        self.middle_frame.pack(fill="both", expand=True)
        self.middle_frame.pack_propagate(0)
        
        self.info_frame = tk.Text(self.middle_frame,bg='white',font=('Arial',10))
        self.info_frame.pack(fill='both',expand=True)
        self.info_frame.pack_propagate(0)

        self.progressbar = ttk.Progressbar(self.left_frame, orient="horizontal", length=600, mode="determinate")
        self.progressbar.pack(side="bottom")
        

        
        

        # Add widgets to the right frame
        self.right_label = tk.Label(self.right_frame, text="  Settings  ", font=("Arial", 20))
        self.right_label.pack(pady=50)

        self.start_button = tk.Button(self.right_frame, text="Start", width=10, height=2)
        self.start_button.pack(side="bottom", pady=10)
        
        self.compress_var = tk.BooleanVar(self.right_frame)
        self.compress_var.set(False)
        self.compress_checkbox = tk.Checkbutton(self.right_frame, text="Sıkıştır?", variable=self.compress_var)
        self.compress_checkbox.pack(side='bottom',pady=10)
        
        self.models = ["Web site Zorlayıcı Model","Hızlı Model","Hızlı Model 2"]
        self.selected_model = tk.StringVar(self.right_frame)
        self.selected_model.set(self.models[0])
        self.model_menu = tk.OptionMenu(self.right_frame,self.selected_model, *self.models)
        self.model_menu.pack(side="bottom",pady=20)
        
        self.resize_var = tk.BooleanVar(self.right_frame)
        self.resize_var.set(False)
        self.resize_checkbox = tk.Checkbutton(self.right_frame,text='Yeniden boyutlandırma?',variable=self.resize_var,command=self.show_inputs)
        self.resize_checkbox.pack(side="bottom")
        
        
        self.entry_frame = tk.Frame(self.right_frame,width=250,height=200,bg='gray')
        
        self.width_label = tk.Label(self.entry_frame,text='Genişlik:   ')
        self.width_label.grid(row=0,column=0)
        self.entry_width = tk.Entry(self.entry_frame)
        self.entry_width.grid(row=0,column=1)
        
        self.height_label = tk.Label(self.entry_frame,text='Yükseklik:')
        self.height_label.grid(row=1,column=0)
        self.entry_height = tk.Entry(self.entry_frame)
        self.entry_height.grid(row=1,column=1)
        
         
        
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def add_info(self,text):
        count = str(self.infocount) + '< ' 
        self.info_frame.insert(tk.END,count + text + '\n')
        self.info_frame.yview_moveto(1.0)
        self.infocount += 1
    
    def update_progress(self,value):
        self.progressbar["value"] = value
        
    def show_inputs(self):
        if self.resize_var.get():
            self.entry_frame.pack(pady=20,side='bottom')
        else:
            self.entry_frame.pack_forget()

    def on_closing(self):
        sys.exit()




class Image_DOWNLOADER:
    def __init__(self) -> None:
        self.inputfile_path = './data/input/'
        self.savefile_path = './data/output/'
        self.RUNNING = True
        self.COMP = False
        self.FIRST_COMP = False
        self.model_data = 'Model 1'
        self.compress_data = False
        self.root = MyApplication()
        self.root.start_button.config(command=self.run)
        self.root.window.mainloop()
       
    def setup_driver(self,headless):
            options = webdriver.ChromeOptions()
            options.headless = headless
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument("--log-level=3")
            services = Service("./driver/chromedriver.exe")
            services.creation_flags = CREATE_NO_WINDOW
            self.driver = webdriver.Chrome(options=options,service=services)
            self.driver.delete_all_cookies()
            self.driver.implicitly_wait(100)

    
    def read_XML(self,filename):
        def read_categories(element_name):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return BeautifulSoup(f.read(),'xml').find_all(element_name)
            except:
                pass
        data = read_categories('img') + read_categories('image')
        self.images = []
        for img in data:
            self.images.append(img.text)
            
    def read_TXT(self,filename):
        self.images = []
        with open(filename, 'r', encoding='utf-8') as f:
            self.images =  f.read().split('\n')

            
    def compress_image(self,path):
        try:
            Fsize = os.path.getsize(path)
            img = Image.open(path)
            
            quality_val = 60
            optimize_val = True
            img.save(path, 'JPEG', quality=quality_val, optimize=optimize_val)
            Lsize = os.path.getsize(path)
            if Lsize < Fsize:
                return True
            else:
                return False
        except:
            pass
    
    def resize_image(self,path):
        im = Image.open(path)
        original_witdh, original_height = im.size
        height = int((original_witdh / original_height) * self.resize_height )
        new_size = (self.resize_height-10,height)
        new_im = im.resize(new_size)
        
        floor_size = (self.resize_witdh,self.resize_height)
        new_floor = Image.new('RGB',floor_size,(255,255,255))
        x = (floor_size[0] - new_im[0]) // 2
        y = (floor_size[1] - new_im[1]) // 2
        new_floor.paste(new_im, (x,y))
        new_floor.save(path)
    
    def download(self,filename):
        def download_image_script(url,img_path):
            try:
                self.driver.get(url)
            except:
                self.root.add_info('HATA!!! {} Üzerinde bir hata oluştu!'.format(img))
            
            base64_img = self.driver.execute_script("return fetch(arguments[0]).then(response => response.blob()).then(blob => new Promise((resolve, reject) => {const reader = new FileReader();reader.onloadend = () => resolve(reader.result);reader.onerror = reject;reader.readAsDataURL(blob);}));", url)
            image_data = base64.b64decode(base64_img.split(',')[1])
            with open(img_path, "wb") as f:
                f.write(image_data)
            
            self.root.add_info('%{}: {} Kaydedildi!'.format(round(progress_value+progress_step,2),img_path))
        
        def download_image_driver(path,name):
            try:
                self.driver.get(img)
            except:
                self.root.add_info('HATA!!! {} Üzerinde bir hata oluştu!'.format(img))
            try:
                img_element = self.driver.find_element(By.TAG_NAME ,'img')
                img_element.screenshot(path+name)
                self.root.add_info('%{}: {} Kaydedildi!'.format(round(progress_value+progress_step,2),path+name))
            except:
                pass
            

        def download_image_request(url, file_path):
            try:
                response = requests.get(url)
                if not response.ok:
                    messagebox.showwarning('HATA!','Bu url ({}) için kullanılan model uygun değildir! Lütfen Zorlayıcı modda çalıştırın.'.format(url))
                    self.RUNNING = False
                    return
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                self.root.add_info('%{}: {} Kaydedildi!'.format(round(progress_value+progress_step,2),file_path))
            except Exception as e:
                self.root.add_info('HATA!!! {} Üzerinde bir hata oluştu!'.format(img))
                
        def download_image_urllib(url, file_path):
            try:
                urllib.request.urlretrieve(url, file_path)
                self.root.add_info('%{}: {} Kaydedildi!'.format(round(progress_value+progress_step,2),file_path))
            except Exception as e:
                messagebox.showwarning('HATA!','Bu url ({}) için kullanılan model uygun değildir! Lütfen Zorlayıcı modda çalıştırın.'.format(url))
                self.RUNNING = False
                return
                
        
        
        
            
        def update_progress_bar(value):
            self.root.update_progress(value)
            self.root.window.update_idletasks()
        
        def resim_boyutunu_degistir(resim_ismi, yeni_boyut):
            im = Image.open(resim_ismi)
            orjinal_genislik, orjinal_yukseklik = im.size
            oran = min(yeni_boyut[0]/orjinal_genislik, yeni_boyut[1]/orjinal_yukseklik)
            yeni_genislik = int(orjinal_genislik * oran)
            yeni_yukseklik = int(orjinal_yukseklik * oran)
            im = im.resize((yeni_genislik, yeni_yukseklik), resample=Image.Resampling.LANCZOS)
            
            yeni_zemin = Image.new('RGB', yeni_boyut, (255, 255, 255))
            x = (yeni_boyut[0] - yeni_genislik) // 2
            y = (yeni_boyut[1] - yeni_yukseklik) // 2
            
            yeni_zemin.paste(im, (x, y))
            yeni_zemin.save(resim_ismi)
        
        self.images = list(set(self.images))
        progress_step = 100 / len(self.images)
        progress_value = 0
        update_progress_bar(0)
        self.root.add_info('{}; için indirme işlemi BAŞLATILIYOR..'.format(filename))
        for img in self.images:
            if len(img) > 0:
                if img.startswith('www') or img.startswith('http'):
                    _img = str(img).rsplit('/',maxsplit=1)
                    if str(img).startswith('www'):
                        parts = _img[0].split('/')
                        img_folder = '/'.join(parts[1:])
                    else:
                        parts = _img[0].split('/')
                        img_folder = '/'.join(parts[3:])
                    img_name = _img[1]
                    img_path = self.savefile_path+img_folder +'/'
                    try:
                        os.makedirs(img_path)
                    except FileExistsError:
                        pass
                    if self.model_data == "Web site Zorlayıcı Model":
                        try:
                            download_image_script(url = img,img_path=img_path+img_name)
                        except:
                            download_image_driver(path=img_path,name= img_name)
                    elif self.model_data == "Hızlı Model":
                        download_image_request(url=img,file_path=img_path+img_name)
                    elif self.model_data == "Hızlı Model 2":
                        download_image_urllib(url=img,file_path=img_path+img_name)
                    
                    if not self.RUNNING:
                        return
                    
                    if self.resize_data:
                        resim_boyutunu_degistir(resim_ismi=img_path+img_name,yeni_boyut=(self.resize_witdh,self.resize_height))
                    
                    if self.compress_data:
                        if not self.FIRST_COMP:
                            if not self.compress_image(path=img_path+img_name):
                                tk.Tk().withdraw()
                                msg = messagebox.askyesno('Uyarı!','İndirilen dosya zaten sıkıştırılmış olarak. Halen sıkıştırmaya devam etmek istiyor musunuz? \n\nNOT: Sıkıştırılmış dosyaları sıkıştırmaya çalışırsanız boyutları azalmak yerine çoğunlukla artar.')
                                if msg:
                                    self.COMP = True
                                else:
                                    self.compress_data = False  
                            else:
                                self.COMP = True                  
                            self.FIRST_COMP = True
                        if self.COMP:
                            self.compress_image(path=img_path+img_name)
                progress_value += progress_step
                update_progress_bar(progress_value)
            else:
                progress_value += progress_step
                update_progress_bar(progress_value)  
        progress_value += progress_step
        update_progress_bar(progress_value)
        self.root.add_info('{}; için indirme işlemi BAŞARILI!'.format(filename))
        if self.model_data == "Web site Zorlayıcı Model":
            self.driver.quit()
        
    def start_download(self):
        self.files = os.listdir(self.inputfile_path)
        for file in self.files:
            if not self.RUNNING:
                break
            if self.model_data == "Web site Zorlayıcı Model":
                self.setup_driver(False)
            if '.txt' in file.lower():
                self.read_TXT(self.inputfile_path+file)
                self.download(file)
            if '.xml' in file.lower():
                self.read_XML(self.inputfile_path+file)
                self.download(file)
        if self.RUNNING:
            self.root.add_info('TÜM FOTOĞRAFLAR BAŞARIYLA İNDİRİLDİ!')
        else:
            self.root.add_info('INDIRME ISLEMI DURDURULDU')
        try:
            self.driver.quit()
        except:
            pass
        self.root.start_button.config(state='normal')
        self.root.resize_checkbox.config(state='normal')
        self.root.compress_checkbox.config(state='normal')
        self.root.entry_width.config(state='normal')
        self.root.entry_height.config(state='normal')
        self.root.model_menu.config(state='normal')

    def run(self):
        self.RUNNING = True
        if self.root.resize_var.get():
            try:
                self.resize_witdh = int(self.root.entry_width.get())
            except ValueError:
                messagebox.showwarning('Uyarı!',"Boyutlandırma 'Genişliği' sayılardan oluşmalı!")
                return
            if self.resize_witdh < 500:
                messagebox.showwarning('Uyarı!',"Boyutlandırma 'Genişliği' 500px'den küçük olamaz.")
                return
            try:
                self.resize_height = int(self.root.entry_height.get())
            except:
                messagebox.showwarning('Uyarı!',"Boyutlandırma 'Yüksekliği' sayılardan oluşmalı!")
                return
            if self.resize_height < 500:
                messagebox.showwarning('Uyarı!',"Boyutlandırma 'Yüksekliği' 500px'den küçük olamaz.")
                return
            self.resize_data = True
        else:
            self.resize_data = False
        
        self.root.start_button.config(state='disabled')
        self.root.resize_checkbox.config(state='disabled')
        self.root.compress_checkbox.config(state='disabled')
        self.root.entry_width.config(state='disabled')
        self.root.entry_height.config(state='disabled')
        self.root.model_menu.config(state='disabled')
        self.model_data = self.root.selected_model.get()
        self.compress_data = self.root.compress_var.get()
        t = threading.Thread(target=self.start_download)
        t.start()
    

Image_DOWNLOADER()