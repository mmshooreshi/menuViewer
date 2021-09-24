from pickle import NONE
from fpdf import FPDF
import os
import xlrd
from PIL import Image
import requests
from io import BytesIO
import numpy 
from alive_progress import alive_bar
from listex import list_output
from os import walk

rows = []

def save_loc(pdf):
    global x_var,y_var
    x_var=pdf.get_x()
    y_var=pdf.get_y()

def set_loc(pdf):
    pdf.set_x(x_var)
    pdf.set_y(y_var)

def imgdimension(imglink):
    if(imglink.startswith=="http"):
        response = requests.get(imglink)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(imglink)
    #rgb_im = img.convert('RGBA')
    #rgb_im.mode='RGBA'
    #print(imglink[:imglink.rfind("."):1]+'.jpg')
    if(imglink[-3::]=="png"):
        png = img.convert('RGBA')
        background = Image.new('RGBA', png.size, (255,255,255))
        alpha_composite = Image.alpha_composite(background, png)
        alpha_composite= alpha_composite.convert("RGB")
        alpha_composite.save(imglink[:imglink.rfind("."):1]+'.jpg', 'JPEG', quality=90)
    #img.convert("RGB")
    #img.save(imglink[:imglink.rfind("."):1]+'.jpg', 'JPEG')
    #rgb_im.save(imglink[:imglink.rfind("."):1]+'.jpg')
    
    widthpx, heightpx = img.size
    widthmm=185
    heightmm= heightpx*(widthmm/widthpx)
    #print(widthpx,heightpx)
    return widthmm,heightmm,heightpx,widthpx

def count_added(l):
    sumv=0
    for val in list(l[:,5]):
        sumv+=int(val)
    return sumv

def mainc(pdf):
    temp=0
    global q_num,added_list
    for question in remaining_rows:
        if(question[3]!="*" and q_num<=100 and question[5]!=0 and pdf.page_no()<=1000):
            imglink=question[2]
            img_local_link=basepath+"/imgs/"+question[4]
            imglink=img_local_link
            #img_local_link = img_local_link[:img_local_link.rfind("."):1]+'.jpg'
            #edit this if you want:
            imglink=img_local_link
            box_height=imgdimension(imglink)[1]
            box_width=imgdimension(imglink)[0]
            box_widthpx=imgdimension(imglink)[3]

            global y_var,x_var
            save_loc(pdf)

            hh=int(box_height)
            if(hh>260):
                #print("in")
                ww=(250/hh)*box_width
                hh=250
                box_widthpx=ww
            
            if(int(box_widthpx)>1000):
                ww=185
                hh=(ww/185)*box_height
                xx=0
            elif(int(box_widthpx)>900):
                ww=180
                hh=(ww/185)*box_height
                xx=5
            elif(int(box_widthpx)>700):
                ww=170
                hh=(ww/185)*box_height
                xx=15
            elif(int(box_widthpx)>600):
                ww=160
                hh=(ww/185)*box_height
                xx=25
            elif(int(box_widthpx)>500):
                ww=150
                hh=(ww/185)*box_height
                xx=35
            else:
                ww=140
                hh=(ww/185)*box_height
                xx=45

            # print("\n")
            # print(question)
            # print("y_var: ",y_var)
            # print("height: ",hh)
            # print("xx: ",xx)
            # print("\n")
            l=numpy.array(remaining_rows)
            if(int(hh)+int(y_var) >260):
                pdf.add_page()
                
            q_num+=1
            number=".("+str(q_num)+")"

            save_loc(pdf)
            #pdf.dashed_line(x_var,y_var+5,x_var+160,y_var+5, dash_length = 1, space_length = 1)
            #print(y_var)
            #print(box_height)
            
            
            save_loc(pdf)


            added_list.append([q_num,question[1],question[3]])
            
            #print(added_list)

            #print("rem: " ,[l[:,[0,5]]],end="\n")
            #print(number+" started to load")
            #print(question)
            try:
                ans_var=str(int(float(question[3])))
            except:
                ans_var=str(question[3])

            pdf.set_text_color(0,200,0)
            pdf.set_font_size(8)
            pdf.cell(w=15,h=5,txt="Answer: "+ans_var,ln=0,border='T',align='R',fill=False)
            pdf.set_text_color(0,0,0)
            x_var-=20
            set_loc(pdf)
            pdf.cell(w=194,h=10,txt=number,ln=1,border='T',align='R',fill=False)

            pdf.cell(w=194,h=hh-2.5,ln=1,border='B',align='R',fill=False)
            y_var=y_var+5
            set_loc(pdf)

            pdf.image(imglink,w=ww,x=pdf.get_x()+xx)
            

            #print(number+"loaded")
            #pdf.line(x_var,y_var+5,x_var+185,y_var+5)
            save_loc(pdf)
            y_var=y_var+2.5
            set_loc(pdf)
    

    return 

#Defining the basepath
basepath=os.path.dirname(__file__)

# ~1 Opening XLS file
""" loc = (basepath+"/input_file.xls")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0) """

# for row in range(sheet.nrows)[::-1]:

""" for row in range(sheet.nrows):
    number=int(row+1)
    name=sheet.cell_value(row, 0)
    link=sheet.cell_value(row, 1)
    link_name=link[link.rfind("/")+1::1]
    answer=sheet.cell_value(row, 2)
    if(answer!="*"):
        rows.append([number,name,link,answer,link_name,1])
remaining_rows=rows
 """
# numpy.random.shuffle(remaining_rows), print(remaining_rows)
# Extracting number of rows --> print(sheet.nrows)


# ~2 Or directly we open images from 'basepath/imgs/...'
filenames = list(next(walk(basepath+"/imgs"), (None, None, []))[2])  # [] if no file


for row in filenames:
    number=int(filenames.index(row)+1)
    #name=sheet.cell_value(row, 0)
    #link=sheet.cell_value(row, 1)
    file_extension=str(row)[-3::]
    if(file_extension=="png" or file_extension=="jpg"):
        link_name=row
        rows.append([number,"name","link","answer",link_name,1])
    #answer=sheet.cell_value(row, 2)
    # if(answer!="*"):
    #     rows.append([number,name,link,answer,link_name,1])
remaining_rows=rows

print(remaining_rows)


pdf = FPDF(orientation = 'P', unit = 'mm', format='A4')
pdf.accept_page_break()
pdf.add_page()
pdf.set_font('Arial', 'B', 12)

#print(remaining_rows)
q_num=0
added_list=[]
l=numpy.array(remaining_rows)

with alive_bar(20,enrich_print=True) as bar:
    pg=pdf.page_no()
    mainc(pdf)
    l=numpy.array(remaining_rows)
    for co in range(pdf.page_no()-pg):
        bar()
print("FINISHED")

#PDF output gets created
pdf.output(basepath+'/output_file.pdf', 'F')

#A list of the answers (for each image) is generated and gets printed
list_output(added_list)




