def sive2mongo(data):
    import pymongo
    # mongodb服务的地址和端口号
    mongo_url = "127.0.0.1:27017"
    # 连接到mongodb，如果参数不填，默认为“localhost:27017”
    client = pymongo.MongoClient(mongo_url)
    # 连接到数据库myDatabase
    DATABASE = "money_data"
    db = client[DATABASE]
    # 连接到集合(表):myDatabase.myCollection
    COLLECTION = "data"
    data_coll = db[COLLECTION]
    student_coll = db['student']
    cate = ['ID', '部门', '商户名称', '交易金额', '交易时间', '卡余额', '入账日期']
    for row in data:
        temp = {}
        for i in range(len(row)):
            temp[cate[i]] = row[i]
        if not data_coll.find(temp):
            data_coll.insert(temp)
    new_data = []
    for item in data:
        if item[0] not in new_data:
            # print(item)
            new_data.append(item[0])
            temp = {'ID': item[0], "name": "null", "class": item[1]}
            if not data_coll.find(temp):
                student_coll.insert(temp)

    return new_data


# 通过 联合条件   查询数据，返回 list 格式
def get_data_by_condition(_id='', _className='', _shop='', _postingDate=''):
    import pymongo
    # mongodb服务的地址和端口号
    mongo_url = "127.0.0.1:27017"
    # 连接到mongodb，如果参数不填，默认为“localhost:27017”
    client = pymongo.MongoClient(mongo_url)
    # 连接到数据库myDatabase
    DATABASE = "money_data"
    db = client[DATABASE]
    # 连接到集合(表):myDatabase.myCollection
    COLLECTION = "data"
    db_coll = db[COLLECTION]
    data = []
    dic = {}
    if _id != '':
        dic['ID'] = str(_id)
    if _className != '':
        dic['部门'] = str(_className)
    if _shop != '':
        dic['商户名称'] = str(_shop)
    if _postingDate != '':
        dic['入账日期'] = str(_postingDate)

    # print(dic)
    for i in db_coll.find(dic):
        del i['_id']
        temp = []
        for item in i.values():
            temp.append(item)
        data.append(temp)

    print('共查询数据: ', len(data), ' 条。')
    print(data)

    # 根据日期进行排序 向下升序
    data.sort(key=lambda item: item[4],reverse=False)
    print(data)
    return data, len(data)


# 通过 id 查找数据，返回 list 格式
def get_data_by_id(_id):
    import pymongo
    # mongodb服务的地址和端口号
    mongo_url = "127.0.0.1:27017"
    # 连接到mongodb，如果参数不填，默认为“localhost:27017”
    client = pymongo.MongoClient(mongo_url)
    # 连接到数据库myDatabase
    DATABASE = "money_data"
    db = client[DATABASE]
    # 连接到集合(表):myDatabase.myCollection
    COLLECTION = "data"
    db_coll = db[COLLECTION]
    data = [['ID', '部门', '商户名称', '交易金额', '交易时间', '卡余额', '入账日期']]
    for i in db_coll.find({'ID': str(_id)}):
        del i['_id']

        data.append(i.values())
        print(list(i.values()))
    print('共查询数据:', len(data) - 1, '条。')
    print(data)

    return data


# 通过班级查找数据，返回 list 格式
def get_data_by_class(_class):
    import pymongo
    # mongodb服务的地址和端口号
    mongo_url = "127.0.0.1:27017"
    # 连接到mongodb，如果参数不填，默认为“localhost:27017”
    client = pymongo.MongoClient(mongo_url)
    # 连接到数据库myDatabase
    DATABASE = "money_data"
    db = client[DATABASE]
    # 连接到集合(表):myDatabase.myCollection
    COLLECTION = "data"
    db_coll = db[COLLECTION]
    data = [['ID', '部门', '商户名称', '交易金额', '交易时间', '卡余额', '入账日期']]
    for i in db_coll.find({'部门': str(_class)}):
        del i['_id']
        data.append(i.values())
        print(list(i.values()))
    print('共查询数据:', len(data) - 1, '条。')
    print(data)
    return data


# 通过商家查找数据，返回 list 格式
def get_data_by_shop(_shop):
    import pymongo
    # mongodb服务的地址和端口号
    mongo_url = "127.0.0.1:27017"
    # 连接到mongodb，如果参数不填，默认为“localhost:27017”
    client = pymongo.MongoClient(mongo_url)
    # 连接到数据库myDatabase
    DATABASE = "money_data"
    db = client[DATABASE]
    # 连接到集合(表):myDatabase.myCollection
    COLLECTION = "data"
    db_coll = db[COLLECTION]
    data = [['ID', '部门', '商户名称', '交易金额', '交易时间', '卡余额', '入账日期']]
    for i in db_coll.find({'商户名称': str(_shop)}):
        del i['_id']
        data.append(i.values())
        print(list(i.values()))

    return data

    # posting date
    # 通过班级查找数据，返回 list 格式


# 通过入账日期查找数据，返回 list 格式
def get_data_by_posting_date(_posting_date):
    import pymongo
    # mongodb服务的地址和端口号
    mongo_url = "127.0.0.1:27017"
    # 连接到mongodb，如果参数不填，默认为“localhost:27017”
    client = pymongo.MongoClient(mongo_url)
    # 连接到数据库myDatabase
    DATABASE = "money_data"
    db = client[DATABASE]
    # 连接到集合(表):myDatabase.myCollection
    COLLECTION = "data"
    db_coll = db[COLLECTION]
    data = [['ID', '部门', '商户名称', '交易金额', '交易时间', '卡余额', '入账日期']]
    for i in db_coll.find({'入账日期': str(_posting_date)}):
        del i['_id']
        data.append(i.values())
        print(list(i.values()))
    return data


# 从数据库获取学生的学号信息，返回 list 格式
def get_all_ids():
    import pymongo
    # mongodb服务的地址和端口号
    mongo_url = "127.0.0.1:27017"
    # 连接到mongodb，如果参数不填，默认为“localhost:27017”
    client = pymongo.MongoClient(mongo_url)
    # 连接到数据库myDatabase
    DATABASE = "money_data"
    db = client[DATABASE]
    # 连接到集合(表):myDatabase.myCollection
    COLLECTION = "student"
    db_coll = db[COLLECTION]
    data = []
    for i in db_coll.find():
        data.append(i['ID'])
    new_data = []
    for i in data:
        if i not in new_data:
            new_data.append(i)
        else:
            pass

    return new_data


if __name__ == '__main__':
    pass
    # 下面两行代码是将文件保存到数据库
    # import fileReader
    #
    # mongoDB().sive2mongo(fileReader.fileReader('data.csv').csvReader())

    # 根据ID获取数据
    # data = mongoDB().get_data_by_id(100000)
    #
    # Ananlyser.personAnalyser(data).get_allmoney_out()
    # print('@@@@@@@@@@@@@@@@')
    # Ananlyser.personAnalyser(data).get_allmoney_in()

    # print(get_data_by_class('2017级-计算机学院-大数据1701'))
