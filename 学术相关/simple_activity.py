def spec_activity():
    i=1
    while i:
         Qh,R,I,Id=input("enter paras: ")
         s=Qh/R*1000000/210
         Ik=1/(1/I-1/Id)
         spec_activity=Ik/s*1000
         print "specific activity(mA/cm2): ",spec_activity
         print "ECSA(cm2)= ",s
        # i=input("continue(0/1):")
   # print "over!"

spec_activity()
