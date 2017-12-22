
from ROOT import *
from array import array;

Error = 0;
z = array( 'f', ( 1., 0.96, 0.89, 0.85, 0.78 ) )
errorz = array( 'f', 5*[0.01] )

x = array( 'f', ( 1.5751, 1.5825,  1.6069,  1.6339,   1.6706  ) )
y = array( 'f', ( 1.0642, 0.97685, 1.13168, 1.128654, 1.44016 ) )

ncount = 0

##______________________________________________________________________________
def testfit():

    
    gMinuit = TMinuit(5)
    gMinuit.SetFCN(fcn)
    gMinuit.SetErrorDef(1)
    # non ha molta importanza, visto che l'errore sui parametri della net non sara' comunque
    # considerato
    
# Set starting values and step sizes for parameters
    gMinuit.DefineParameter( 0, "a1", 3,      0.1,0,0)
    gMinuit.DefineParameter( 1, "a2", 1,      0.1,0,0)
    gMinuit.DefineParameter( 2, "a3", 0.1,   0.01,0,0)
    gMinuit.DefineParameter( 3, "a4", 0.01, 0.001,0,0)

 # Now ready for minimization step
    gMinuit.Migrad()

 # Print results
    par,err = Double(0),Double(0)
    gMinuit.GetParameter(0,par,err)
    print par

    par = Double(0)
    funclass("TMVATest.root","TreeS",par)
    return


##______________________________________________________________________________
def fcn( npar, gin, f, par, iflag ):
    global ncount
    nbins = 5
    
# calculate chisquare
    chisq, delta = 0., 0.
    for i in range(nbins):
        delta  = (z[i]-func(x[i],y[i],par))/errorz[i]
        chisq += delta*delta
    
    f[0] = chisq
    ncount += 1

def func( x, y, par ):
    value = ( (par[0]*par[0])/(x*x)-1)/ ( par[1]+par[2]*y-par[3]*y*y)
    return value

def funclass(fname,tname,par):
    rootfile = TFile.Open(fname,'read')
    tree     = TTree()
    rootfile.ls()
    rootfile.GetObject(tname,tree)

    tree.Print()
    for event in tree:
      print event.Len
      var = [event.Len, event.IP_B1, event.IP_B2, event.IP_A, event.Pt, event.MinDist]
      print teststat(var,par)

# vettore parametri 
def teststat(var,par):
    return 1;


##______________________________________________________________________________
if __name__ == '__main__':
   testfit()
