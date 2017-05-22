import hashlib
import pickle
import os
import time
import copy
import platform
ori_path = os.getcwd()
'''
history = 2013.03.28, 2013.03.29, 2013.03.31, 2013.04.02, 2013.04.16, 2013.04.17, 2013.04.18, 2013.04.24, 2013.04.26,
          2013.04.28, 2013.04.30, 2013.05.09, 2013.05.13, 2013.05.15, 2013.05.16, 2013.05.24, 2013.05.30, 2013.06.02,
          2013.06.05, 2013.06.10, 2013.06.14, 2013.07.01, 2013.07.09, 2013.07.10, 2013.07.30, 2013.08.02, 2013.09.06,
          2013.09.11, 2013.09.14, 2013.10.02, 2013.11.10, 2013.11.12, 2013.11.27, 2013.11.30, 2013.12.02, 2013.12.10,
          2013.12.31, 2013.01.09, 2014.01.13, 2014.02.05, 2014.12.15, 2015.03.02, 2017.05.22
'''

#-----------------------------------------------------------------------------------------------


class openFastAfile:    
    
    def __init__(self):
        self.data_number = 0
        self.FastA_dictionary = {} 
    
    def open(self, file_name = '.fa'):        
        
        FastA_dictionary = {}
        total = open(file_name,'r').read()
        total = '\n'.join(total.split('\n')[0:-1])
        A = total.split('>')
        A = multilistshorten([A])[0]
        
        for x in A:
            ID = "".join("".join(x).split('\n')[0])
            sequence = "".join([x.replace('\n', "") for x in "".join(x).split('\n')[1:]])
            FastA_dictionary[ID] = sequence
        
        self.data_number = len(FastA_dictionary.keys())
        self.FastA_dictionary = FastA_dictionary
        
        return FastA_dictionary
    
    def build(self, dictionary = {}):
        self.data_number = len(dictionary.keys())
        self.FastA_dictionary = dictionary
    
    def read(self, ID = ''):        
        
        result = self.FastA_dictionary[ID]
        
        return result
    
    def report(self, ID_list = []):
        
        if ID_list == []:
            ID_list = list(self.FastA_dictionary.keys())
        else:
            ID_list = ID_list
        
        ID_list.sort()
        E = []
        for x in ID_list:
            E.append('>' + x + '\n' + self.read(x))
        
        display = '\n'.join(E)+'\n'+str(len(E))
        
        return display

#-----------------------------------------------------------------------------------------------


def listXYreverse(XY = [[]]):
    
    i = 1
    j = 1
    E = []
    YX = []
    while i < len(XY[0]) + 1:
        
        j = 1
        E = []
        while j < len(XY) + 1:
            E.append(XY[j-1][i-1])
            j = j + 1
            
        YX.append(E)
      
        i = i + 1

    return YX

#-----------------------------------------------------------------------------------------------


def listNSplit(E = [], N = 0):
    
    result = [E[i:i+N] for i in range(0, len(E), N)]

    return result

#-----------------------------------------------------------------------------------------------


def listPartSeparate(E = [], Part = 0):
    
    N = int((len(E) / Part)) + 1
    result = [E[i:i+N] for i in range(0, len(E), N)]
    
    return result

#-----------------------------------------------------------------------------------------------


def multilistextend(inp = [[]]):
    
    oup = []
    E = [int(len(x)) for x in inp]
    E.sort()
    
    for x in inp:
        if int(len(x)) < E[-1]: 
            x.extend(' '*(E[-1]-int(len(x))))
            oup.append(x)
        else:
            oup.append(x)

    return oup

#-----------------------------------------------------------------------------------------------


def multilistshorten(inp = [[]]):
    
    oup = []
    for E in inp:
        oup.append([x for x in E if x != ' ' and x != ""])
    
    return oup

#-----------------------------------------------------------------------------------------------


def listIntersection(E = [[]]):
    
    if len(E) < 2:
        print('input = ')
        print(E)
        print('input is too small to ListIntersection')
        print('print location: ')
        input()
        raise KeyboardInterrupt
    elif len(E) == 2:
        R = set(E[0]) & set(E[1])
    else:
        R = set(E[0]) & set(E[1])
        i = 3
        while i < len(E) + 1:
            R = set(R) & set(E[i-1])
            i = i + 1
    
    T = list(R)
    T.sort()
    
    return T
    
#-----------------------------------------------------------------------------------------------


def listUnion(E = [[]]):
    
    if len(E) < 2:
        print('input = ')
        print(E)
        print('input is too small to ListIntersection')
        print('print location: ')
        input()
        raise KeyboardInterrupt
    elif len(E) == 2:
        R = set(E[0]) | set(E[1])
    else:
        R = set(E[0]) | set(E[1])
        i = 3
        while i < len(E) + 1:
            R = set(R) | set(E[i-1])
            i = i + 1
    
    T = list(R)
    T.sort()
    
    return T

#-----------------------------------------------------------------------------------------------


class tabfilewithtitle:
    
    def __init__(self):
        self.title_tuple = [()]
        self.title_dicX = {}
        self.title_dicY = {}
        self.title_box = {}
        self.main_key = ""
        self.main_key_list = []
        self.title_list = []
        self.len_X = 0
        self.len_Y = 0
    
    def copy(self):
        return copy.deepcopy(self)
    
    def build(self, XY = 'X or Y', title_dic = {}, main_key = ''):
        
        if XY == 'X':
            self.main_key = main_key
            self.title_dicX = title_dic
            self.title_dicY = {main_key:1}
            self.title_box = {}
            self.main_key_list = []
            E_ = dicKeysortVal(title_dic, '<-')
            self.title_list = [x for x in E_ if x != main_key]
            self.len_X = len(title_dic)
            self.len_Y = 1
            self.title_tuple = [(title_dic[x], x) for x in E_]
            
        elif XY == 'Y':
            self.main_key = main_key
            self.title_dicX = {main_key:1}
            self.title_dicY = title_dic
            self.title_box = {}
            self.main_key_list = [x for x in dicKeysortVal(title_dic, '<-') if x != main_key]
            self.title_list = []
            self.len_X = 1
            self.len_Y = len(title_dic)
            self.title_tuple = [(1, main_key)]

        else:
            print('title_dic length = ', len(title_dic))
            print('main_key = ', main_key)
            print('Error at tabfilewithtitle.build()\nPlease define the XY value ! ')
            print('print location: ')
            input()
            raise KeyboardInterrupt
        
        return self.title_tuple
    
    def open(self, file_name = '.txt', main_key = ''):
        
        target_path = os.getcwd()
        
        h = hashlib.new('ripemd160')
        f = open(file_name, 'rb')
        h.update(f.read())
        f.close()
        
        if os.path.exists(target_path+r'/__pycache__') == False:
            os.makedirs(target_path+r'/__pycache__')
        os.chdir(target_path+r'/__pycache__')
        
        for i in range(3):
            try:
                Pickle_box = open('tabfilewithtitle_cache', 'rb')
                file_box = pickle.load(Pickle_box)
                Pickle_box.close()
                
                if file_name in file_box[0].keys():
                    
                    if h.hexdigest() == file_box[0][file_name]:
                        
                        if file_box[1][file_name] == main_key:
                            
                            f = open(file_box[2][file_name], 'rb')
                            pickle_EE = pickle.load(f)
                            f.close()
                            self.title_tuple = pickle_EE[0]
                            self.title_dicX = pickle_EE[1]
                            self.title_dicY = pickle_EE[2]
                            self.title_box = pickle_EE[3]
                            self.main_key = pickle_EE[4]
                            self.main_key_list = pickle_EE[5]
                            self.title_list = pickle_EE[6]
                            self.len_X = pickle_EE[7]
                            self.len_Y = pickle_EE[8]
                            
                            Pickle_box.close()
                            os.chdir(target_path)
                            return self.title_tuple
                            
                        else:
                            file_box[0].pop(file_name)
                            file_box[1].pop(file_name)
                            file_box[2].pop(file_name)
                            pass
                        
                    else:
                        file_box[0].pop(file_name)
                        file_box[1].pop(file_name)
                        file_box[2].pop(file_name)
                        pass
                    
                else:
                    pass
                
            except:
                time.sleep(1)
            
        file_box = [{}, {}, {}]
        
        os.chdir(target_path)

        E_ = open(file_name,'r').readlines()
        title = E_[0].replace('\n', "")
        if len(E_[-1].split('\t')) == 1:
            data = [x.replace('\n', "") for x in E_[1:-1]]
        else:
            data = [x.replace('\n', "") for x in E_[1:]]

        title_list = title.split('\t')
        main_key_location = title_list.index(main_key)
        self.title_list = [x for x in title_list if x != main_key]
        
        k = 2
        title_dic = {}
        title_dic[main_key] = 1
        for title in self.title_list:
            title_dic[title] = k
            k = k + 1
        
        j = 2
        key_M = {}
        key_M[main_key] = 1
        for row in data:
            W = "".join(row).split('\t')[main_key_location]
            key_M[W] = j
            j = j + 1
        E_ = dicKeysortVal(key_M, '<-')
        self.main_key_list = [x for x in E_ if x != main_key]
        
        
        title_box = {}
        position = 1
        colunm_N = 1
        for title in title_list:
            
            if position-1 == main_key_location:
                
                position = position + 1
                continue
                
            else:
                
                row_N = 1
                for row in data:
                    
                    integer = "".join("".join(row).split('\t')[position-1].split('.')[0])
                    decimal = "".join("".join(row).split('\t')[position-1].split('.')[-1])
                    if str.isdigit(integer) == True and str.isdigit(decimal) == True:
                        title_box[(colunm_N+1, row_N+1)] = float("".join(row).split('\t')[position-1])
                    else:
                        title_box[(colunm_N+1, row_N+1)] = "".join(row).split('\t')[position-1]
                    
                    row_N = row_N + 1
                    
                position = position + 1
                
            colunm_N = colunm_N + 1
        
        item_number = len(title_dic.keys())
        
        title_tuple = [(x[1],x[0]) for x in title_dic.items()]
        title_tuple.sort()
        self.title_tuple = title_tuple
        self.title_dicX = title_dic
        self.title_dicY = key_M
        self.title_box = title_box
        self.len_X = item_number
        self.len_Y = len(key_M)
        self.main_key = main_key
        
        #os.chdir(ori_path+r'/__pycache__')
        os.chdir(target_path+r'/__pycache__')
        f = open(file_name+'.tabfilewithtitle.picklebox', 'wb')
        pickle.dump([self.title_tuple, self.title_dicX, self.title_dicY, self.title_box,
                     self.main_key, self.main_key_list, self.title_list, self.len_X, self.len_Y], f, )
        f.close()
        
        file_box[0][file_name] = h.hexdigest()
        file_box[1][file_name] = self.main_key
        file_box[2][file_name] = file_name+'.tabfilewithtitle.picklebox'
        
        Pickle_box = open('tabfilewithtitle_cache', 'wb')
        pickle.dump(file_box, Pickle_box, )
        Pickle_box.close()
        
        os.chdir(target_path)
        return self.title_tuple
    
    def read(self, X = '', Y = ''):
        
        P = (self.title_dicX, self.title_dicY, self.title_box)
        try:
            result = P[2][(P[0][X], P[1][Y])]
        except:
            print('X =', X, ', Y =', Y)
            print("Can not catch the value !")
            input()
            raise KeyboardInterrupt
        
        return result
    
    def readrow(self, XY = 'X or Y', inp = ""):
        
        P = (self.title_dicX, self.title_dicY, self.title_box)
        result = []
        
        if XY == 'X':
            
            result.append(inp)
            location = P[1][inp]
            for Tup in [(x, location) for x in range(2,2+self.len_X-1)]:
                result.append(self.title_box[Tup])
            
        elif XY == 'Y':

            result.append(inp)
            location = P[0][inp]
            for Tup in [(location, x) for x in range(2,2+self.len_Y-1)]:
                result.append(self.title_box[Tup])
            
        else:
            print(inp)
            print('Error at tabfilewithtitle.readrow()\nPlease define the XY value ! ')
            print('print location: ')
            input()
            raise KeyboardInterrupt
        
        return result
    
    def printtable(self, column_list = []):
        
        lenght_list = []
        
        E_ = [len(x) for x in [self.main_key]+self.main_key_list]
        E_.sort()
        lenght_list.append(E_[-1])
        
        for title in self.title_list:
            E_ = [len(str(x)) for x in self.readrow('Y', title)]
            E_.sort()
            lenght_list.append(E_[-1])
        oup_list = []
        
        E_ = []
        i = 1
        for title in [self.main_key]+self.title_list:
            
            E_.append('| '+title.rjust(lenght_list[i-1], ' ')+' |')
            i = i + 1
        oup_list.append(E_)
        
        for key in self.main_key_list:
            row = self.readrow('X', key)
            
            E_ = []
            i = 1
            for read in row:
                E_.append('| '+str(read).rjust(lenght_list[i-1], ' ')+' |')
                i = i + 1
            oup_list.append(E_)
        
        print('\n'.join(["".join(x) for x in oup_list]))
        
        return
    
    def report(self, file_name = '.txt'):
        
        display_list = []
        
        title_list = [x[1] for x in self.title_tuple]
        one_line = '\t'.join(title_list)
        display_list.append(one_line)

        E_ = []
        for key in self.main_key_list:
            row = self.readrow('X', key)
            E_.append('\t'.join([str(x) for x in row]))
        
        two_line = '\n'.join(E_)
        display_list.append(two_line)
        
        display = '\n'.join(display_list)+'\n'+str(self.len_Y-1)

        ori_path = os.getcwd()
        if file_name != '.txt':
            
            file_box = [{}, {}, {}]
            
            h = hashlib.new('ripemd160')
            h.update(display.encode('cp950'))
            
            if os.path.exists(ori_path+r'/__pycache__') == False:
                os.makedirs(ori_path+r'/__pycache__')
            os.chdir(ori_path+r'/__pycache__')
            
            f = open(file_name+'.tabfilewithtitle.picklebox', 'wb')
            pickle.dump([self.title_tuple, self.title_dicX, self.title_dicY, self.title_box,
                         self.main_key, self.main_key_list, self.title_list, self.len_X, self.len_Y], f, )
            f.close()
            
            file_box[0][file_name] = h.hexdigest()
            file_box[1][file_name] = self.main_key
            file_box[2][file_name] = file_name+'.tabfilewithtitle.picklebox'
            
            Pickle_box = open('tabfilewithtitle_cache', 'wb')
            pickle.dump(file_box, Pickle_box, )
            Pickle_box.close()
        else:
            pass
        
        os.chdir(ori_path)
        
        return display
    
    def append(self, XY = 'X or Y', inp = "", value = []):
        
        if XY == 'X':
            
            if len(value) == self.len_X-1:

                self.title_dicY[inp] = self.len_Y+1
                i = 2
                for item in value:
                    self.title_box[(i, self.len_Y+1)] = item
                    i = i + 1
                self.main_key_list = self.main_key_list+[inp]

            else:
                print(inp)
                print(value)
                print('Error at tabfilewithtitle.append()\nPlease check the length of value !\nThat is different from the table. ')
                print('print location: ')
                input()
                raise KeyboardInterrupt
        
        elif XY == 'Y':

            if len(value) == self.len_Y-1:

                self.title_dicX[inp] = self.len_X+1
                i = 2
                for item in value:
                    self.title_box[(self.len_X+1, i)] = item
                    i = i + 1
                self.main_key_list = self.main_key_list

            else:
                print(inp)
                print(value)
                print('Error at tabfilewithtitle.append()\nPlease check the length of value !\nThat is different from the table. ')
                print('print location: ')
                input()
                raise KeyboardInterrupt

        else:
            print(inp)
            print(value)
            print('Error at tabfilewithtitle.append()\nPlease define the XY value ! ')
            print('print location: ')
            input()
            raise KeyboardInterrupt
        
        title_tuple = [(x[1],x[0]) for x in self.title_dicX.items()]
        title_tuple.sort()
        self.title_tuple = title_tuple
        self.len_X = len(self.title_dicX)
        self.len_Y = len(self.title_dicY)
        self.title_list = dicKeysortVal({x:y for x, y in self.title_dicX.items() if x != self.main_key}, '<-')
        
        return
    
    def delete(self, inp = ""):
        
        if inp == self.main_key:
            
            print(inp, '= main_key')
            print('Error at tabfilewithtitle.delete()\n\nmain_key can not delete !\n="=  What are you doing~!')
            print('print location: ')
            input()
            raise KeyboardInterrupt
            
        elif inp in self.title_dicX:
            
            value_large_Then_inp = [x for x in dicKeysortVal(self.title_dicX, '<-') if self.title_dicX[x] > self.title_dicX[inp]]
            copy = self.readrow('Y', inp)
            #change title_box value
            for key in value_large_Then_inp:
                
                for i in range(2,self.len_Y+1):
                    self.title_box[(self.title_dicX[key]-1, i)] = self.title_box[(self.title_dicX[key], i)]
                self.title_dicX[key] = self.title_dicX[key]-1
            #delete inp
            for i in range(2,self.len_Y+1):
                self.title_box.pop((self.len_X, i))
            self.title_dicX.pop(inp)
            
        elif inp in self.title_dicY:
            value_large_Then_inp = [x for x in dicKeysortVal(self.title_dicY, '<-') if self.title_dicY[x] > self.title_dicY[inp]]
            copy = self.readrow('X', inp)
            #change title_box value
            for key in value_large_Then_inp:
                
                for i in range(2,self.len_X+1):
                    self.title_box[(i, self.title_dicY[key]-1)] = self.title_box[(i, self.title_dicY[key])]
                self.title_dicY[key] = self.title_dicY[key]-1
            #delete inp
            for i in range(2,self.len_X+1):
                self.title_box.pop((i, self.len_Y))
            self.title_dicY.pop(inp)
            
        else:
            print(inp)
            print('Error at tabfilewithtitle.delete()\n\nPlease check the input !\nThat is not in the table. ')
            print('print location: ')
            input()
            raise KeyboardInterrupt
        
        title_tuple = [(x[1],x[0]) for x in self.title_dicX.items()]
        title_tuple.sort()
        self.title_tuple = title_tuple
        self.len_X = len(self.title_dicX)
        self.len_Y = len(self.title_dicY)
        
        if len(self.title_dicY) != 0:
            self.main_key_list = [x for x in dicKeysortVal(self.title_dicY, '<-') if x != self.main_key]
        else:
            self.main_key_list = []
        
        if len(self.title_dicX) != 0:
            self.title_list = dicKeysortVal({x:y for x, y in self.title_dicX.items() if x != self.main_key}, '<-')
        else:
            self.title_list = []
        
        return copy
    
    def insert(self, XY = 'X or Y', inp = "", value = [], location = 0):
        
        if XY == 'X':
            
            if len(value) == self.len_X-1:

                value_large_Then_inp = [x for x in dicKeysortVal(self.title_dicY, '->') if self.title_dicY[x] > location]

                for key in value_large_Then_inp:
                    for i in range(2,self.len_X+1):
                        self.title_box[(i, self.title_dicY[key]+1)] = self.title_box[(i, self.title_dicY[key])]
                    self.title_dicY[key] = self.title_dicY[key]+1

                for i in range(2,self.len_X+1):
                    self.title_box[(i, location+1)] = value[i-2]
                self.title_dicY[inp] = location+1

            else:
                print(inp)
                print(value)
                print('Error at tabfilewithtitle.insert()\n\nPlease check the length of value !\nThat is different from the table. ')
                print('print location: ')
                input()
                raise KeyboardInterrupt
        
        elif XY == 'Y':

            if len(value) == self.len_Y-1:

                value_large_Then_inp = [x for x in dicKeysortVal(self.title_dicX, '->') if self.title_dicX[x] > location]

                for key in value_large_Then_inp:
                    for i in range(2,self.len_Y+1):
                        self.title_box[(self.title_dicX[key]+1, i)] = self.title_box[(self.title_dicX[key], i)]
                    self.title_dicX[key] = self.title_dicX[key]+1

                for i in range(2,self.len_Y+1):
                    self.title_box[(location+1, i)] = value[i-2]
                self.title_dicX[inp] = location+1

            else:
                print(inp)
                print(value)
                print('Error at tabfilewithtitle.insert()\n\nPlease check the length of value !\nThat is different from the table. ')
                print('print location: ')
                input()
                raise KeyboardInterrupt

        else:
            print(inp)
            print(value)
            print('Error at tabfilewithtitle.insert()\n\nPlease define the XY value ! ')
            print('print location: ')
            input()
            raise KeyboardInterrupt
        
        title_tuple = [(x[1],x[0]) for x in self.title_dicX.items()]
        title_tuple.sort()
        self.title_tuple = title_tuple
        self.len_X = len(self.title_dicX)
        self.len_Y = len(self.title_dicY)
        self.main_key_list = [x for x in dicKeysortVal(self.title_dicY, '<-') if x != self.main_key]
        self.title_list = dicKeysortVal({x:y for x, y in self.title_dicX.items() if x != self.main_key}, '<-')
        
        return
    
    def find(self, value = ''):
        
        result_Array = []
        for key in self.title_box.keys():
            if self.title_box[key] == value:
                result_Array.append(key)
        
        return result_Array
    
    def XYreverse(self):
        
        new_title_box = {}
        for key in self.title_box.keys():
            new_title_box[(key[1], key[0])] = self.title_box[key]
        
        self.title_box = new_title_box
        M_ = self.title_dicX
        self.title_dicX = self.title_dicY
        self.title_dicY = M_
        M_ = self.title_list
        self.title_list = self.main_key_list
        self.main_key_list = M_
        self.len_X = len(self.title_dicX)
        self.len_Y = len(self.title_dicY)
        self.title_list = dicKeysortVal({x:y for x, y in self.title_dicX.items() if x != self.main_key}, '<-')
        
        return
    
    def mainkeyChange(self, new_main_key = ""):
        
        if new_main_key in self.title_dicX.keys():

            new_mainkey_row = self.readrow('Y', new_main_key)

            if len([x for x in new_mainkey_row if type(x) != str]) == 0:

                new_title_dicY = {}
                new_title_dicY[new_main_key] = 1
                for i in range(2, self.len_Y+1):
                    self.title_box[(self.title_dicX[new_main_key], i)] = self.main_key_list[i-2]

                    new_title_dicY[new_mainkey_row[i-1]] = i
                self.title_dicY = new_title_dicY

                self.title_dicX[self.main_key] = self.title_dicX[new_main_key]
                self.title_dicX[new_main_key] = 1

                self.main_key = new_main_key
                self.main_key_list = new_mainkey_row[1:]
                self.len_X = len(self.title_dicX)
                self.len_Y = len(self.title_dicY)
                self.title_list = dicKeysortVal({x:y for x, y in self.title_dicX.items() if x != self.main_key}, '<-')

            else:
                print('new_main_key_list = ('+str(new_mainkey_row)+') \nCan not add it in new_main_key_list unless it is String, please double check~!')
                print('print location: ')
                input()
                raise KeyboardInterrupt
            
        else:
            print('new_main_key = ('+new_main_key+') is not in title_dicX, please double check~!')
            print('print location: ')
            input()
            raise KeyboardInterrupt
        
        return
    
#-----------------------------------------------------------------------------------------------


def mixXOrderfile(tabfilewithtitle_list = [], outputFile_Name = '.txt'):
    
    check_title_list = []
    for TabT in tabfilewithtitle_list:
        check_title_list.append(TabT.title_tuple.__str__())
    
    if len(set(check_title_list)) != 1:
        print('The title of tables are different, please double check~!')
        print('print location: ')
        input()
        raise KeyboardInterrupt
    else:
        pass
    
    table = tabfilewithtitle()
    table.build('X', TabT.title_dicX, TabT.main_key)
    
    new_title_box = {}
    new_title_dicY = {TabT.main_key:1}
    new_main_key_list= []
    i = 0
    for TabT in tabfilewithtitle_list:
        for key in TabT.title_box.keys():
            new_title_box[(key[0], key[1]+i)] = TabT.title_box[key]

        for key in TabT.main_key_list:
            new_main_key_list.append(key)
            new_title_dicY[key] = TabT.title_dicY[key]+i

        i += TabT.len_Y-1
    table.title_box = new_title_box
    table.title_dicY = new_title_dicY
    table.main_key_list = new_main_key_list
    table.len_X = len(table.title_dicX)
    table.len_Y = len(table.title_dicY)
    table.title_list = dicKeysortVal({x:y for x, y in table.title_dicX.items() if x != table.main_key}, '<-')
    title_tuple = [(x[1],x[0]) for x in table.title_dicX.items()]
    title_tuple.sort()
    table.title_tuple = title_tuple

    if outputFile_Name != '.txt':
        
        f = open(outputFile_Name, 'w')
        f.write(table.report())
        f.close()
        
        h = hashlib.new('ripemd160')
        f = open(outputFile_Name, 'rb')
        h.update(f.read())
        f.close()
        
        target_path = os.getcwd()
        
        if os.path.exists(target_path+r'/__pycache__') == False:
            os.makedirs(target_path+r'/__pycache__')
        os.chdir(target_path+r'/__pycache__')
        
        try:
            Pickle_box = open('tabfilewithtitle_cache', 'rb')
            file_box = pickle.load(Pickle_box)
            Pickle_box.close()
        except:
            file_box = [{}, {}, {}]
        
        f = open(outputFile_Name+'.tabfilewithtitle.picklebox', 'wb')
        pickle.dump([table.title_tuple, table.title_dicX, table.title_dicY, table.title_box,
                     table.main_key, table.main_key_list, table.len_X, table.len_Y], f, )
        f.close()
        
        file_box[0][outputFile_Name] = h.hexdigest()
        file_box[1][outputFile_Name] = table.main_key
        file_box[2][outputFile_Name] = outputFile_Name+'.tabfilewithtitle.picklebox'
        
        Pickle_box = open('tabfilewithtitle_cache', 'wb')
        pickle.dump(file_box, Pickle_box, )
        Pickle_box.close()
        
        os.chdir(target_path)
        
    else:
        pass
    
    return table

#-----------------------------------------------------------------------------------------------


def newOrderfile(title_list = ['order', 'A', 'B' ], group_list = [['a', 'b'], ], outputFile_Name = '.txt'):
    
    table = tabfilewithtitle()
    
    i = 1
    title = {}
    for tit in title_list:
        title[tit] = i
        
        i = i + 1
    table.build('X', title, 'order')
    
    i =  1
    group_list.sort()
    for group in group_list:
        order = str(i)+'_'

        table.append('X', order, group)
        
        i = i + 1

    if outputFile_Name != '.txt':
        
        f = open(outputFile_Name, 'w')
        f.write(table.report(outputFile_Name))
        f.close()
        
        h = hashlib.new('ripemd160')
        f = open(outputFile_Name, 'rb')
        h.update(f.read())
        f.close()
        
        target_path = os.getcwd()
        
        if os.path.exists(target_path+r'/__pycache__') == False:
            os.makedirs(target_path+r'/__pycache__')
        os.chdir(target_path+r'/__pycache__')
        
        try:
            Pickle_box = open('tabfilewithtitle_cache', 'rb')
            file_box = pickle.load(Pickle_box)
            Pickle_box.close()
        except:
            file_box = [{}, {}, {}]
        
        f = open(outputFile_Name+'.tabfilewithtitle.picklebox', 'wb')
        pickle.dump([table.title_tuple, table.title_dicX, table.title_dicY, table.title_box,
                     table.main_key, table.main_key_list, table.len_X, table.len_Y], f, )
        f.close()
        
        file_box[0][outputFile_Name] = h.hexdigest()
        file_box[1][outputFile_Name] = table.main_key
        file_box[2][outputFile_Name] = outputFile_Name+'.tabfilewithtitle.picklebox'
        
        Pickle_box = open('tabfilewithtitle_cache', 'wb')
        pickle.dump(file_box, Pickle_box, )
        Pickle_box.close()
        
        os.chdir(target_path)
        
    else:
        pass
    
    return table

#-----------------------------------------------------------------------------------------------


def tabfileaddorder(file_name = '.txt', title_list = "['order', 'A', 'B'] or 'X'", outputFile_Name = '.txt'):
    
    if title_list == 'X':
        B = open(file_name,'r').read()
        Line_list = B.split('\n')[0:-1]
        
        E = []
        i = 1
        E.append('\t'.join(['order', Line_list[0]]))
        for Line in Line_list[1:]:
            E.append('\t'.join([str(i)+'_', Line]))
            i = i + 1
        
        result = '\n'.join(E)
        display = '\n'.join([result, str(len(E)-1)])

    else:
        B = open(file_name,'r').read()
        Line_list = B.split('\n')[0:-1]
        
        E = []
        i = 1
        for Line in Line_list:
            E.append('\t'.join([str(i)+'_', Line]))
            i = i + 1
        
        result = '\n'.join(E)
        title = '\t'.join(title_list)
        display = '\n'.join([title, result, str(len(E))])
    
    if outputFile_Name != '.txt':
        f = open(outputFile_Name, 'w')
        f.write(display)
        f.close()
    else:
        pass
    
    return display

#-----------------------------------------------------------------------------------------------


def dicKeysortVal(dictionary = {}, pattern = '-> or <-'):
    result = []
    BtupleA = []
    if pattern == '->':
        
        for x in dictionary.keys():
            BtupleA.append((dictionary[x],x))
        
        BtupleA.sort()
        BtupleA.reverse()
        for x in BtupleA:
            result.append(x[1])
        
    elif pattern == '<-':
        
        for x in dictionary.keys():
            BtupleA.append((dictionary[x],x))
        
        BtupleA.sort()        
        for x in BtupleA:
            result.append(x[1])
        
    return result

#-----------------------------------------------------------------------------------------------


def ntComRev(string = '', complete = 'C or nC', reverse = 'r or nr', case = 'U or L', seq_type = 'RNA or DNA'):
    
    if string.islower() == True:
        string_type = 1
    elif string.isupper() == True:
        string_type = 0
    else:
        #print('string is hybrid! ')
        string_type = 2
    
    if complete == 'C':
        string = string.upper()
        E = []
        for x in string:
            if x == 'G':
                x = 'C'
                E.append(x)
            elif x == 'C':
                x = 'G'
                E.append(x)
            elif x == 'T':
                x = 'A'
                E.append(x)
            elif x == 'A':
                x = 'T'
                E.append(x)
            elif x == 'U':
                x = 'A'
                E.append(x)
    elif complete == 'nC':
        string = string.upper()
        E = [x for x in string]
    else:
        string = string.upper()
        E = [x for x in string]
    
    if reverse == 'nr':
        result = "".join(E)
    elif reverse == 'r':
        E.reverse()
        result = "".join(E)
    else:
        result = "".join(E)
    
    if case == 'U':
        result = result.upper()
    elif case == 'L':
        result = result.lower()
    else:
        if string_type == 1:
            result = result.lower()
        elif string_type == 0:
            result = result.upper()
        elif string_type == 2:
            result = result.upper()
    
    if seq_type == 'RNA':
        result = result.replace('T', 'U')
        result = result.replace('t', 'u')
    elif seq_type == 'DNA':
        result = result.replace('U', 'T')
        result = result.replace('u', 't')
    else:
        result = result
    
    return result

#-----------------------------------------------------------------------------------------------


def ntmatch(A_seq = '', B_seq = ''):
    
    if len(A_seq) >= len(B_seq):
        
        template = A_seq
        seq = B_seq
        marker1 = 'A'
        marker2 = 'B'
        
    elif len(B_seq) >= len(A_seq):
        
        template = B_seq
        seq = A_seq
        marker1 = 'B'
        marker2 = 'A'
    
    def seqreturn(marker, loac):
        if marker == 'A':
            seq = B_seq
            template = A_seq
            
            new_seq = '-'*loac + seq
            new_template = template + '-'*(len(new_seq)-len(template))
            
            if len(new_template) != len(new_seq):
                new_seq = new_seq + '-'*(len(template)-len(new_seq))
            
            new_A = new_template
            new_B = new_seq
            
        elif marker == 'B':
            seq = A_seq
            template = B_seq
            
            new_seq = '-'*loac + seq
            new_template = template + '-'*(len(new_seq)-len(template))
            
            if len(new_template) != len(new_seq):
                new_seq = new_seq + '-'*(len(template)-len(new_seq))
            
            new_A = new_seq
            new_B =  new_template
        return new_A, new_B
    
    def locationscore(template, seq, marker = 'A or B'):
        score_list = []
        location = 0
        while location < (len(template)/1):
            
            seq_location = 0
            score = 0
            
            new_seq = '-'*location + seq
            new_template = template + '-'*(len(new_seq)-len(template))
            
            i = 1
            for x in seq:
                
                if x == new_template[location+i-1]:
                    score = score + 1
                    
                i = i + 1
            
            if score > int(len(template)/1):
                R = seqreturn(marker, location)
                result = (R[0], R[1])
                return result
            
            score_list.append((score, location, marker))
            
            location = location + 1
        return score_list
    
    score_list_1 = locationscore(template, seq, marker1)
    if isinstance(score_list_1,tuple) == True:
        return score_list_1
    score_list_2 = locationscore(seq, template, marker2)
    if isinstance(score_list_2,tuple) == True:
        return score_list_2
    
    score_list = score_list_1 + score_list_2
    
    score_list.sort()
    marker = score_list[-1][2]
    loac = score_list[-1][1]
    
    R = seqreturn(marker, loac)
    
    result = (R[0], R[1])
    
    return result

#-----------------------------------------------------------------------------------------------


class LoopingTime:
    
    def __init__(self, ):
        self.looptitle = ""
        self.total_loop = 0
        self.mark = '|'
        self.passingtime_list = []
        self.needTime = ""
        self.switch = 'off'
    
    def open(self, looptitle = "", total_list = []):
        self.looptitle = looptitle
        self.total_loop = len(total_list)
    
    def showEndTime(self, passingtime = 'seconds from loopend cut loopin', switch = 'off'):
        
        self.passingtime_list.append(passingtime)
        if len(self.passingtime_list) < self.total_loop:
            ending = '\r'
        elif len(self.passingtime_list) == self.total_loop:
            ending = '\n'
        else:
            print('Looptime Error')
            raise KeyboardInterrupt
        
        mean = self.meanSD(self.passingtime_list)[0]
        self.needTime = mean*self.total_loop
        if switch == 'on':
            display = '{0}\t{1:25}\t{2}/100\tTotal time(m): {3:.8}\tStill time(m): {4:.8}'
            display = display.format(self.looptitle,
                                     self.mark*int(20/self.total_loop*len(self.passingtime_list)),
                                     str(int(100/self.total_loop*len(self.passingtime_list))),
                                     str(self.needTime/60),
                                     str(mean*(self.total_loop-len(self.passingtime_list))/60))
        else:
            display = '{0}\t{1:25}\t{2}/100'
            display = display.format(self.looptitle,
                                     self.mark*int(20/self.total_loop*len(self.passingtime_list)),
                                     str(int(100/self.total_loop*len(self.passingtime_list))))
        
        print(display, end = ending)

    def clean(self,):
        self.looptitle = ""
        self.total_loop = 0
        self.mark = '|'
        self.passingtime_list = []
        self.needTime = ""

    def meanSD(self, E = [0.0]):
        
        mean = 0.0
        SD = 0.0
        i = 0.0
        j = 0.0
        
        if len(E) == 0:
            
            mean = 'na'
            SD = 'na'
            
        elif len(E) > 0:
            
            for x in E:
                i = i + float(x)
            mean = float(i/len(E))
            
            for x in E:
                j = j + (float(x)-mean)**2
            SD = float(j/len(E))**(0.5)
        
        return mean, SD

#-----------------------------------------------------------------------------------------------


class ReadDirectory:

    def __init__(self, dir):
        self.ori_dir = dir
        self.temp_dir = ""
        self.file_list = []
        sysstr = platform.system()
        if sysstr == 'Windows':
            self.spacer = '\\'
        elif sysstr == 'Linux':
            self.spacer = '/'
        else:
            print("Error: doesn't support~!")
            exit()

    def read(self):
        E_ = self.ori_dir.split(self.spacer)
        self.check_dir(E_[-1], self.spacer.join(E_[:-1]))

    def check_dir(self, root, path):
        self.adddirfiles()
        os.chdir(path+self.spacer+root)
        E = os.listdir(path+self.spacer+root)
        dirs = [x for x in E if os.path.isdir(x) is True]
        if len(dirs) != 0:
            for x in dirs:
                self.check_dir(x, path+self.spacer+root)
            return
        else:
            return

    def adddirfiles(self):
        if os.getcwd() not in self.file_list:
            self.file_list.append(os.getcwd())
        s = os.getcwd()
        E = os.listdir(os.getcwd())
        for x in E:
            if s+self.spacer+x not in self.file_list:
                self.file_list.append(s+self.spacer+x)
