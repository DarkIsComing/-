from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField,FloatField, DateTimeField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileRequired , FileAllowed

class AttrForm(FlaskForm):
    name=StringField('属性',validators=[DataRequired()])
    value=StringField('值',validators=[DataRequired()])
    submit=SubmitField('添加')

class NumForm(FlaskForm):
    num=StringField('请输入要生产的块数:',validators=[DataRequired()])
    submit=SubmitField('提交')

class ChangeSumForm(FlaskForm):
    num=StringField('请输入要修改的数量:',validators=[DataRequired()])
    submit=SubmitField('提交')


class TableForm(FlaskForm):
    name=StringField('物料属性表',validators=[DataRequired()])
    submit=SubmitField('添加表')

class AddMaterialForm(FlaskForm):
    #material_ID=StringField('物料ID',validators=[DataRequired()])
    material_name=StringField('物料名称',validators=[DataRequired()])
    material_number=StringField('物料型号',validators=[DataRequired()])
    #material_type=SelectField('物料类型',choices=[('电阻','电阻'),('二极管','二极管')],coerce=str)
    material_type=SelectField('物料类型',choices=[('','')],coerce=str)
    submit=SubmitField('提交')
    
class SearchOrder(FlaskForm):
    name=StringField('请输入要搜索的名称',validators=[DataRequired()],render_kw={'placeholder':u'输入名称'})
    submit=SubmitField('搜索')

class FileForm(FlaskForm):
    files=FileField('文件名:',validators=[FileRequired()])
    submit=SubmitField('提交')

class AttachForm(FlaskForm):
    attach = FileField('请上传你需要的文件:', validators=[
        FileRequired(),
        # FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit=SubmitField('提交')

class RecordOrder(FlaskForm):
    record=StringField('请输入损耗掉的物料数量',validators=[DataRequired()],render_kw={'placeholder':u'输入损耗掉的物料数量'})
    submit=SubmitField('提交')

class BuyOrder(FlaskForm):
    #进货ID=StringField('进货编号',validators=[DataRequired()])
    #物料名称=StringField('进货物料名称',validators=[DataRequired()])
    进货数量=StringField('进货数量',validators=[DataRequired()])
    进货价格=StringField('进货价格',validators=[DataRequired()])
    #进货日期=DateTimeField('进货日期')
    submit=SubmitField('提交')


class SaleOrder(FlaskForm):
    #出货ID=StringField('出货编号',validators=[DataRequired()])
    #出货物料名称=StringField('出货物料名称',validators=[DataRequired()])
    出货数量=StringField('出货数量',validators=[DataRequired()])
    出货价格=StringField('出货价格',validators=[DataRequired()])
    #入库时间=StringField('入库时间',validators=[DataRequired()])
    submit=SubmitField('提交')


class InventoryForm(FlaskForm):
    inventory=StringField('请输入要查询库存信息的物料ID:')
    submit=SubmitField('提交')






#增删查改


#改
class ChangeForm(FlaskForm):
    number=StringField('请输入要修改的数量:')
    submit=SubmitField('提交')