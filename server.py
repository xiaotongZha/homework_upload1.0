from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
app = Flask(__name__)

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'zip', '7z', 'tar','rar','docx','doc','png'}

task_record={}

@app.route('/page',methods=['GET'])
def page():
    task=request.args.get('task')
    if not task:
        return "<h1>FBI Warning<h1>"
    
    with open("student.info",'r', encoding="utf-8") as f:
        options=f.readlines()
    options=[_[:-1] for _ in options]
    with open(f"report/{task}/cnt.txt",'r', encoding="utf-8") as f:
        stu_list=f.readlines()
    with open(f"report/{task}/log.txt",'r', encoding="utf-8") as f:
        log_list=f.readlines()    
    tot_num=len(stu_list)
    return render_template('uploadPage.html',task_title=task_record[task],task=task,options=options,stu_list=stu_list,log_list=log_list,tot_num=tot_num)

@app.route('/upload',methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename == '':
        return "<h1>ERROR:请选择你的文件!<h1>"
    ext=file.filename.split(".")[-1]
    if ext not in ALLOWED_EXTENSIONS:
        return "<h1>ERROR:错误的文件后缀名!<h1>"
    stu=request.form['dropdown']
    if stu=='---请选择姓名学号---':
        return "<h1>ERROR:请选择学号姓名!<h1>"
    now_date = datetime.datetime.now()
    date_str = now_date.strftime("%Y-%m-%d %H:%M:%S")
    stu_info = stu.split('\t')
    task=request.form['taskType']
    if task[:2]=='os' and task[-3:]=='lab':
        parts = task.split('_')
        lab_number = int(parts[1])
        if parts[2]=="prelab":
            report_type="预习报告"
        if parts[2]=="lab":
            report_type="实验报告"
        filename=f"实验{lab_number}{report_type}_{stu_info[1]}_{stu_info[0]}.{ext}" #改这里
    else:
        filename=f"{stu_info[1]} {stu_info[0]}.{ext}"
    file.save(os.path.join(os.path.dirname(__file__),"report",task,'files',filename))

    with open(f"report/{task}/log.txt",'a',encoding='utf-8') as f: #改这里
        f.write(f"{date_str} {filename} 已保存\n")

    with open(f"report/{task}/cnt.txt",'r',encoding='utf-8') as f:
        exist_stus=f.readlines()

    if stu+'\n' not in exist_stus:
        with open(f"report/{task}/cnt.txt",'a',encoding='utf-8') as f:
            f.write(stu+'\n') 
    
    return redirect(url_for('page',task=task))        

@app.route('/')
def navigation():
    with open('task.info','r',encoding='utf-8') as f:
        task_list=f.readlines()
    task_list=[_.split(' ') for _ in task_list]
    
    for task in task_list:
        if task_record.get(task[0])==None:
            task_record.update({task[0]:task[1]})

    return render_template('index.html',task_list=task_list)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8823)
