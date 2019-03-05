# 增加一个考务工作，如：增加理工大学考务需要3人,可得8积分:addWork('理工大学', '考务', pnum = 3, integral = 8)
# site:地点  project:项目  pnum:人数  integral:积分
def addWork(site, project, pnum=1, integral=0):
    if site == '':
        print('地点不能为空！')
        return
    if project == '':
        print('工作内容不能为空！哈！')
        return
    if pnum < 0:
        print(('人数必须大于或等于1'))
        return
    if isinstance(integral, int):
        work = {'site': site, 'project': project, 'pnum': pnum, 'integral': integral}
        return work
    else:
        print('积分必须是整数')
        return


# 增加一个员工
# empno:工号  name:姓名  integral:积分
def addEmployee(empno, name, integral):
    if empno == '':
        print('工号不能为空！')
        return
    if name == '':
        print('姓名不能为空！')
        return
    if isinstance(integral, int):
        employee = {'empno': empno, 'name': name, 'integral': integral}
        return employee
    else:
        print('积分必须是整数')
        return


# 将本次考试所有考务工作加入列表
def createWorks():
    works = []
    works.append(addWork('考试中心', 'XX考务值班值班', pnum=1, integral=4))
    return works


# 将所有可分配员工加入列表
# def createEmployees():
#     employees = []
#     employees.append(addEmployee('01', '汪仁宏', integral=48))
#     employees.append(addEmployee('02', '吴明亮', integral=38))
#     employees.append(addEmployee('03', '林琳', integral=48))
#     employees.append(addEmployee('04', '林宝珠', integral=64))
#     employees.append(addEmployee('05', '陈书尧', integral=56))
#     employees.append(addEmployee('06', '曾晨曦', integral=32))
#     return employees

# 判断工作列表中的所有工作是否有足够的员工进行分配
def isEnoughEmployees(employees, works):
    employeeNum = len(employees)
    projectNum = 0
    for item in works:
        projectNum = projectNum + item['pnum']
    if employeeNum < projectNum:
        return False
    else:
        return True


# 1、将工作列表中的所有工作按积分从大到小排列
# 2、将员工目前积分数按从小到大排列
# 3、将以上两个列表中的‘工作地点’、‘工作内容’、‘分配人员姓名’汇总到一个列表
# 以上处理方法，将使本次排班积分低的工作人员优先安排积分高的工作，从而尽快增加他们的积分
def paiBan(employees, works):
    pLines = []
    works.sort(key=lambda x: x['integral'], reverse=True)  # 工作按积分从大到小排序
    employees.sort(key=lambda x: x['integral'])  # 人员按积分从小到大排序
    j = 0
    for item in works:
        for i in range(0, item['pnum']):
            pLines.append((item['site'], item['project'], employees[j]['name']))  # 汇聚到pLines列表
            employees[j]['integral'] = employees[j]['integral'] + item['integral']  # 更改人员积分
            j = j + 1
            if j == len(employees):
                print('人员已全部排上！')
                return pLines
    print('人员未全部排上!')
    writeFile(employees)
    return pLines

#将员工列表按工号顺序写入文件employees.dat,如果文件不存在，自动建立该文件
def writeFile(employees):
    employees.sort(key=lambda x: x['empno'])
    fileStr = ''
    file = open('employees.dat', mode='w+')
    for employee in employees:
        fileStr = fileStr + employee['empno'] + ':' + employee['name'] + ':' + str(employee['integral']) + '\n'
    file.write(fileStr)
    file.close()

#将人员名单读处内存
def readFile():
    employees = []
    file = open('employees.dat', mode='r')
    employeeStr = file.readline()
    while employeeStr != '':
        employeeList = employeeStr.strip('\n').split(':')
        employees.append({'empno': employeeList[0], 'name': employeeList[1], 'integral': int(employeeList[2])})
        employeeStr = file.readline()
    file.close()
    return employees

def printEmployees(employees):
    print('工号\t姓名\t积分')
    for employee in employees:
        print(employee['empno']+'\t'+employee['name']+'\t'+str(employee['integral']))

printEmployees(readFile())
print('='*30)
distributeWorks = paiBan(readFile(), createWorks())

print('='*30)
print('人员安排如下：')
for distributeWork in distributeWorks:
    print('工作地点：'+ distributeWork[0]+'\t'+'工作任务：'+ distributeWork[1]+'\t'+'工作人员姓名：'+distributeWork[2])
print('='*30)
printEmployees(readFile())
