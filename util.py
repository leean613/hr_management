from sqlalchemy.engine import create_engine



def connect_server():
    #Server Info
    DIALECT = 'oracle'
    SQL_DRIVER = 'cx_oracle'
    USERNAME = 'DEV' #enter your username
    PASSWORD = 'qtdata@2021' #enter your password
    HOST = '118.69.32.128' #enter the oracle db host url
    PORT = 1521 #enter the oracle port number
    SERVICE = 'XE' #enter the oracle db service name
    engine_str = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + \
                           ':' + str(PORT) + '/' + SERVICE + '?encoding=UTF-8&nencoding=UTF-8'
    engine = create_engine(engine_str, max_identifier_length = 128)
    print('-- CONNECTED TO SERVER --')
    return engine

ENGINE = connect_server()

##Execute SQL command
#import cx_Oracle
#conn_str = USERNAME + '/' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/' + SERVICE
#conn = cx_Oracle.connect(conn_str)
#c = conn.cursor() 

#Read SQL query or database table into a DataFrame
#df = pd.read_sql('SELECT * FROM {}'.format(db_name), engine)