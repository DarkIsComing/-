# from datetime import datetime

# print(datetime.now())
# print(datetime.utcnow())

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

Base = declarative_base()   #生成orm基类
engine = create_engine('mysql+pymysql://root:woaini123..@localhost:3306/practice',encoding='utf-8')
DBSession = sessionmaker(bind=engine)
session = DBSession()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(20), nullable=False)

class Addresss(Base):
    __tablename__ = 'addresss'
    id = Column(Integer, autoincrement=True, primary_key=True)
    email_address = Column(String(32), nullable=False)
    user_info = Column(Integer, ForeignKey('user.id'))

    user = relationship(User, backref='addresss')



for i in range(3):
    setattr(Addresss,'Col'+str(i),(Column('Col'+str(i), String(50),comment='Col'+str(i))))
Base.metadata.create_all(engine)

# 添加数据
dt=table_class(Col1='aaa',Col2="aaa")
session.add(dt)
session.commit()
# session.add_all([User(name='alex',),
#                  User(name='jack'),
#                  User(name='jim')])

# session.add_all([Addresss(email_address='11.com',user_info=1),
#                  Addresss(email_address='22.com',user_info=2)])


# user_obj = session.query(User).filter(User.name=='jack').first()
# print(user_obj.id, user_obj.name)
# print(user_obj)

# print('===============')
# print(user_obj.addresss)
# for i in user_obj.addresss:  #通过user对象反查关联的address记录
#     print(i)

# print('===============')
# address_obj = session.query(Addresss).filter(Addresss.email_address=='11.com').first()
# print(address_obj.user)      #在address对象里直接查关联的user记录
# session.commit()
# session.close()


{%if flag==2%}
					<td id="s" style="color:black">{{s}}</td>
					{%elif flag==1%}
					<td id="s" style="color:green">{{s}}</td>
					{%elif flag==0%}
					<td id="s" style="color:red">{{s}}</td>
					{%elif flag==-1%}
					<td id="s" style="color:orange">{{s}}</td>
					{%endif%}