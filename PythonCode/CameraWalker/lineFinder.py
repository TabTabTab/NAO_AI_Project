import cv2
import numpy
import time
numpy.set_printoptions(threshold=numpy.nan)
import Image
from naoqi import ALBroker
from naoqi import ALProxy
from naoqi import ALModule

IP = "192.168.0.101"  # Replace here with your NaoQi's IP address.
PORT = 9559


rPeriod=1.0
bVerbose=True

headRadAngle=-0.0

pic_height=240
pic_width=320

# all these valuesare used only for the andle -0.3 rad
transform=headRadAngle!=-0.0
start=20.0/90*pic_width
step=4.0/90/pic_height*pic_width
end=24.0/89*pic_width # should be 90 but better to use a too long array
## if headANgle=0.3 these values will work nicely:
addList=numpy.arange(start,end,step)
pi=3.14
headDegAngle=-headRadAngle*(pi/4)
def printImageData(img):
    print "left img angle: ",img[8]
    print "top angle: ",img[9]
    return
    aMaxL = numpy.argmax(img, axis=1 );
    print "Image surrounding pixel values"
    delta=10
    for i in xrange(0,len(img)):
        middleI=aMaxL[i]
        leftI=max(0,middleI-delta)
        rightI=min(middleI+delta,len(img)-1)
        #print "indexes: ",leftI," ",middleI," ",rightI 
        print img[6][i]
        #print img[i][leftI:rightI]
    print len(img)
    print len(img[0])
    #for i in xrange(0,len(img)):

        

def showImg(imgArray):
    print "pi 1"
    im=Image.fromstring("RGB",(imgArray[0],imgArray[1]),imgArray[6])
    print "pi 2"
    im.save("camImg.png","PNG")
    print "pi 3"
    im.show()
    print "pi 4"
    exit(0)

def detectLine( img, bVerbose = False ):
    """
    detect a line in an image
    Return [rOffset, rOrientation]
    - rOffset: rough position of the line on screen [-1, +1] (-1: on the extrem left, 1: on the extrem right, 0: centered)
    - rOrientation: its orientation [-pi/2,pi/2]
    or [None,None], if no line detected
    """
    nWidth = img.shape[1];
    nHeight = img.shape[0];

    # filter to detect vertical line
    kernel = -numpy.ones((1,3), dtype=numpy.float);
    kernel[0,1] = 2;

    img = cv2.filter2D(img, -1, kernel);

    #if (bVerbose):
    #    printImageData(img)


    # thresholding to remove low differential
    retval, img = cv2.threshold( img, 45, 255, cv2.THRESH_TOZERO );

    


    aMaxL = numpy.argmax(img, axis=1 );


    # we will no try to move all the points:
    if(transform):
        shiftedList=[]
        for i in xrange(0,len(aMaxL)):
            if(i==0):

                shiftedList.append(i)
            else:
                shiftedList.append(i+addList[i])

        aMaxL= numpy.array(shiftedList)

    print "\naMaxL\n",aMaxL
    aMaxLWithoutZeros = aMaxL[aMaxL>0];
    print "\naMaxLWithoutZeros\n",aMaxLWithoutZeros
    if( bVerbose ):
        print( "Line Length: %s" % len(aMaxLWithoutZeros) );

    if( len( aMaxLWithoutZeros ) < 4 ):
        print( "WRN: abcdk.image.detectLine: detected line is very short: %s" % aMaxLWithoutZeros );
        return [None, None];

    aNonZeroIdx = numpy.where(aMaxL != 0)[0]; # here we retravelling thru the list, it's not optimal (TODO: optimise!)
    nFirstNonZero = aNonZeroIdx[0];
    nLastNonZero = aNonZeroIdx[-1];
    nHeightSampling = nLastNonZero - nFirstNonZero;

    if( bVerbose ):
        print( "nFirstNonZero: %s" % nFirstNonZero );
        print( "nLastNonZero: %s" % nLastNonZero );
        print( "nHeightSampling: %s" % nHeightSampling );
        print( "nHeight: %s" % nHeight );
        print( "nWidth: %s" % nWidth );

    # here instead of take the average of left and right border, we just keep left, sorry for the approximation
    aLine = aMaxLWithoutZeros;

    # averaging
    nSamplingSize = max( min(len(aLine) / 40, 8), 1 );
    if( bVerbose ):
        print( "nSamplingSize: %s" % nSamplingSize );
    rTop = numpy.average(aLine[:nSamplingSize]); # first points
    rMed =  numpy.average(aLine[len(aLine)/2:len(aLine)/2+nSamplingSize]);
    rBase = numpy.average(aLine[-nSamplingSize:]); # last points

    # this computation is very approximative: we just take the top and bottom position and we compute an average direction (we should make a linear regression or...)
    rOrientation = ((rTop-rBase))/nHeightSampling; # WRN: here it could be wrong as the aLine has zero removed, so perhaps the top and bottom are not really at top or bottom !

    if( bVerbose ):
        print( "rOrientation rough: %s" % rOrientation );
        print rTop," ",rMed," ",rBase
        print( "rBase: %f, rMed: %f, rTop: %f, rOrientation: %f" % (rBase, rMed, rTop, rOrientation) );

    return( [(rMed/nWidth)*2-1, rOrientation] );
# detectLine - end


def rotateImage(image, angle):
    #print "calling empty method rotateImage"
    #return image
    #currently not usable
    print "turning angle: ",angle
    col = image.shape[1];
    row = image.shape[0];
    #row,col = image.shape
    center=tuple(numpy.array([row,col])/2)
    rot_mat = cv2.getRotationMatrix2D(center,angle,1.0)
    new_image = cv2.warpAffine(image, rot_mat, (col,row))
    return new_image


class LineFinder():
    """ THE line detector in a box without any external library """
    def __init__(self):
        myBroker = ALBroker("myBroker","0.0.0.0",0,IP,PORT)
        self.name="LineFinder"
        #self.kCameraSelectID = 18
        #self.cameraModule = ALProxy( "ALVideoDevice" )
        #self.cameraModule.setParam( self.kCameraSelectID, 1 )

    def setHeadPitch(self):
        self.motionProxy.angleInterpolationWithSpeed( "Head", [headRadAngle, 0.3500 ], 0.1 )

    def onLoad(self):
        self.bMustStop = False;
        self.bIsRunning = False;

    def onUnload(self):
        self.onInput_onStop(); # stop current loop execution

    def connectToMotion(self):
        try:
            self.motionProxy = ALProxy("ALMotion")
            pNames = "Head"
            pStiffnessLists = 1.0
            pTimeLists = 1.0
            self.motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e

    def connectToCamera( self ):
        try:
            self.avd = ALProxy( "ALVideoDevice" );
            strMyClientName = self.name;
            nCameraNum = 1;
            nResolution = 1;
            nColorspace = 0;
            nFps = 5;
            #self.strMyClientName=self.avd.subscribe("python_client",nResolution,nColorspace,nFps)
            self.strMyClientName = self.avd.subscribeCamera( strMyClientName, nCameraNum, nResolution, nColorspace, nFps );
        except BaseException, err:
            print( "ERR: connectToCamera: catching error: %s!" % err );

    def disconnectFromCamera( self ):
        try:
            self.avd.unsubscribe( self.strMyClientName );
        except BaseException, err:
            print ( "ERR: disconnectFromCamera: catching error: %s!" % err );

    def getImageFromCamera( self ):
        """
        return the image from camera or None on error
        """
        try:
            dataImage = self.avd.getImageRemote( self.strMyClientName )
            



            #print "showing raw image"
            #print dataImage[6]
            #showImg(dataImage)

            if( dataImage != None ):
                printImageData(dataImage)
                image = (numpy.reshape(numpy.frombuffer(dataImage[6], dtype='%iuint8' % dataImage[2]), (dataImage[1], dataImage[0], dataImage[2])))
                return image;

        except BaseException, err:
            print( "ERR: getImageFromCamera: catching error: %s!" % err );
        return None;


    def onInput_onStart(self):

        print( self.name + ": start - begin" );

        if( self.bIsRunning ):
            print ( self.name + ": already started => nothing" );
            return;

        self.bIsRunning = True;
        self.bMustStop = False;

        # camera connection
        self.connectToCamera()

        # bow your head robot!

        self.connectToMotion()
        self.setHeadPitch()


        while( not self.bMustStop ):
            timeBegin = time.time();
            img = self.getImageFromCamera();

            


            #stopping after one itteration now
            self.onInput_onStop()


            timeImg = time.time();
            if( img == None ):
                print( "ERR: error while getting image from camera: img is none" );
                #abcdk.debug.raiseCameraFailure();
            else:
                #flip the image acc to head orientation:
                print "imgDimPrev: ",len(img)
                img=rotateImage(img, headDegAngle)
                print "rotated image Dim: ",len(img)
                rBase, rOrientation = detectLine( img, bVerbose );
                print( "detectLine takes: %5.3fs" % (time.time() - timeBegin ) );
                if( rBase == None ):
                    print "no line found"
                    #self.output_none();
                else:
                    print "found line"
                    print "TODO:should send data to walker"
                    #self.output_detected( [rBase, rOrientation] );
                    rT = -rOrientation/2.
                    rY = -rBase/1.;
                    print "rT: ",rT
                    print "rY: ",rY
            timeDetect = time.time();
            print ( "end of loop, time total: %5.3fs, time get image: %5.3fs, time detect: %5.3fs" % ((time.time()-timeBegin),(timeImg-timeBegin),(time.time()-timeImg) ) );

            time.sleep( rPeriod );
        # end while
        self.bIsRunning = False;
        self.disconnectFromCamera();
        #self.onStopped();
        print( self.name + ": start - end" );

    def onInput_onStop(self):
        self.bMustStop = True; # stop current loop execution

# Template_White - end
pass