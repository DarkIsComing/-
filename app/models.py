from . import db
from datetime import datetime
from sqlalchemy import ForeignKey 

class MaterialType(db.Model):
    __tablename__='type'
    ID=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64))  
#物料表
class Material(db.Model):
    __tablename__='materials'       
    ID=db.Column(db.Integer,primary_key=True)       #物料内部ID
    物料名称=db.Column(db.String(64),nullable=False)                          #物料名称
    物料型号=db.Column(db.String(64))                     #物料型号
    物料类型=db.Column(db.String(64))                          #物料类型
    物料库存=db.Column(db.Integer)                            #物料库存
    备注=db.Column(db.String(64))                              #备注
    stockin_info = db.relationship('Stock_In',backref="materials")
    stockout_info = db.relationship('Stock_Out',backref="materials")
    buy_order = db.relationship('Buy_Order',backref="materials")
    sale_order = db.relationship('Sale_Order',backref="materials")
    # package_type=db.Column(db.String(64))                           #包装类型

#物料详情表
class MaterialDetail(db.Model):
    __tablename__='material_detail'
    编号=db.Column(db.Integer,primary_key=True)
    物料ID=db.Column(db.Integer,db.ForeignKey('materials.ID'),nullable=False,unique=True)

    

# #库存信息表
# class Inventory(db.Model):
#     __tablename__='inventory'
#     库存编号=db.Column(db.Integer,primary_key=True)
#     类型=db.Column(db.Enum('in','out','adjust'))
#     #发生数量=db.Column(db.Integer)
#     库存数量=db.Column(db.Integer)
    
#     物料名称=db.Column(db.String(64))
#     物料ID=db.Column(db.Integer,db.ForeignKey('materials.ID'),nullable=False)

#入库表 
class  Stock_In(db.Model):
    __tablename__='stock_in'
    入库单id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    入库数量=db.Column(db.Integer,nullable=False)
    入库价格=db.Column(db.Float,nullable=False)
    入库日期=db.Column(db.DateTime(),default=datetime.now)
    
    物料名称=db.Column(db.String(64))
    物料ID=db.Column(db.Integer,db.ForeignKey('materials.ID'))

#出库单 
class  Stock_Out(db.Model):
    __tablename__='stock_out'
    出库单id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    出库数量=db.Column(db.Integer,nullable=False)
    出库价格=db.Column(db.Float,nullable=False)
    出库日期=db.Column(db.DateTime(),default=datetime.now)
    物料名称=db.Column(db.String(64))
    物料ID=db.Column(db.Integer,db.ForeignKey('materials.ID'))




#进货表
class Buy_Order(db.Model):
    __tablename__="buy_order"
    进货id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    进货数量=db.Column(db.Integer,nullable=False)
    进货价格=db.Column(db.Float,nullable=False)
    进货日期=db.Column(db.DateTime(),default=datetime.now)
    物料名称=db.Column(db.String(64))
    物料ID=db.Column(db.Integer,db.ForeignKey('materials.ID'))

    物料 = db.relationship('Material',backref="buy_order_of_material")

#出货表
class Sale_Order(db.Model):
    __tablename__="sale_order"
    出货id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    出货数量=db.Column(db.Integer,nullable=False)
    出货价格=db.Column(db.Float,nullable=False)
    出货日期=db.Column(db.DateTime(),default=datetime.now)
    物料名称=db.Column(db.String(64))
    物料ID=db.Column(db.Integer,db.ForeignKey('materials.ID'))

    物料 = db.relationship('Material',backref="sale_order_of_material")

#库存流水表 
class  InventoryFlow(db.Model):
    __tablename__='inventory_flow'
    ID=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    #价格=db.Column(db.Float,nullable=False)
    日期=db.Column(db.DateTime(),default=datetime.now)
    类型=db.Column(db.String(32))
    发生数量=db.Column(db.Integer,nullable=False)
    库存数量=db.Column(db.Integer,nullable=False)
    物料名称=db.Column(db.String(64))
    物料ID=db.Column(db.Integer,db.ForeignKey('materials.ID'))

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


#调整信息表
class Adjust(db.Model):
    __tablename__='adjust'
    ID=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    物料ID=db.Column(db.Integer,db.ForeignKey('materials.ID'))
    物料名称=db.Column(db.String(64))
    调整日期=db.Column(db.DateTime(),default=datetime.now)
    调整数据=db.Column(db.Integer)



#物料生产信息表
class MaterialsInfo(db.Model):
    __tablename__='materials_product_info'       
    ID=db.Column(db.Integer,primary_key=True)       #编号
    封装名称=db.Column(db.String(64),nullable=False)             #封装名称                          #物料类型
    封装数量=db.Column(db.String(64))                            #封装数量
    倍率=db.Column(db.String(64)) 
    生产数量=db.Column(db.String(64)) 


# #供应商
# class Supplier(db.Model):
#     __tablename__='supplier'        
#     supplier_id=db.Column(db.Integer,primary_key=True)   #供应商ID
#     material_id           
#     supplier_name=db.Column(db.String(64))                          #供应商名字
#     package_type=db.Column(db.String(64))                           #包装类型

#电rong表
# class Resistance(db.Model):
#     __tablename__='resistance'  
#     encapsulation_type=db.Column(db.String(64))                     #封装类型 0603
#     material_id     
#     resistance_type=db.Column(db.String(64),primary_key=True)                          #电阻类型
    

'''
#二极管
class Diode(db.Model):
    __tablename__='diode'   
    material_id    
    encapsulation_type=db.Column(db.String(64))                     #封装类型
    diode_type=db.Column(db.String(64),primary_key=True)       #二极管类型
'''


