# -*- coding: utf-8 -*-
#2018/8/5 zc
#2018/8/6 加入简易winsound的Beeper

#古琴音位模拟器
#需求1：给出单弦音高，推算出所有散、泛、按音的音高及指法
#需求2：给出七弦音高，推算出所有音域内所有散泛按指法的集合

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

#部分操作所需函数
def setify(*vals):
    '''
    将一串变量变成集合
    只支持拆分一次集合，非递归
    return:一个集合，不包含None
    '''
    result=set()
    items=vals
    for item in items:
        if isinstance(item,set):
            for underitem in item:
                result.add(underitem)
        else:
            result.add(item)
    return result-{None}
        
def dic_rev(dic):
    '''
    将一个字典key,value反转，并变为值集合形式
    dic:一个普通字典
    return:一个字典 {'键':{值的集合},'键',{值的集合},}
    '''
    result={}
    for k,v in dic.items():
        result[v]=setify(k,result.get(v))
    return result

def dic_merge(diclist,reverse=False):
    '''
    将多个集合字典合并为一个字典的集合形式
    diclist:多个集合式字典的列表
    reverse:是否反转所有字典，默认否
    return:一个字典 {'键':{值的集合},'键',{值的集合},}
    '''
    result={}
    for d in diclist:
        if reverse:d=dic_rev(d) #如反转
        for k,v in d.items():
            result[k]=setify(v,result.get(k))
    return result
    
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
        '''
        self.AFDIC = {
            k:440.0/2/2/2/2*(1.0594630944**(v-1))
            for k,v in self.ANDIC.items()
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

class Qinxian(object):
    '''
    琴弦类
    '''
    #散音键数值差
    S_DELTA={
        's':0,
        }
    #泛音键数值差
    F_DELTA={
        '13f':36,
        '12f':31,
        '11f':28,
        '10f':24,
        '9f':19,
        '8f':28,
        '7f':12,
        '6f':28,
        '5f':19,
        '4f':24,
        '3f':28,
        '2f':31,
        '1f':36,
        '4.4f':34,  #以下为非标准泛音
        '6.3f':34,
        '7.7f':34,
        }
    #按音键数值差
    A_DELTA={
        '13.7a':1,
        '13a':2,
        '11.8a':3,
        '11a':4,
        '10a':5,
        '9.4a':6,
        '9a':7,
        '8.4a':8,
        '8a':9,
        '7.7a':10,
        '7.3a':11,
        '7a':12,
        '6.7a':13,
        '6.4a':14,
        '6.2a':15,
        '6a':16,
        '5.7a':17,
        '5.2a':18,
        '5a':19,
        '4.8a':20,
        '4.6a':21,
        '4.3a':22,
        '4.1a':23,
        '4a':24,
        '3.8a':25,
        '3.5a':26,
        }
    
    def __init__(self,num=16,diapason=36,which=0):
        '''
        初始化
        num:弦的空弦音高（钢琴键数值）
        diapason:弦的音域，默认3个八度
        which:第几根弦，默认虚拟弦
        delta_dic:自动生成的字典：{钢琴键数值差值:技法字符串} 
        '''
        self.num=num
        self.diapason=diapason
        self.ddic=self.init_ddic(which)

    def init_ddic(self,which):
        '''
        实例方法：生成字典：{钢琴键数值差值:技法字符串}
        which:如有，自动补全古琴弦数据
        return:字典
        '''
        if which not in range(1,8):which=''  #非1-7弦为无效数据
        ddic=dic_merge([   #散泛按字典{钢琴键数值差值:技法字符串集合}
            self.S_DELTA,
            self.F_DELTA,
            self.A_DELTA,
            ],True)
        for k,v in ddic.items():
            cur_s=set()
            for item in v:
                cur_s.add( '%s%s' % (item,which) )  #添加琴弦数据
            ddic[k]=cur_s
        return ddic

class Fingering(object):
    '''
    指法类
    '''
    #琴弦名
    XIAN_NAMES={
        '1':'一弦',
        '2':'二弦',
        '3':'三弦',
        '4':'四弦',
        '5':'五弦',
        '6':'六弦',
        '7':'七弦',
        }        
    #音色名
    TONE_NAMES={
        's':'散',
        'f':'泛',
        'a':'按',
        }
    #音位名
    POS_NAMES={
        '1':'一徽',   #常规徽位
        '2':'二徽',
        '3':'三徽',
        '4':'四徽',
        '5':'五徽',
        '6':'六徽',
        '7':'七徽',
        '8':'八徽',
        '9':'九徽',
        '10':'十徽',
        '11':'十一徽',
        '12':'十二徽',
        '13':'十三徽',
        '13.7':'徽外七分',  #平均律按音
        '11.8':'十一徽八分',
        '9.4':'九徽四分',
        '8.4':'八徽四分',
        '7.7':'七徽七分',
        '7.3':'七徽三分',
        '6.7':'六徽七分',
        '6.4':'六徽四分',
        '6.2':'六徽二分',
        '5.7':'五徽七分',
        '5.2':'五徽二分',
        '4.8':'四徽八分',
        '4.6':'四徽六分',
        '4.3':'四徽三分',
        '4.1':'四徽一分',
        '3.8':'三徽八分',
        '3.5':'三徽五分',
        '6.3':'六徽三分',   #特殊泛音
        '4.4':'四徽四分',
        '7.7':'七徽七分',
        }

    @classmethod
    def trans(cls,fstr):
        '''
        类方法：翻译单个指法表字符串
        fstr:简写版指法字符串
        return:面向用户的指法字符串
        '''
        if 's' in fstr:
            pre,suf=fstr.split('s')
            tone=cls.TONE_NAMES['s']
        elif 'f' in fstr:
            pre,suf=fstr.split('f')
            tone=cls.TONE_NAMES['f']
        elif 'a' in fstr:
            pre,suf=fstr.split('a')
            tone=cls.TONE_NAMES['a']
        pos=''
        if pre:
            pos=cls.POS_NAMES.get(pre)
        name=''
        if suf:
            name=cls.XIAN_NAMES.get(str(suf))
        return '%s%s%s' % (pos,tone,name)

    @classmethod
    def dic_trans(cls,qx):
        '''
        类方法：翻译全部ddic
        qx:琴弦对象，使用其中的ddic及num属性
        return:面向用户的ddic
        '''
        ddic=qx.ddic
        num=qx.num
        new_dic={}
        for k,v in ddic.items():
            cur_n=ST_PIANO.NADIC.get(num+k)
            cur_s=set()
            for item in v:
                cur_s.add(cls.trans(item))
            new_dic[cur_n]=cur_s
        return new_dic
    
class Guqin(object):
    '''
    古琴类
    '''
    #调性名
    SCALE_NAMES={
        (16,18,21,23,25,28,30):'正调',
        (16,18,20,23,25,28,30):'慢三',
        (16,18,21,23,26,28,30):'紧五',
        }
    def __init__(self,scale='正调'):
        '''
        初始化，需要给出古琴音调或一至七弦的音高，默认为正调定弦
        scale:（1）汉字的调式名称（2）7个音名元组
        '''
        if isinstance(scale,str):
            for k,v in self.SCALE_NAMES.items():
                if v==scale:
                    self.nums=k #查出数值
                    self.scale=tuple([ST_PIANO.NADIC.get(i) for i in self.nums]) #找出音名
                    return
        else:
            self.scale=scale #直接给出各弦音名
            self.nums=tuple([ST_PIANO.ANDIC.get(i) for i in self.scale]) #各弦钢琴键数值
        
    def xian_fingerings(self,which):
        '''
        实例方法：获取某根弦的指法表
        which:哪根弦
        return:字典{音高:指法列表}
        '''
        qx=Qinxian(num=self.nums[which-1],which=which)
        return Fingering.dic_trans(qx)
        
    @property
    def all_fingerings(self):
        '''
        实例属性：古琴所有指法表
        '''
        merge={}
        for which in range(1,8): 
            merge=dic_merge([merge,self.xian_fingerings(which)])
        return merge

    def output(self,tone=None,inc_no=False,which=0):
        '''
        实例方法：输出所需音色指法表
        tone:音色，可使用散泛按sfa，默认输出所有
        inc_no:输出不符合要求的指法，默认不输出
        which:如果非0，则输出某一弦的数据
        '''
        if tone in Fingering.TONE_NAMES.values():
            pass
        else:
            tone=Fingering.TONE_NAMES.get(tone)
        print(
            '#'*20,
            self.SCALE_NAMES.get(self.nums,self.scale),
            '%s' % Fingering.XIAN_NAMES.get(str(which),''),
            '%s音' % tone,
            '#'*20,
            )            
        if which:
            fs=self.xian_fingerings(which)  #单弦指法数据
        else:
            fs=self.all_fingerings  #所有指法数据
        for item in ST_PIANO.ANDIC.keys():
            begon=False #本音已开始
            sets=fs.get(item)
            if sets:    #有指法
                for f in sets:
                    if not tone or tone in f:   #输出全部，或有需求音色
                        if not begon:   #本音第一次出现
                            print(item,':')
                            beeper(ST_PIANO.AFDIC[item])
                            begon=True
                        print('    ',f)
            else:
                if inc_no:print(item,': 无')
    
def __test():
    l=('E-3','D-4','E-4','G-4','A-4','C-5','C-8')
    for item in l:
        beeper(ST_PIANO.AFDIC[item],1000)    
    piano=Piano()
    #print(piano.NADIC)  #字典{钢琴键数值:音名}
    qx=Qinxian()
    #print(qx.fdic)   #字典{音程差数值:指法字符串列表}
    gq=Guqin()
    #print(gq.xian_fingerings(1))   #一弦字典{音高:指法列表}
    #print(gq.all_fingerings)
    #gq.output(inc_no=True)
    gq.output('f')
    gq=Guqin(scale=('C-2','D-2','E-2','G-2','A-2','C-3','D-3'))    #慢三
    gq.output(tone='按',which=3)
    gq.output(tone='散',inc_no=True)

if __name__ == '__main__':
    __test()
