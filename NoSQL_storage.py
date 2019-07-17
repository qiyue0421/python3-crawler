import pymongo
from redis import StrictRedis

"""非关系型数据库存储"""
# NoSQL，全称Not Only SQL,意为不仅仅是SQL，泛指非关系型数据库。NoSQL是基于键值对的，而且不需要经过SQL层的解析，数据之间没有耦合性，性能非常高
# 常见的NoSQL数据库有Redis（键值存储数据库）、MongoDB（文档型数据库）等。
# 爬虫使用NoSQL的必要性：
# 1、对于爬虫的数据存储来说，一条数据可能存在某些字段提取失败而缺失的情况，而且数据可能随时调整
# 2、数据之间存在嵌套关系，如果是关系数据库需要提前建表，嵌套数据需要进行序列化操作才能存储


"""MongoDB存储"""
"""数据库连接
# MongoDB是由C++语言编写的非关系型数据库，是一个基于分布式文件存储的开源数据库系统，其内容存储形式类似JSON对象，它的字段值可以包含其他文档、数组及文档数组，非常灵活

# 连接MongoDB
client = pymongo.MongoClient(host='localhost', port=27017)  # 传入地址和端口
# client = pymongo.MongoClient('mongodb://localhost:27017/')  # 或者传入连接字符串

# 指定数据库
db = client.test
# db = client['test']  # 调用test属性也可以返回test数据库

# 指定集合
# MongoDB数据库包含许多集合，他们类似于关系型数据库中的表
collection = db.students  # 指定一个集合名称为students
"""


"""插入数据
student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}
result = collection.insert_one(student)  # 调用insert_one()方法插入数据
print(result.inserted_id)  # 每条数据都有_id属性来唯一标识，如果不显示指明，则自动产生。

student1 = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

student2 = {
    'id': '20170202',
    'name': 'Mike',
    'age': 21,
    'gender': 'male'
}
result = collection.insert_many([student1, student2])  # 调用insert_many()方法插入多条数据
print(result.inserted_ids)
"""


"""查询数据
query = collection.find_one({'name': 'Mike'})  # 单条数据查询，返回一个生成器对象
print(type(query))
print(query)

querys = collection.find({'age': 20})  # 多条数据查询，返回生成器
print(querys)
for i in querys:  # 遍历获取结果
    print(i)

# 条件查询——使用比较符号
# 符号    含义       示例
# $lt     小于       {'age': {'$lt': 20}}
# $gt     大于       {'age': {'$gt': 20}}
# $lte    小于等于   {'age': {'$lte': 20}}
# $gte    小于等于   {'age': {'$gte': 20}}
# $ne     不等于     {'age': {'$ne': 20}}
# $in     在范围内   {'age': {'$in': [20, 30]}}
# $nin    不在范围内 {'age': {'$nin': [20, 30]}}

# 查询年龄大于20的数据
querys = collection.find({'age': {'$gt': 20}})  # 查询的条件键值是一个字典，其键名为比较符号$gt，意为大于，键值为20
for i in querys:
    print(i)

# 功能查询——使用功能符号
# 符号     含义            示例                                               示例含义
# $regex   匹配正则表达式  {'name': {'$regex': '^M.*'}}                       name以M开头
# $exists  属性是否存在    {'name': {'$exists': True}}                        name属性存在
# $type    类型判断        {'age': {'$type': 'int'}}                          age的类型为int
# $mod     数字模操作      {'age': {'$mod': [5, 0]}}                          age模5余0
# $text    文本查询        {'$text': {'$search': 'Mike'}}                     text类型的属性中包含Mike字符串
# $where   高级条件查询    {'$where': 'obj.fans_count==obj.follows_count'}    自身粉丝数等于关注数

# 查询名字以M开头的学生数据
querys = collection.find({'name': {'$regex': '^M.*'}})
print()
for i in querys:
    print(i)
"""


"""计数——统计查询结果有多少条数据
count = collection.find().count()  # 统计所有数据
print(count)
count = collection.count_documents({'age': 20})  # 统计符合条件数据
print(count)
"""


"""排序
results = collection.find().sort('name', pymongo.ASCENDING)  # 指定升序，降序使用DESCENDING
print([result['name'] for result in results])
"""


"""偏移
results = collection.find().sort('name', pymongo.ASCENDING).skip(2).limit(2)  # 偏移两个位置，就忽略了前两个元素，得到第三个及以后的元素，使用limit(2)限制获取两个元素
print([result['name'] for result in results])
"""


"""更新
condition = {'name': 'Mike'}  # 指定查询条件
student = collection.find(condition)  # 查询数据
result = collection.update_one(condition, {'$set': student})  # 更新数据，需要使用$set类型操作符作为键名
# result = collection.update_many(condition, {'$set': {'age': 26}})  # 更新多条数据
print(result)
print(result.matched_count, result.modified_count)  # 获取匹配的数据条数和影响的数据条数
"""


"""删除
result = collection.delete_one({'name': 'Kevin'})  # 删除一条数据
print(result)
print(result.deleted_count)  # 获取删除的数据条数
result = collection.delete_many({'age': {'$lt': 25}})  # 删除所有符合条件的数据
print(result.deleted_count)
"""


"""Redis"""
# Redis是一个基于内存的高效的键值型非关系型数据库，存取效率极高，而且支持多种存储数据结构，使用非常简单
"""连接
redis = StrictRedis(host='localhost', port=6379, db=0, password='123456')
redis.set('name', 'Bob')
print(redis.get('name'))
"""
