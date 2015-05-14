class LineParam():
    def __init__(self):

    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self, p):
        rOffset, rOrientation = p;
        rX = 1.;
        rY = -rOffset/1.;
        rT = -rOrientation/2.;
        print( "rX: %5.2f, rY: %5.2f, rT: %5.2f" %( rX, rY, rT ) );
        #self.output_X(rX);
        #self.output_Y(rY);
        #self.output_T(min(max(rT,-1.),+1.)); # set zero to follow using straffing
        pass