from flask import render_template, flash, redirect, url_for, Request, request, session, jsonify
from . import main
from .forms import AddMaterialForm, BuyOrder, SaleOrder, InventoryForm, SearchOrder, RecordOrder, FileForm,AttachForm, ChangeForm, AttrForm, TableForm, NumForm, ChangeSumForm
from ..models import Material, Buy_Order, Sale_Order,  Stock_In, Stock_Out, InventoryFlow, Adjust, MaterialsInfo, MaterialDetail, MaterialType
from .. import db
import time
from datetime import datetime
from sqlalchemy import or_,and_
import json
from werkzeug import secure_filename
import os
import pandas as pd
import numpy as np
import re
#from manage import connection
from .utils import table_exists,connect_to_mysql

@main.route('/',methods=['GET','POST'])
def index():
    form=SearchOrder()
    if form.validate_on_submit():
        words=form.name.data
        return redirect(url_for('.search_material_list',words=words))
    return render_template('index.html',form=form)
        #words=form.name.data.strip().split()    #words列表
        #print(words,type(words))
        # word_dict={}
        # for i,s in enumerate(words):
        #     word_dict['words_{}'.format(i+1)] = s
        #print(word_dict.items())
        
        
#search列表
@main.route('/search', methods=['GET','POST'])
def search_material_list():
    if request.args.get('words'):
        words=request.args.get('words')
    else:
        words=request.args.get('words')
    words=words.strip().split()
    page = int(request.args.get('page') or 1)
    word={}
    for i,s in enumerate(words):
        word['words_{}'.format(i+1)] = s
    print('dict:',word)
    #print('参数长度：',len(words))
    if len(word)==1:
        page_data=Material.query.filter(or_(Material.物料名称.like("%" + word['words_1'] + "%")
                            )).paginate(page, 5, False)
    elif len(word)==2:
        page_data=Material.query.filter(or_(Material.物料名称.like("%" + word['words_1'] + "%"),
                            Material.物料名称.like("%" + word['words_2'] + "%")
                            )).paginate(page, 5, False)
    elif len(word)==3:
        page_data=Material.query.filter(or_(Material.物料名称.like("%" + word['words_1'] + "%"),
                            Material.物料名称.like("%" + word['words_2'] + "%"),
                            Material.物料名称.like("%" + word['words_3'] + "%")
                            )).paginate(page, 5, False)
    elif len(word)==4:
        page_data=Material.query.filter(or_(Material.物料名称.like("%" + word['words_1'] + "%"),
                            Material.物料名称.like("%" + word['words_2'] + "%"),
                            Material.物料名称.like("%" + word['words_3'] + "%"),
                            Material.物料名称.like("%" + word['words_4'] + "%"))
                            ).paginate(page, 5, False)
    else:
        flash('关键词过多,目前仅支持4个关键词以内搜索')
        return redirect(url_for('.index'))
    return render_template("search_materials_result.html",page_data=page_data,words=words)
    
 #检查      
@main.route('/check', methods=('GET', 'POST'))
def check():
    data=request.get_data(as_text=True)     #str
    print(data,type(data))      
    lists=data.split('&')
    yj=[]
    ids=[]
    boolean=[]
    for l in lists:
        if l.startswith('yj'):
            yj.append(l)
        if l.startswith('id'):
            ids.append(l)
    for i,item in enumerate(yj):
        yj[i]=yj[i][3:]
    for i,item in enumerate(ids):
        ids[i]=ids[i][3:]
    print('id',ids)
    print('yj',yj)
    for i,j in zip(yj,ids):
        query_info=Material.query.filter(and_(Material.物料名称==i,Material.物料型号==j)).first()
        if query_info is None:
            boolean.append(False)
        else:
            boolean.append(True)
    print(boolean)
    
    return jsonify({'data': boolean})

#上传文件
@main.route('/upload', methods=('GET', 'POST'))
def upload():
    
    form = AttachForm()
    if form.validate_on_submit():
        files= request.files['attach']
        filename = secure_filename(files.filename)
        files.save(os.path.join('/Users/zhaotengwei/Desktop/ERP/app/static',filename))
        j=[]
        with open(os.path.join('/Users/zhaotengwei/Desktop/ERP/app/static',filename),'rb') as f:        
            s=f.readlines()
            #print(s)
            for line in s:
                l=line.split()
                if len(l) == 6:
                #j.append({'横坐标':l[0],'纵坐标':l[1],'角度':l[2],'元件名':l[3],'封装':l[4]})
                    j.append({'贴装位':bytes.decode(l[0]),'横坐标':bytes.decode(l[1]),'纵坐标':bytes.decode(l[2]),'角度':bytes.decode(l[3]),'元件名':bytes.decode(l[4]),'封装':bytes.decode(l[5])})
                elif len(l) ==5:
                    j.append({'贴装位':bytes.decode(l[0]),'横坐标':bytes.decode(l[1]),'纵坐标':bytes.decode(l[2]),'角度':bytes.decode(l[3]),'元件名':bytes.decode(l[4]),'封装':''})
            #print(j)
            df=pd.DataFrame(j)
            print(df)
    
            new_df=df[['元件名','封装']]
            print('新df:',new_df,type(new_df))
            data_frame=new_df.groupby(['元件名','封装']).size()
            new_dataframe=data_frame.reset_index(name='counts')
            print(new_dataframe)
            yjm=new_dataframe['元件名'].values
            fz=new_dataframe['封装'].values
            count=new_dataframe['counts'].values
            print(yjm,fz,count)
            #series=df['封装'].value_counts()
            # print('分组：',series1)
            z=zip(yjm,fz,count)
            #z=zip(series.index,series.values) 
            #print('之前：',z,type(z)) 
            # print(series.index,series.values)     
            # print(type(series))   #<class 'pandas.core.series.Series'>
            f.close()
            # flash('Upload successfully!')
        return render_template('curd.html',form=form,filename=filename,z=z)
    return render_template('curd.html',form=form)
            

#保存
@main.route('/save',methods=['GET','POST'])
def save():
    #as_text=True 将原始数据格式bytes转换成Unicode了
    data=request.get_data(as_text=True)         #id=1206&id=FIDUCIAL_1MM&id=DIO4148-0805&id=SOT-23&id=SOT223&id=SSOP28DB&id=SOT323-5L&id=CRYSTAL-3.2-2.5&id=TQFP100&num=13&num=2&num=1&num=1&num=1&num=1&num=1&num=1&num=1 <class 'str'>
    print(data)
    lists=data.split('&')
    yj=[]
    ids=[]
    number=[]
    filename='noname'
    for l in lists:
        if l.startswith('yj'):
            yj.append(l)
        if l.startswith('id'):
            ids.append(l)
        if l.startswith('num'):
            number.append(l)
        if l.startswith('filename'):
            filename=l[9:].split('.')[0]
    for i,item in enumerate(yj):
        yj[i]=yj[i][3:]
    for i,item in enumerate(ids):
        ids[i]=ids[i][3:]
    for i,item in enumerate(number):
        number[i]=number[i][4:]
    # print('id',ids)
    # print('num',number)
    # print('file',filename)
    df=pd.DataFrame({"元件名":yj,"封装名称":ids,"数量":number})
    
    if filename !='noname' and filename !='':
        df.to_csv("/Users/zhaotengwei/Desktop/ERP/app/static/csv/"+filename+".csv",index=False,sep=',')
        return jsonify({'data': 'success'})
    #     return redirect(url_for('.csv'))
    # else:
    #     flash('未保存成功，文件可能不存在')
    # return redirect(url_for('csv'))
    return jsonify({'data': 'fail'})
    
    #print(ids)      #['1206', 'FIDUCIAL_1MM', 'DIO4148-0805', 'SOT-23', 'SOT223', 'SSOP28DB', 'SOT323-5L', 'CRYSTAL-3.2-2.5', 'TQFP100']
    #print(number)       #['13', '2', '1', '1', '1', '1', '1', '1', '1']
    # delete_query=MaterialsInfo.query.filter(MaterialsInfo.封装名称 not in ids).all()   
    # if delete_query:
    #     for item in delete_query:
    #         #print(item)
    #         db.session.delete(item)
    # for i,j in zip(ids,number):
    #     fengzhuang=MaterialsInfo()
    #     fengzhuang.封装名称=i
    #     fengzhuang.封装数量=j
    #     query_info=MaterialsInfo.query.filter(MaterialsInfo.封装名称==i).first()
        
    #     if query_info:
    #         query_info.封装数量=j
    #     else:          
    #         db.session.add(fengzhuang)
    
    # try:
    #     db.session.commit()
    # except:
    #     db.session.rollback()
    #     flash('新的记录添加失败。')
    # flash('新的记录添加成功。')

@main.route('/AdjustInventory',methods=['GET','POST'])
def adjust_inventory():
    
    s=int(request.args.get('s'))
    path=request.args.get('path')       #保存的csv路径
    name=request.args.get('name')       #打开的csv的文件名称
    single_yj=request.args.get('yj')
    single_fz=request.args.get('fz')
    query_info=Material.query.filter(and_(Material.物料名称==single_yj,Material.物料型号==single_fz)).first()
    if query_info:
        if query_info.物料库存 >=s:
            flag=1          #正常
            query_info.物料库存=int(query_info.物料库存)-s

        else:
            flag=0          #
            query_info.物料库存=int(query_info.物料库存)-s
            flash('入库成功,但是库存已经为负')

    #库存流水表
        inventory_flow=InventoryFlow()
        inventory_flow.物料名称=single_yj
        inventory_flow.物料ID= query_info.ID
        inventory_flow.日期= datetime.now()
        inventory_flow.类型='product'
        inventory_flow.发生数量=-s
        inventory_flow.库存数量=query_info.物料库存
        db.session.add(inventory_flow)
        try:
            db.session.commit()
            flash('修改库存成功')
        except:
            db.session.rollback()
            flash('修改库存失败')
    else:
        flag=-1             #
        flash('该物料不存在')
    return redirect(url_for('.opencsv',flag=flag,single_yj=single_yj,single_fz=single_fz,name=name,path=path))


@main.route('/changeSum',methods=['GET','POST'])
def change_sum():  
    form=ChangeSumForm()
    path=request.args.get('path')       #保存的csv路径
    name=request.args.get('name')       #打开的csv的文件名称
    source_file=path+'/'+name           #资源路径
    yj=request.args.get('yj')
    fz=request.args.get('fz')
    # print(yj,fz)
    # print(type(yj),type(fz))
    df=pd.read_csv(source_file)
    
    #print('总数：',data.values,type(data.values))
    if form.validate_on_submit():
        num=int(form.num.data)
        #print(num,type(num))
        # print('元件名a',df['元件名'])
        # print('封装名称b',df['封装名称'])
        # print('匹配项',df.loc[(df['元件名']==yj)&(df['封装名称']==fz)])
        if not df.loc[(df['元件名']==yj)&(df['封装名称']==fz),'总数'].empty:
            df.loc[(df['元件名']==yj)&(df['封装名称']==fz),'总数']+=num
            df.to_csv(source_file,index=False,sep=',')
            flash('修改成功')
        else:
            flash('修改失败')
        return redirect(url_for('.opencsv',name=name,path=path))
    return render_template('change_sum.html',form=form)


@main.route('/opencsv',methods=['GET','POST'])          #待解决。
def opencsv():
    # single_fz=None
    # single_yj=None
    # if request.args.get('single_yj'):
    #     single_yj=request.args.get('single_yj')
    # if request.args.get('single_fz'):
    #     single_fz=request.args.get('single_fz')
    path=request.args.get('path')       #保存的csv路径
    name=request.args.get('name')       #打开的csv的文件名称
    source_file=path+'/'+name           #资源路径
    df=pd.read_csv(source_file)
    yj=df['元件名'].values          #<class 'numpy.ndarray'>
    fz=df['封装名称'].values        #<class 'numpy.ndarray'>
    num=df['数量'].values           #<class 'numpy.ndarray'>
    if '总数' not in df.columns:
        df['总数']=0    
        df.to_csv(source_file,index=False,sep=',')  
    #print('前:',df['总数'])
    sum_number=df['总数'].values
    #print('之前的sum:',sum_number)
    form=NumForm()
    if form.validate_on_submit():
        df['总数']=0
        block_num=form.num.data 
        df['总数']=df['数量'].map(lambda x:x*int(block_num))
        df.to_csv(source_file,index=False,sep=',')
        #print('计算后：',df['总数'])
        sum_number=df['总数'].values
        #print('之后的sum:',sum_number)
    # print('索引：',df.loc[])
    z=zip(yj,fz,num,sum_number)
    # if single_fz and single_yj:
    #     return render_template('opencsv.html',z=z,flag=flag,single_yj=single_yj,single_fz=single_fz,form=form,name=name,path=path)
    # else:
    return render_template('opencsv.html',z=z,form=form,name=name,path=path)
        

# 获取数据yj
@main.route('/data_yj',methods=['GET','POST'])
def get_yj():
    results=[]
    search=request.args.get('q_yj')
    query=Material.query.filter(Material.物料名称.like('%'+str(search)+'%')).all()
    for item in query:
        results.append(item.物料名称)
    print(results,type(results))
    return jsonify(result=results)

# 获取数据fz
@main.route('/data_fz',methods=['GET','POST'])
def get_fz():
    results=[]
    search=request.args.get('q_fz')
    query=Material.query.filter(Material.物料型号.like('%'+str(search)+'%')).all()
    for item in query:
        results.append(item.物料型号)
    print(results,type(results))
    return jsonify(result=results)

        
    
    
@main.route('/t3', methods=['GET'])
def autocomplete():
    return render_template('test3.html')

@main.route('/t4', methods=['GET'])
def t4():
    return render_template('test4.html')

@main.route('/t5', methods=['GET'])
def t5():
    return render_template('test5.html')

# 显示csv
@main.route('/csv',methods=['GET','POST'])
def csv():
    # ids=request.args.getlist("ids")
    # number=request.args.getlist('number')
    # filename=request.args.get('filename')
    # page = int(request.args.get('page') or 1)
    # page_data=MaterialsInfo.query.paginate(page, 50, False)
    # df=pd.DataFrame({"封装名称":ids,"数量":number})
    # if filename:
    #     df.to_csv("/Users/zhaotengwei/Desktop/ERP/app/static/csv/"+filename+".csv",index=False,sep=',')
    # else:
    #     flash('未保存成功，文件可能不存在')
    # print('ids',ids)
    # print('number',number)
    path = "/Users/zhaotengwei/Desktop/ERP/app/static/csv" #文件夹目录
    files= os.listdir(path) #得到文件夹下的所有文件名称
    form=SearchOrder()
    if form.validate_on_submit():
        words=form.name.data
        
        suggestions = []
        pattern = '.*'.join(words) # Converts 'djm' to 'd.*j.*m'
        regex = re.compile(pattern)     # Compiles a regex.
        
        for item in files:
            match = regex.search(item.split('.')[0])  # Checks if the current item matches the regex.
            if match:
                suggestions.append(item)
        #print(suggestions)
        return render_template("csv.html",suggestions=suggestions,form=form,path=path)
    return render_template("csv.html",files=files,path=path,form=form)




#添加物料属性表
@main.route('/addMaterialAttribute',methods=['GET','POST'])
def add_material_attribute():
    form= TableForm()
    con=connect_to_mysql()
    if form.validate_on_submit():
        name=form.name.data
        cursor=con.cursor()
        if table_exists(cursor,name) is False:
            try:                           
                cursor.execute("create table %s (ID integer AUTO_INCREMENT,物料ID integer,primary key(ID),FOREIGN KEY (物料ID) REFERENCES materials(ID))"%name)     
                flash('表格添加成功')         
            except:
                flash('表格添加失败')
        cursor.execute("SELECT name FROM type WHERE name='%s'"%name)
        attr=cursor.fetchone()
        print('属性内容：',attr)
        if attr is None:
            try:
                cursor.execute("INSERT INTO type (name) VALUES ('%s')"%name)       
                flash('表格记录添加成功')  
            except:
                flash('表格记录添加失败')  
        else:
            flash('该类型已经存在！')
        con.commit()
        cursor.close()
        con.close()
        return redirect(url_for('.add_material'))
    return render_template("add_table.html",form=form)



#添加物料
@main.route('/addMaterials',methods=['GET','POST'])
def add_material():
    
    form=AddMaterialForm()
    results = MaterialType.query.all()
    names=[]
    for result in results:
        names.append(result.name)
    #print(names)
    
    form.material_type.choices += [(name,name) for name in names]
    if form.validate_on_submit():
        old_material=Material.query.filter(and_(Material.物料名称==form.material_name.data,Material.物料型号==form.material_number.data)).first()
        if old_material:
            flash('该物料已经存在,请重新添加')
            return redirect(url_for('.add_material'))

        material=Material()
        #material.ID=form.material_ID.data
        material.物料名称=form.material_name.data
        material.物料型号=form.material_number.data
        material.物料类型=form.material_type.data
        db.session.add(material)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('新的物料添加失败。')
        flash('新的物料添加成功。')
        return redirect(url_for('.material_list'))
    return render_template("add_material.html",form=form)

#物料属性展示
@main.route('/showAttr',methods=['GET','POST'])
def show_attr():
    ID=request.values.get('ID')
    name=request.args.get('name')
    fz=request.args.get('fz')
    mtype=request.values.get('mtype')
    con=connect_to_mysql()
    cursor=con.cursor()
    if table_exists(cursor,mtype) is True:
        cursor.execute("select * from %s where 物料ID=%s"%(mtype,ID))
        col1=cursor.description
        data_dict=[]                #这张表中所有的列名组成的列表
        for field in col1:
            if field[0] !='ID':
                data_dict.append(field[0])
        print(data_dict)
        value_dict=[]
        val=cursor.fetchone()   #元组    
        print(val)              
        if val:
            value=list(val[1:])
        else:
            value=None
        con.commit()
        cursor.close()
        con.close()
        return render_template('show_attr.html',data_dict=data_dict,value=value,fz=fz,name=name,ID=ID,mtype=mtype)
    else:
        con.commit()
        cursor.close()
        con.close()
        flash('表格不存在,请先添加表')
    return render_template('show_attr.html',fz=fz,name=name,ID=ID,mtype=mtype)



#添加物料属性
@main.route('/detail',methods=['GET','POST'])
def material_detail():
    form =AttrForm()
    ID=request.values.get('ID')
    name=request.args.get('name')
    fz=request.args.get('fz')
    mtype=request.values.get('mtype')
    print(ID)
    print(mtype)
    con=connect_to_mysql()
    cursor=con.cursor()
    if table_exists(cursor,mtype) is True:         #如果该类型表存在
        if form.validate_on_submit():       #提交添加属性表单数据      
            attribute=form.name.data        #获取表单中的属性名称   str
            value=form.value.data           #获取属性值  
            cursor.execute("SELECT 物料ID FROM %s WHERE 物料ID=%s"%(mtype,ID))         #查询属性表中该物料ID对应的记录
            query_info=cursor.fetchone()
            cursor.execute("select * from %s where 物料ID=%s"%(mtype,ID))
            col=cursor.description
            data_dict=[]
            for field in col:
                data_dict.append(field[0])        #该表列名集合
            if query_info is None:                  #如果该记录不存在
                #add_query="ALTER TABLE material_detail ADD %s INTEGER"  
                if attribute not in data_dict:
                    cursor.execute("ALTER TABLE %s ADD %s varchar(10)"%(mtype,attribute))         
                cursor.execute("INSERT INTO %s (物料ID,%s) VALUES (%s,%s)"%(mtype,attribute,ID,value))               
                flash('添加成功')
            else:                   #如果有和该物料ID匹配的一条数据存在
                if attribute in data_dict:
                    cursor.execute("UPDATE %s set %s=%s,物料ID=%s where 物料ID=%s"%(mtype,attribute,value,ID,ID))                   
                    flash('更新成功')
                else:
                    cursor.execute("ALTER TABLE %s ADD %s varchar(10)"%(mtype,attribute))          
                    cursor.execute("UPDATE %s set %s=%s,物料ID=%s where 物料ID=%s"%(mtype,attribute,value,ID,ID))                                 
                    flash('添加成功')
            con.commit()
            cursor.close()
            con.close()
            return redirect(url_for('.show_attr',fz=fz,name=name,ID=ID,mtype=mtype))
    else:
        flash('该表不存在,请先创建表')
        return redirect(url_for('.add_material_attribute'))
    #return redirect(url_for('.add_material_attribute',ID=ID,mtype=mtype,name=name,fz=fz))
    return render_template('material_detail.html',form=form)


#物料列表
@main.route('/materialList', methods=['GET','POST'])
def material_list():
    page = int(request.args.get('page') or 1)
    page_data=Material.query.paginate(page, 5, False)
    return render_template("material_list.html",page_data=page_data)

#删除物料
@main.route('/del',methods=['GET','POST'])
def delete_material():
    ids=request.args.get('ID')
    del_material=Material.query.filter(Material.ID==ids).first()  
    db.session.delete(del_material)
    db.session.commit()
    flash('删除成功')
    
    return redirect(url_for('.material_list'))


#出货单列表
@main.route('/saleList', methods=['GET','POST'])
def sale_list():
    page = int(request.args.get('page') or 1)
    page_data=Sale_Order.query.paginate(page, 5, False)
    if page_data is None:
        flash('出货表为空')
    return render_template("show_sale_order.html",page_data=page_data)

#进货单列表
@main.route('/buyList', methods=['GET','POST'])
def buy_list():
    page = int(request.args.get('page') or 1)
    page_data=Buy_Order.query.paginate(page, 5, False)
    if page_data is None:
        flash('进货表为空')
    return render_template("show_buy_order.html",page_data=page_data)
    
# #单项进货
# @main.route('/singlebuy',methods=['GET','POST'])
# def single_buy():
#     ids=request.args.get('ID')
#     material=Material.query.filter(Material.ID==ids).first()
#     ids=request.args.get('material.ID')
#     print(ids)
#     return 'ggg'


#进货表
@main.route('/buy',methods=['GET','POST'])
def buy():
    ids=request.args.get('ID')
    query_info=Material.query.filter(Material.ID==ids).first()
    form= BuyOrder()
    if form.validate_on_submit():
        # old_order=Buy_Order.query.filter_by(进货id=form.进货ID.data).first()
        # if old_order:
        #     flash('该进货单编号已存在')
        new_order= Buy_Order()
        new_order.物料ID= query_info.ID
        new_order.物料名称= query_info.物料名称
        new_order.进货数量= form.进货数量.data
        new_order.进货价格= form.进货价格.data
        new_order.进货日期= datetime.now()
        # query_info=Material.query.filter(Material.物料名称== form.物料名称.data).first()
        # if query_info:
        #     new_order.物料ID= query_info.ID
        # else:
        #     new_order.物料ID= None
        #入库表
        new_stock_in_model=Stock_In()
        new_stock_in_model.入库数量=new_order.进货数量
        new_stock_in_model.入库价格=new_order.进货价格
        new_stock_in_model.入库日期=new_order.进货日期
        new_stock_in_model.物料名称=new_order.物料名称
        new_stock_in_model.物料ID=new_order.物料ID

        
        
        new_material_model=Material()
        inventory_query_info= Material.query.filter_by(ID= ids).first()  #查询库存表中属性物料ID等于进货单中进货的物料的物料ID的第一条数据。
        if inventory_query_info:        #如果该条数据存在
            material_inventory_num= inventory_query_info.物料库存        #物料库存数量=查询所得到的库存数量
            if material_inventory_num is None:      #如果该物料库存数量为空，则赋值为0
                material_inventory_num=0            
            material_inventory_num+= int(new_order.进货数量)      #该物料库存数量加上新的进货单的进货数量
            inventory_query_info.物料库存=material_inventory_num    #更新库存表中该物料的库存数量
        else:                       #如果库存表中没有该物料ID对应的库存数据
            material_inventory_num=0            
            #print(new_order.进货数量,type(new_order.进货数量))
            material_inventory_num+= int(new_order.进货数量)
            new_material_model.库存数量=material_inventory_num
            db.session.add(new_material_model)

        #库存流水表
        inventory_flow=InventoryFlow()
        inventory_flow.物料名称=new_order.物料名称
        inventory_flow.物料ID= new_order.物料ID
        inventory_flow.价格= new_order.进货价格
        inventory_flow.日期= new_order.进货日期
        inventory_flow.类型='in'
        inventory_flow.发生数量=(+int(new_order.进货数量))
        inventory_flow.库存数量=material_inventory_num

        db.session.add(new_order)
        db.session.add(new_stock_in_model)
        db.session.add(inventory_flow)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('新的购货记录添加失败。')
        flash('新的购货记录添加成功。')
        return redirect(url_for('.buy_list'))

    return render_template('buy_order.html',form=form)


# #进货单显示
# @main.route('/buyOrder/<int:ID>',methods=['GET'])
# def show_buy_order(ID):
#     buy_order = Buy_Order.query.filter_by(进货id=ID).first()
#     if buy_order is None:
#         return '该进货表不存在'
#         flash('该进货表不存在')
    
#     return render_template('show_buy_order.html', buy_order=buy_order)


#出货表
@main.route('/sale',methods=["GET",'POST'])
def sale():
    ids=request.args.get('ID')
    query_info=Material.query.filter(Material.ID==ids).first()
    form=SaleOrder()
    if form.validate_on_submit():
        new_order=Sale_Order()
        new_order.物料ID= query_info.ID
        new_order.出货数量=form.出货数量.data
        new_order.出货价格=form.出货价格.data
        new_order.出货日期=datetime.now()
        new_order.物料名称=query_info.物料名称
        # query_info=Material.query.filter(Material.物料名称==form.出货物料名称.data).first()         #filter是==
        # if query_info:
        #     new_order.物料ID=query_info.ID
        # else:
        #     new_order.物料ID=None

        #出库表
        new_stock_out_model=Stock_Out()
        new_stock_out_model.出库数量=new_order.出货数量
        new_stock_out_model.出库价格=new_order.出货价格
        new_stock_out_model.出库日期=new_order.出货日期
        new_stock_out_model.物料名称=new_order.物料名称
        new_stock_out_model.物料ID=new_order.物料ID

        inventory_query_info= Material.query.filter_by(ID= new_order.物料ID).first()  #查询库存表中属性物料ID等于出货单中进货的物料的物料ID的第一条数据。
        if inventory_query_info:
            if inventory_query_info.物料库存 is None or inventory_query_info.物料库存 < int(new_order.出货数量):
                flash('出货失败，该物料没有库存或者库存数量小于出货数量')
                return redirect(url_for('.sale'))
            else:
                inventory_query_info.物料库存-=int(new_order.出货数量)
                
        else:
            flash('出货失败，库存中没有该物料')
            return redirect(url_for('main.sale'))

        #库存流水表
        inventory_flow=InventoryFlow()
        inventory_flow.物料名称=new_order.物料名称
        inventory_flow.物料ID= new_order.物料ID
        inventory_flow.价格= new_order.出货价格
        inventory_flow.日期= new_order.出货日期
        inventory_flow.类型='out'
        inventory_flow.发生数量=(-int(new_order.出货数量))
        inventory_flow.库存数量=inventory_query_info.物料库存

        db.session.add(inventory_flow)
        db.session.add(new_order)
        db.session.add(new_stock_out_model)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('新的出货记录添加失败。')
        flash('新的出货记录添加成功。')

        return redirect(url_for('main.sale_list'))
    return render_template('sale_order.html', form=form)


#生产损耗记录表
@main.route('/record',methods=['GET','POST'])
def production_record():
    form=RecordOrder()
    ids=request.args.get('ID')
    name=request.args.get('name')
    
    if form.validate_on_submit():
        inventory=Material.query.filter(Material.ID==ids).first()
        data=form.record.data           #输入的物料数量
        inventory_flow=InventoryFlow()
        #adjust=Adjust()
        inventory_flow.物料ID=ids
        inventory_flow.物料名称=name
        inventory_flow.类型='adjust'
        inventory_flow.日期=datetime.now()
        inventory_flow.发生数量=(-int(data))
        inventory_flow.库存数量=inventory.物料库存-int(data)
        inventory.物料库存=inventory_flow.库存数量
        db.session.add(inventory_flow)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('新的调整记录添加失败。')
        flash('新的调整记录添加成功。')
        return redirect(url_for('.material_list'))
    return render_template('loss.html',form= form)



# #出货单显示
# @main.route('/saleOrder/<int:ID>',methods=['GET'])
# def show_sale_order(ID):
#     sale_order = Sale_Order.query.filter_by(出货id=ID).first()
#     if sale_order is None:
#         return '该出货表不存在'
#         flash('该出货表不存在')
    
#     return render_template('show_sale_order.html', sale_order=sale_order)






# #显示库存信息
# @main.route('/Inventory/<int:ID>', methods=['GET'])
# def show_inventory(ID):
#     new_inventory=Inventory.query.filter_by(物料ID=ID).first()
#     if new_inventory is None:
#         return '该库存信息不存在'
#         flash('该库存信息不存在')
    
#     return render_template('show_inventory.html', new_inventory=new_inventory)

#库存流水
@main.route('/inventoryFlow', methods=['GET','POST'])
def inventory_flow():
    page = int(request.args.get('page') or 1)
    page_data=InventoryFlow.query.paginate(page, 5, False)
    #     page_data=InventoryFlow.query.filter(InventoryFlow.物料名称.like("%"+words+"%")).paginate(page, 5, False)
    #     print(page_data,type(page_data))
    #     return render_template("inventory_flow.html",page_data=page_data,form=form)
    return render_template("inventory_flow.html",page_data=page_data)


#库存流水搜索
@main.route('/searchInventoryFlow', methods=['GET','POST'])
def search_inventory_flow():
    form= SearchOrder()
    if form.validate_on_submit():
        words=form.name.data
        return redirect(url_for('.search_result',words=words))
    
    return render_template('search_flow.html',form=form)


#流水搜索结果
@main.route('/searchResult', methods=['GET','POST'])
def search_result():
    if request.args.get('words'):
        words=request.args.get('words')
    else:
        words=request.args.get('words')
    words=words.strip().split()
    page = int(request.args.get('page') or 1)
    
    word={}
    for i,s in enumerate(words):
        word['words_{}'.format(i+1)] = s
    print('dict:',word)
    if len(word)==1:
        page_data=InventoryFlow.query.filter(or_(InventoryFlow.物料名称.like("%" + word['words_1'] + "%")
                        )).paginate(page, 5, False)
    elif len(word)==2:
        page_data=InventoryFlow.query.filter(or_(InventoryFlow.物料名称.like("%" + word['words_1'] + "%"),
                            InventoryFlow.物料名称.like("%" + word['words_2'] + "%")
                            )).paginate(page, 5, False)
    elif len(word)==3:
        page_data=InventoryFlow.query.filter(or_(InventoryFlow.物料名称.like("%" + word['words_1'] + "%"),
                            InventoryFlow.物料名称.like("%" + word['words_2'] + "%"),
                            InventoryFlow.物料名称.like("%" + word['words_3'] + "%")
                            )).paginate(page, 5, False)
    elif len(word)==4:
        page_data=InventoryFlow.query.filter(or_(InventoryFlow.物料名称.like("%" + word['words_1'] + "%"),
                            InventoryFlow.物料名称.like("%" + word['words_2'] + "%"),
                            InventoryFlow.物料名称.like("%" + word['words_3'] + "%"),
                            InventoryFlow.物料名称.like("%" + word['words_4'] + "%"))
                            ).paginate(page, 5, False)
    else:
        flash('关键词过多,目前仅支持4个关键词以内搜索')
        return redirect(url_for('.search_inventory_flow'))
    
    return render_template("search_result.html",page_data=page_data,words=words)



def is_zero(ids):
    innum=0
    outnum=0
    stock_in_list=Stock_In.query.filter(Stock_In.物料ID==ids).all()
    stock_out_list=Stock_In.query.filter(Stock_In.物料ID==ids).all()
    if stock_in_list and stock_out_list:
        for item in stock_in_list:
            if item.入库数量:
                innum+=int(item.入库数量)
            else:
                continue
        for item in stock_out_list:
            if item.出库数量:
                outnum+=int(item.出库数量)
            else:
                continue
        num=innum-outnum
        if num==0:
            return True
        else:
            return num
    else:
        return False



#盘库
@main.route('/consolidate',methods=['GET','POST'])
def consolidate():
    pass
            