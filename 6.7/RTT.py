import configparser

'''程序运行屏幕输出要点：
显示初始RTT的值
显示本次的RTT值
计算显示平滑后RTTs
计算显示当前的RTO
重复上述步骤，一直到完成所有测量RTT数据为止
'''

config = configparser.ConfigParser()
config.read("./config.ini")

rtt=config.get("RTO","RTT")
rttlist=rtt.split(",")

alpha=float(config.get("RTO","Alpha"))
beta=float(config.get("RTO","Beta"))

EstimatedRTT=0.0
DevRTT=0.0
for i in rttlist:
    print("-------------------------------------")
    print("Original RTT is", "%.2f ms"%EstimatedRTT if EstimatedRTT!=0 else "Undefined")
    print("RTT is",float(i),"ms in this round!")
    SampleRTT=int(i)
    if EstimatedRTT==0:
        EstimatedRTT=SampleRTT
    else:
        EstimatedRTT=(1-alpha)*EstimatedRTT+alpha*SampleRTT
    DevRTT=(1-beta)*DevRTT+beta
    print("the new adapted RTT : %.2f ms "%EstimatedRTT)
    print("current RTO: %.2f ms"%(EstimatedRTT+4*DevRTT))

