from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

app = Flask(__name__)
Id="None"
status=False
print(Id,status)

@app.route('/')
def index():
    global Id
    global status
    return render_template('index.html',inputid=Id,inputstatus=status)

@app.route('/register', methods=['POST'])
def register():
    if request.method=='POST':
        register_info= request.form
        username=register_info['username']
        password=register_info['password']
        f=open('peoplelist.csv','a',newline='')
        mywriter=csv.writer(f)
        mywriter.writerow([username,password])
        f.close()
        
    return render_template('login1.html')

@app.route('/login1',methods=['GET','POST'])
def login1():
    global Id
    global status
    if request.method=='POST':
        login1_data=request.form
        _id=login1_data['username']
        _pw=login1_data['password']
        f=open('./peoplelist.csv','r')
        data=csv.reader(f)

        for i in data:
            if i[0]==_id and i[1]==_pw:

                Id=i[0] 

                status=True
                
                filelist=os.listdir('./user/'+Id)
                
                return render_template('memo.html',inputid=Id,inputstatus=status, filelist=filelist)
        if i[0]!=_id or i[1]!=_pw:
            status=False
            return render_template('index.html',inputid=Id,inputstatus=status)
    return render_template('login1.html', inputid=Id, inputstatus=status)  

@app.route('/logout',methods=['GET','POST'])
def logout():
    global Id
    global status
    if request.method=='POST':
        status=False
    return render_template('index.html',inputid=Id,inputstatus=status)

@app.route('/memo')
def memo():
    filelist=os.listdir('./user/'+Id)

    return render_template('memo.html',inputid=Id,inputstatus=status, filelist=filelist)

@app.route('/addfile',methods=['POST'])
def addfile():
    global Id
    if request.method=='POST':
        addfile_data= request.form
        filename=addfile_data['filename']
        dir_path='.\\user'
        dir_name=Id
        
        filelist=os.listdir('./user/'+Id)
        if os.path.isfile(dir_path+"\\"+dir_name+'\\'+filename+".txt")==False:
            f=open(dir_path+"\\"+dir_name+'\\'+filename+".txt","w")
            f.close()
            
            if os.path.isfile(dir_path+"\\"+dir_name+'\\'+filename+".txt")==True:
                f=open(dir_path+"\\"+dir_name+'\\'+filename+".txt","r", encoding='UTF8')
                content=f.readlines()
                f.close()
                return render_template('memocontent.html', title=filename, content=content)
            
    return render_template('memo.html',inputid=Id,inputstatus=status, filelist=filelist)

@app.route('/deletefile',methods=['POST'])
def deletefile():
    global Id
    if request.method=='POST':
        deletefile_data=request.form
        filename=deletefile_data['filename']
        dir_path='.\\user'
        dir_name=Id
        if os.path.isfile(dir_path+"\\"+dir_name+'\\'+filename+".txt")==True:
            os.remove(dir_path+"\\"+dir_name+'\\'+filename+".txt")
            filelist=os.listdir('./user/'+Id)
            return render_template('memo.html',inputid=Id,inputstatus=status, filelist=filelist)
    filelist=os.listdir('./user/'+Id)
    return render_template('memo.html',inputid=Id,inputstatus=status, filelist=filelist)

@app.route('/filelist',methods=['POST'])
def filelist():
    global Id
    if request.method=='POST':
        filelist_data=request.form
        filename=filelist_data['filename']
        dir_path='.\\user'
        dir_name = Id
        if os.path.isfile(dir_path+"\\"+dir_name+'\\'+filename)==True:
            f=open(filename+".txt","w")
    filelist=os.listdir('./user/'+Id)
    return render_template('memo.html',inputid=Id,inputstatus=status, filelist=filelist)

@app.route('/open/<filename>',methods=['POST'])
def openfile(filename):
    global Id
    if request.method=='POST':
        dir_path='.\\user\\'
        dir_name = Id
        if os.path.isfile(dir_path+dir_name+'\\'+filename+".txt")==True:
            f=open(dir_path+dir_name+'\\'+filename+".txt","r", encoding='UTF8')
            content=f.readlines()
            f.close()
    return render_template('memocontent.html', title=filename, content=content)

@app.route('/save/<title>',methods=['POST'])
def savefile(title):
    global Id
    if request.method=='POST':
        dir_path='.\\user\\'
        dir_name = Id
        content_html=request.form
        content=content_html['content']
        if os.path.isfile(dir_path+dir_name+'\\'+title+".txt")==True:
            f=open(dir_path+dir_name+'\\'+title+".txt","w", encoding='UTF8')
            f.write(content)
            
            f.close()
            
    filelist=os.listdir('./user/'+Id)
    return render_template('memo_copy.html',inputid=Id,inputstatus=status, filelist=filelist)

if __name__ == '__main__':
  app.run(debug=True)