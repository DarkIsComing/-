from app import create_app, db
from flask_script import Shell, Manager
from flask_migrate import MigrateCommand, Migrate
import pymysql  
from app.models import Material, Stock_In, Stock_Out, Buy_Order, Sale_Order
app=create_app()
manager=Manager(app)
migrate = Migrate(app, db)
def make_shell_context():
    return dict(db= db, Material= Material, Stock_In= Stock_In, Stock_Out= Stock_Out, 
    Buy_Order=Buy_Order, Sale_Order=Sale_Order)
manager.add_command('db',MigrateCommand)
manager.add_command('shell',Shell(make_context= make_shell_context))









if __name__=='__main__':
    app.run(debug=True)
    manager.run()