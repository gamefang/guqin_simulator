# -*- coding: utf-8 -*-
#2018/8/26
#python2

import mingus.core.notes as notes

#检查音符合法性
notes.is_valid_note('C')    # True
#音符、值互转
notes.note_to_int('C')  # 0
notes.int_to_note(1)    # C#
#半音升降
notes.augment('C')  # C#
notes.diminish('C#')    # C
#大小调转化(无方法)
#notes.to_minor('C') # A
#notes.to_major('A') # C

#无模块
#import mingus.core.diatonic as diatonic
#十二音
#diatonic.basic_keys
#E调七音
#diatonic.get_notes('E')

import mingus.core.intervals as interval
#间隔半音数
interval.measure('C','D')   #2

import mingus.core.scales as scales
#爱奥尼音阶对象
scales.Ionian('C')


#音对象
from mingus.containers import Note
#C4音对象
n=Note('C')
#变为C5
n.set_note('C',5)
#音对象属性
n.name  #十二音名
n.octave #第几八度
n.dynamics #其它属性
#音对象方法
int(n)  #音对象的数值
c=Note()
c.from_int(12)  #使用数值创建音对象
c.octave_up()   #升八度
c.octave_down() #降八度
c.change_octave(2)  #升n八度
c.transpose('3',up=True)    #向上升三度
c.augment() #升半音
c.diminish()    #降半音
c.remove_redundant_accidentals()    #清理多余升降号(只能成对清理，烂)


#谱容器
from mingus.containers import NoteContainer
#创建谱容器对象（继承列表，完全可以按列表操作，不用看下面的）
n=NoteContainer(['A-3','C-5','B-4'])
n.add_note('F-1')   # 0位加音
n.remove_note('B',4)   #删音
n.empty()   #清空


#乐器音色
from mingus.containers.instrument import Instrument, Piano, Guitar
#创建乐器对象
i=Instrument()
i.range #乐器音域
i.set_range( ( Note('C-2'),Note('E-4') ) )    #设定音域
i.note_in_range('F-4')  #判断音是否在乐器音域内
#音轨
from mingus.containers import Track
t=Track(i)  #乐器放入音轨容器


#MIDI音乐播放(安装困难)
#from mingus.midi import fluidsynth
#fluidsynth.init("soundfont.SF2")
#fluidsynth.play_Note( Note('C-5') )


from mingus.midi import MidiFileOut
MidiFileOut.write_NoteContainer('test.mid',n)
