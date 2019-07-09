import pymysql

"""关系型数据库"""
# 关系型数据库是基于关系模型的数据库，而关系模型是通过二维表来保存的，所以它的存储方式就是行列组成的表，每一列是一个字段，每一行是一条记录。
# 现阶段比较流行的关系型数据库有：MySQL、SQLite、Oracle、SQL Server、DB2等

"""MySQL的存储
# 连接数据库
db = pymysql.connect(host='localhost', user='root', password='123456', port=3306)  # 声明一个MySQL连接对象db
cursor = db.cursor()  # 获取MySQL的操作游标，利用游标来执行SQL语句
cursor.execute('SELECT VERSION()')
data = cursor.fetchone()  # 获取第一条数据，即版本号
print('Database version:', data)
# cursor.execute("CREATE DATABASE qiyue DEFAULT CHARACTER SET utf8")  # 创建数据库qiyue，并设置默认编码为utf-8
db.close()

# 创建表
db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='qiyue')
cursor = db.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id))")  # 创建表语句

# 插入数据与更新数据
data = {
    'id': '20120004',
    'name': 'Jacy',
    'age': 25
}
table = 'students'
keys = ', '.join(data.keys())
values = ', '.join(['%s'] * len(data))

sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '.format(table=table, keys=keys, values=values)  # 构造动态sql语句，如果数据存在更新数据；不存在则插入数据
update = ','.join([" {key} = %s".format(key=key) for key in data])  # 更新语句
sql += update
print(sql)
# INSERT INTO students(id, name, age) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE  id = %s, name = %s, age = %s
try:
    if cursor.execute(sql, tuple(data.values()) * 2):
        print('Successful')
        db.commit()  # commit()方法实现数据插入，对于数据插入、更新、删除操作，都需要调用该方法才能生效
except Exception as e:
    print(e)
    print('Failed')
    db.rollback()  # 异常处理，如果执行失败，则调用rollback()执行数据回滚

# 删除数据
table = 'students'
condition = 'age < 22'
sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table, condition=condition)
try:
    cursor.execute(sql)
    db.commit()  # 仍然需要commit()方法才能生效
except:
    db.rollback()

# 查询数据
sql = 'SELECT * FROM students WHERE age >= 20'
try:
    cursor.execute(sql)  # 注意查询操作不需要commit()方法
    print('Count:', cursor.rowcount)
    one = cursor.fetchone()  # 获取结果的第一条数据，指针偏移到下一条数据，返回类型为元组
    print('One:', one)
    results = cursor.fetchall()  # 获取结果的所有数据，返回的是偏移指针指向的数据一直到结束的所有数据
    # row = cursor.fetchone()  # 可以用while循环加fetchone()方法来获取所有数据，优点是数据流过大时节省内存资源
    #     if row:
    #         print('Row:', row)
    #         row = cursor.fetchone()  # 每循环一次，指针会偏移一条数据，随用随取
    print('Results:', results)
    print('Results Type:', type(results))
    for row in results:
        print(row)
except:
    print('Error')
"""