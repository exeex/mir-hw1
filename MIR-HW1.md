# MIR HW1
Q1~ Q4 程式碼在：
key_detector.py     Q1~ Q5  
loader.py  
temp_blue.py         Q5  
temp_classic.py     Q1~ Q3  
temp_KS.py            Q4  

# Q1

result:

    #Q1
    gamma = 100
    [('pop', 0.16), ('blues', 0.07), ('metal', 0.05), ('rock', 0.17), ('hiphop', 0.01)]

pop和rock類的表現比較好，這可能是因為pop和rock所使用的音符多半是按照一般七聲音階，大小調系統的音符。

metal由於大量使用破音吉他、超大聲的鼓組，以及吼叫的唱腔，因此metal類的音樂在頻譜上的訊號分佈很雜，干擾了chromagram的產生，使得我們用chromagram分析效果很差

blues和hiphop比較有趣
藍調音樂使用的不是大小調七聲音階系統，是用下面這兩種藍調6聲/7聲音階系統
https://en.wikipedia.org/wiki/Blues_scale

![](https://d2mxuefqeaa7sj.cloudfront.net/s_5909B5834B28A596DEB3970B02A47D88036B098D2E866EB7F074745861A82748_1525786184250_file.png)

![](https://d2mxuefqeaa7sj.cloudfront.net/s_5909B5834B28A596DEB3970B02A47D88036B098D2E866EB7F074745861A82748_1525786196810_file.png)


我們做了個實驗，我把Major/Minor的Template換成上面這兩種藍調音階系統的Template，得到了一個新的結果：

    gamma = 100
     [('pop', 0.139), ('blues', 0.14), ('metal', 0.03), ('rock', 0.062), ('hiphop', 0.106)] 

藍調的表現果然提昇了許多。

更有趣的是hiphop也一起提昇了，由此可見，hiphop所使用的音階系統可能和藍調音樂更為相近。（不過我不是這方面的專家，有待考證。）




# Q2
    #Q2
    
    gamma = 1
    [('pop', 0.22), ('blues', 0.06), ('metal', 0.07), ('rock', 0.25), ('hiphop', 0.02)]
    
    gamma = 10
    [('pop', 0.19), ('blues', 0.07), ('metal', 0.06), ('rock', 0.22), ('hiphop', 0.02)]
    
    gamma = 100
    [('pop', 0.16), ('blues', 0.07), ('metal', 0.05), ('rock', 0.17), ('hiphop', 0.01)]
    
    gamma = 1000
    [('pop', 0.15), ('blues', 0.07), ('metal', 0.05), ('rock', 0.16), ('hiphop', 0.01)]

gamma是一個非線性校正，類似的概念也用在影像處理
可以用來補強或削弱某些訊號，這邊看起來是gamma=1更好一點


# Q3
    #Q3
    
    gamma = 1
    [('pop', 0.33100000000000007), ('blues', 0.09300000000000001), ('metal', 0.11800000000000005), ('rock', 0.365), ('hiphop', 0.05999999999999999)] 
    
    gamma = 10
    [('pop', 0.31700000000000006), ('blues', 0.12200000000000001), ('metal', 0.11200000000000003), ('rock', 0.3440000000000001), ('hiphop', 0.06)] 
    
    gamma = 100
    [('pop', 0.30500000000000005), ('blues', 0.139), ('metal', 0.10200000000000004), ('rock', 0.30600000000000005), ('hiphop', 0.045)] 
    
    gamma = 1000
    [('pop', 0.30500000000000005), ('blues', 0.134), ('metal', 0.10500000000000004), ('rock', 0.30400000000000005), ('hiphop', 0.04999999999999999)] 

顯然這個毫無疑問一定會比Q2更高，我可以從數學證明證明這個結果出來一定會更高
高得很合理！沒啥好討論的


# Q4


    #Q4
    
    gamma = 1
    [('pop', 0.47), ('blues', 0.27), ('metal', 0.26), ('rock', 0.37), ('hiphop', 0.09)]
    [('pop', 0.5409999999999999), ('blues', 0.28300000000000003), ('metal', 0.311), ('rock', 0.46699999999999997), ('hiphop', 0.14100000000000001)]
    
    gamma = 10
    [('pop', 0.45), ('blues', 0.26), ('metal', 0.22), ('rock', 0.35), ('hiphop', 0.09)]
    [('pop', 0.518), ('blues', 0.28300000000000003), ('metal', 0.278), ('rock', 0.45699999999999996), ('hiphop', 0.131)]
    
    gamma = 100
    [('pop', 0.43), ('blues', 0.21), ('metal', 0.21), ('rock', 0.32), ('hiphop', 0.09)]
    [('pop', 0.493), ('blues', 0.23800000000000002), ('metal', 0.281), ('rock', 0.42700000000000005), ('hiphop', 0.131)]
    
    gamma = 1000
    [('pop', 0.43), ('blues', 0.2), ('metal', 0.21), ('rock', 0.31), ('hiphop', 0.09)]
    [('pop', 0.503), ('blues', 0.228), ('metal', 0.281), ('rock', 0.419), ('hiphop', 0.126)]

這個每個gamma值後面有兩組結果，一個是Q1的ACC算法一個是Q3的ACC算法
這個真是有顯著的提昇。

主要是在7聲音階中，主音和第五音的組合是最和諧的（大調），這兩個音的比例應該要占的比其他組合高。

而原本的template不能忠實的反映出這項事實（都是1），KS template則能比較能忠實呈現大小調音符的分佈，因此有更好的表現我並不感到意外。


# Q5

這兩個方法是純粹靠統計加上一些音階理論所構成的。
其中限制就如我在Q1的討論中所提及。西洋古典音樂的大小調7聲音階的模型，並不能很好的拿來解釋所有音樂。在blue/hiphop/meta奇糟無比的表現就是很好的例子。

我們也證明了，使用藍調6/7聲音階系統取代大小調音階，可以得到比較好的表現
（hiphop也順帶提昇了）
temp_blue.py

    Heptatonic_template = np.array([[1,0,0,1,0,1,1,1,0,1,0,1]])
    Hexatonic_template = np.array([[1,0,0,1,0,1,0,1,0,1,0,1]])

不過表現還是不如KS法，或許我們可以將KS法的idea(用統計分析的數字取代0/1)，再加在這個template上，可以獲得更好的表現。

再來，有很多時候，看音符組成比例，並不能正確的偵測出整個樂曲的key。可能還需要從結構下手。我們可以隨便設計個無腦的捲積神經網路去搞定這件事。



# Q6

程式碼在
local_key_detector.py
key_detector.py

我的做法是對整首歌做chroma
且令hop_size=sample_rate

因此如果整首有800秒
會得到一個array其shape = (12, 800)

然後取sliding window, window = 10
得array = (10, 12, 800)

reshape得 X.shape  = (120,800)
且Key為 y.shape =(800) 

直接丟到一個multi-class SVM， kernel function='rbf'

我隨便找10首train
找5首test

得結果：

train

    auc= 0.707

test

    auc= 0.391

