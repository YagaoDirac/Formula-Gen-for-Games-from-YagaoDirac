'''
推荐使用vs code以及vs code插件版本的pylance，mypy编辑。python版本3.13，或者你如果要用别的版本应该也可以，
3.5之后的应该都可以，代码里面没有什么新特性。
实在搞不懂的，去 https://higher.smartedu.cn/ 上找一个python的课看看。

注意标点符号！！！！！！！！！必须用英语的！！！！！！！！！！包括逗号，括号，空格。除了字符串。

我简单解释一下这个工具的原理。
你们要用这个db生成器，生成一些转换关系，放到你的???_db.py文件里面。
最后在soup.py文件的最后写上实际的制作的情况。
例如你生成了一个a转换成b的关系，这个关系会加入到???_db.py文件，之后，你在游戏中，真的使用了a，那么你要在soup.py的最后，
写上相应的指令，来得到最终的结果。

整个算法的原理是，先计算出总量，计算出每一个成分在soup里面的占比，之后每一步计算转换关系，但是无论如何计算，
这个占比的综合永远是100%。最后计算了很多步之后，最终乘以总量，得到新的结果的每一种成分的量。

那么，转换关系来说，有几种典型结构。当然这个只是我觉得比较值得说的，你们也可以自己设计新的。
现在版本只支持一种成分转换成另外的，或者2种成分共同转换成另外的，转换目标不一定有几种，可能1种也可能很多。
公式是，每一个时间步，
Ca表示a在体系里面的占比（而不是绝对量），Cb同理。强度为s，时间为t。
a -> b
Ca变成Ca-Ca*s*t
Cb变成Cb+Ca*s*t
a+b -> c
Ca变成Ca-Ca*Cb*sa*t
Cb变成Cb-Ca*Cb*sb*t
Cc变成Cc+Ca*Cb*(sa+sb)*t

为了数值不抽风，在在db文件的开头对转换关系的强度做了限制，两个加起来不超过1即可，你们可以根据需要做调整。
如果转换过于缓慢，你们可以自行决定时间的对应关系，从而让转换更彻底。


！！！重要！！！
加入转换关系的时候，要同时讲名字加入到db文件的ingre_names里面，并且将转换关系加入到db文件的最后。
！！！重要！！！


如果一个物质没有任何的转换关系，那么它是惰性的，这种物质可以用于减缓其他反应的速率。可以考虑加一个，也可以考虑不加。不过不推荐过多。
加的方法就是直接在ingre_names里面加上它的名字即可。

1变1的情况，可以用于生食物变成熟食物。
例如
set_self_react_with_name("生肉","熟肉",0.001)
set_self_react_with_name("米","米饭",0.005)
最后的数字是转换速率，越大越快
可以使用 从一种原料 函数得到例子，例子将会被打印到命令行窗口

1变多的情况由多个使用相同原料的转换关系共同组成，使用多次one_to_one来得到。
注意，速率的差异会决定产物的相对数量。

用2个原料形成的变化和1个原料的情况相似，差异是，需要分别指定两个不同的原料的消耗量。
目标产物的生成量是两个消耗量的总和。
产生多种不同产物的写法和1变多的一样，不同的消耗量关系也会保留。
可以使用 从两种原料 函数得到例子，例子将会被打印到命令行窗口
'''

from typing import Optional
import random

print('请将以下代码复制到你的???_db文件的末尾')

def 从一种原料(原料:str, 结果:str, 速率:Optional[float] = None):
    if 速率 is None:
        速率 = random.random()*0.005
    print(f'set_self_react_with_name("{原料}","{结果}",{速率:.5f})')
    pass

#1变1举例
从一种原料("生肉","熟肉",0.001)
从一种原料("生肉","熟肉")#最后的数字会是随机的。第二次会覆盖第一次的结果。

#1变多举例
从一种原料("某植物","某植物的花",0.0001)
从一种原料("某植物","某植物的叶子",0.0003)
从一种原料("某植物","某植物的枝条",0.001)
从一种原料("某植物","某植物的根",0.0003)
#速率的差异会决定产物的相对数量。        


def 从两种原料(原料1:str, 原料2:str, 结果:str, 原料1消耗速率:Optional[float] = None, 原料2消耗速率:Optional[float] = None):
    if 原料1消耗速率 is None:
        原料1消耗速率 = random.random()*0.005
    if 原料2消耗速率 is None:
        原料2消耗速率 = random.random()*0.005
    print(f'set_cross_react_with_name("{原料1}","{原料2}","{结果}",{原料1消耗速率:.5f},{原料2消耗速率:.5f})')
    pass
#举例
从两种原料("原料1", "原料2", "结果", 0.001, 0.001)
从两种原料("原料1", "原料2", "另外一个结果", 0.001, 0.002)

