'''
history =  2013.06.05, 2013.06.14, 2013.06.25, 2013.09.14, 2013.09.15, 2013.12.10, 2015.03.02
'''
# there is a "#@" follow the list_name_in_code at the end of the code in processing_code
# because list_name_in_code is the morker of the "file_name" list start_side.
# And "#@" is the marker of the "file_name" list end_side.
# That will be using in modification of the origen processing_code.
#-----------------------------------------------------------------------------------------------
import Raxpy3Libbasic_2015_03_02 as RaxLib
import platform
#-----------------------------------------------------------------------------------------------


def multiprocessing(jobs_list = [], processing_code = "", list_name_in_code = "", CUP_N = 0, deleteTempNorY = 'Y'):

    ori_path = RaxLib.os.getcwd()
    sysstr = platform.system()

    #-----------------------------------------------------------------------------------------------s
    #seperate jobs_list
    RaxLib.os.chdir(ori_path)

    modify_jobs_list = ['@##@n@##@@'.join(x.split('\n')) for x in jobs_list]
    modify_jobs_list = ['#@#@t@#@#@'.join(x.split('\t')) for x in modify_jobs_list]
    list_box = RaxLib.listPartSeparate(modify_jobs_list, CUP_N)

    showTime1 = RaxLib.LoopingTime()
    showTime1.open('build job_part ', list_box)

    i = 1
    for job in list_box:
        t = RaxLib.time.time()

        RaxLib.newOrderfile(['order', 'job'], [[x] for x in job], 'job_part_'+str(i)+'.txt')

        t1 = RaxLib.time.time()-t
        showTime1.showEndTime(t1)
        i += 1

    #-----------------------------------------------------------------------------------------------
    #open job_part file

    file_list = RaxLib.os.listdir(ori_path)
    sub_file_list = [x for x in file_list if 'job_part_' in x]

    for job_file in sub_file_list:

        number = job_file.split('job_part_')[1].split('.txt')[0]

        table = RaxLib.tabfilewithtitle()
        table.open(job_file, 'order')

        A = '['+','.join(["'"+'\\t'.join('\\n'.join(x.split('@##@n@##@@')).split('#@#@t@#@#@'))+"'" for x in table.readrow('Y', 'job')])+']'

        #-----------------------------------------------------------------------------------------------
        #seperate processing_code

        P1 = processing_code.replace("'\n'","'\\n'").split(list_name_in_code+' =')
        P2 = P1[1].split('#@')
        P2.pop(0)
        B = '#@'.join(P2)
        P1[1] = A +'#@'+ B
        midify_code = (list_name_in_code+' =').join(P1)

        #-----------------------------------------------------------------------------------------------
        #add check_point_file
        end_info = '''
#-----------------------------------------------------------------------------------------------
os.chdir(r"'''+ori_path+'''")
out_put_file_name= 'py_end_'+str('''+str(number)+''')+'.py'
f = open(out_put_file_name, 'w')
f.write(' ')
f.close()
'''
        midify_code = midify_code+'\n'+end_info
        out_put_file_name = 'py_'+str(number)+'.py'
        f = open(out_put_file_name, 'w')
        f.write(midify_code)
        f.close()

    #-----------------------------------------------------------------------------------------------
    #start python file

    file_list = RaxLib.os.listdir(ori_path)
    py_file_list = [x for x in file_list if 'py_' in x]
    print(py_file_list)
    for py_file in py_file_list:
        print('python '+py_file+' &')
        RaxLib.os.system('python '+py_file+' &')

    #-----------------------------------------------------------------------------------------------
    #check processing end or not
    s = 1
    while s < 43200:
        end_file_list = RaxLib.os.listdir(ori_path)
        checkfilelist = [x for x in end_file_list if 'py_end_' in x]
        if len(checkfilelist) == len(list_box):

            #-----------------------------------------------------------------------------------------------
            #delete job_list_.txt file
            RaxLib.os.chdir(ori_path)
            i = 1
            while i < len(list_box)+1:
                if deleteTempNorY == 'N':
                    pass
                elif deleteTempNorY == 'Y':
                    if sysstr == 'Windows':
                        cmd = 'del'
                    elif sysstr == 'Linux':
                        cmd = 'rm'
                    RaxLib.os.system(cmd+' job_part_'+str(i)+'.txt')
                    RaxLib.os.system(cmd+' py_'+str(i)+'.py')
                    RaxLib.os.system(cmd+' py_end_'+str(i)+'.py')
                else:
                    print("please Enter 'N' or 'Y', Thanks~! ")
                i += 1

            print('processing end')
            return

        else:

            RaxLib.time.sleep(10)
            s += 10

    #-----------------------------------------------------------------------------------------------
    #delete job_list_.txt file
    RaxLib.os.chdir(ori_path)
    i = 1
    while i < len(list_box)+1:
        if deleteTempNorY == 'N':
            pass
        elif deleteTempNorY == 'Y':
            RaxLib.os.system('rm job_part_'+str(i)+'.txt')
            RaxLib.os.system('rm py_'+str(i)+'.py')
            RaxLib.os.system('rm py_end_'+str(i)+'.py')
        else:
            print("please Enter 'N' or 'Y', Thanks~! ")
        i += 1

    print('processing end')
    return

if __name__ == '__main__':
    #-----------------------------------------------------------------------------------------------
    #to list directory in "C:\Program Files" and separate into 3 parts to run
    #then get the response in "./Result"
    import os

    while True:
        ori_path = os.getcwd()
        os.chdir(r"C:\Program Files")
        E_ = [x for x in os.listdir(os.getcwd()) if os.path.isdir(x) is True]

        processing_code = '''

import Raxpy3Libbasic_2015_03_02 as Lib
import os
ori_path = os.getcwd()
os.chdir(r"C:\Program Files")
E_ = [x for x in os.listdir(os.getcwd()) if os.path.isdir(x) is True]#@
for x in E_:
    #t = time.time()
    C = Lib.ReadDirectory(ori_path)
    C.read()
    os.chdir(ori_path)
    if 'Result' not in os.listdir(os.getcwd()):
        os.mkdir('Result')
    os.chdir(ori_path+'\\\\'+'Result')
    f = open(x+'_directory_and_file_list.txt', 'w')
    f.write('\\n'.join(C.file_list))
    f.close()
    #print(time.time()-t)

        '''

        os.chdir(ori_path)
        multiprocessing(E_, processing_code, 'E_', 3, 'N')
