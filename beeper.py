# -*- coding: utf-8 -*-
#2018/8/6 zc

core_c='C-5'
beats_long=500

note='''
G-4=250 A-4=250 C-5=1250 D-5=250 E-5=250 G-5=250 G-4=1500
D-5=250 E-5=250 G-5=1250 E-5=250 D-5=166 G-5=166 E-5=168 D-5=1500
D-5=250 E-5=250 G-5=1250 E-5=250 D-5=125 G-5=125 E-5=125 D-5=125 C-5=1250 D-5=250 E-5=500
E-4=250 G-4=125 A-4=125 D-5=1250 C-5=250 A-4=250 C-5=125 A-4=125 G-4=1500
'''
data=note.split()
        

#####################
def beeper(fre,ms=200):
    '''
    仅适用于windows的简易音频播放
    fre:频率
    ms:持续毫秒
    '''
    try:
        import winsound
    except Exception:
        return
    winsound.Beep(int(fre),ms)

#钢琴类
class Piano(object):
    '''
    钢琴类，用于建立一个标准数值体系
    '''
    #基础十二音名
    BASE_MUSICAL_ALPHABET={
        1:'C',
        2:'C#',
        3:'D',
        4:'D#',
        5:'E',
        6:'F',
        7:'F#',
        8:'G',
        9:'G#',
        10:'A',
        11:'A#',
        12:'B',
        }
    BEGIN_NOTE=10 #起始音名（默认10:a）
    OCTAVE_BEGIN_NUMBER=0 #起始八度数值（默认0）
    KEYS=88 #钢琴键数（默认88）

    def __init__(self):
        '''
        初始化
        '''
        self.init_number_alpha_dic()
        self.init_note_fre_dic()

    def init_number_alpha_dic(self):
        '''
        实例方法：初始化钢琴键数值与音名的映射关系，并存储为字典
        return:字典{钢琴键值:音名字符串}
        '''
        keys=range(1,self.KEYS+1)   #映射中的钢琴键数值
        self.NADIC={key:self.__get_alpha(key) for key in keys}  #建立映射字典
        self.ANDIC={v:k for k,v in self.NADIC.items()}  #逆向字典
        return self.NADIC

    def init_note_fre_dic(self):
        '''
        实例方法：初始化钢琴键音名与频率的映射关系，并存储为字典
        return:字典{音名字符串:频率}
        '''
        self.AFDIC = {
            k:440.0/2/2/2/2*(1.0594630944**(v-1))
            for k,v in self.ANDIC.items()
            }
        self.NFDIC = {
            k:self.AFDIC[v]
            for k,v in self.NADIC.items()
            }
        return self.AFDIC

    @classmethod
    def __get_alpha(cls,key):
        '''
        类方法：通过钢琴键值，获取音名
        return:音名字符串
        '''
        note_number=(key-1+cls.BEGIN_NOTE)%12 or 12 #获取音名
        octave_number=cls.OCTAVE_BEGIN_NUMBER+int((key-note_number)/12+1) #获取八度名
        return '%s-%s' % (cls.BASE_MUSICAL_ALPHABET[note_number],octave_number)
    
#创建标准钢琴，简化後续流程
ST_PIANO=Piano()

def __test():
    swanlake=[
        ('E-4',1000),
        ('A#-3',250),('B-3',250),('C-4',250),('D-4',250),
        ('E-4',250),('C-2',500),('C-4',250),
        ('E-4',750),('C-4',250),
        ('E-4',750),
        ('A-3',250),('C-4',250),('A-3',250),('F-3',250),('C-4',250),
        ('A-3',1500),
        ]
    for item in data:
        print(item)
        alp,ms=item.split('=')
        beeper(ST_PIANO.AFDIC[alp],int(ms))
    
if __name__ == '__main__':
     __test()
