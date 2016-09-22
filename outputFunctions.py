#   Copyright (C) 2016 Francisco Favela

#   This file is part of isonav

#   isonav is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   isonav is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from isonavBase import *
import webbrowser

def pSReaction(iso1,iso2,isoEject,isoRes,ELab=2.9,ang=30):
    react1,react2=sReaction(iso1,iso2,isoEject,isoRes,ELab,ang)
    if not react1:
        print("Reaction is invalid")
        return 0

    fR1=react1[0][1:]
    sR1=react1[1][1:]#switching the ejectile and the residue
    if fR1[1] != False:
        stringFormat="%.3f\t"*(len(fR1)-1)+"%.3f"
        print(str(isoEject)+'\t'+str(isoRes))
        print(stringFormat % tuple(fR1))
        print("")
    #The second solution
    if react2 != []:
        fR2=react2[0][1:]
        sR2=react2[1][1:]
        if fR2[0] != False:
            if fR1[1] == False:
                print(str(isoEject)+'\t'+str(isoRes))

            stringFormat="%.3f\t"*(len(fR2)-1)+"%.3f"
            print(stringFormat % tuple(fR2))
            print("")

    if sR1:
        print(str(isoRes)+'\t'+str(isoEject))
        print(stringFormat % tuple(sR1))
        print("")
    if sR2 != []:
        stringFormat="%.3f\t"*(len(sR2)-1)+"%.3f"
        print(stringFormat % tuple(sR2))
        print("")

def pXReaction(isop,isot,isoE,isoR,Elab,angle,xF1,xF2):
    xReact=xReaction(isop,isot,isoE,isoR,Elab,angle,xF1,xF2)
    for e in xReact:
        print(str(e[0][0])+'\t'+str(e[0][1]))
        stringFormat="%d\t"+"%.3f\t\t"+"%.3f\t"*2+"%.3f"
        for ee in e[1]:
            level=ee[0][0]
            lE=ee[0][1]
            rest=ee[1][1:]
            tup=(level,lE, rest[0],rest[1],rest[2])
            print(stringFormat % tuple(tup))
        print("")
            
def pXXTremeTest(iso1,iso2,Elab,angle):
    XXList=xXTremeTest(iso1,iso2,Elab,angle)
    stringFormat="%d\t%0.3f\t\t"+"%.3f\t"*2+"%.3f"
    for e in XXList:
        isoE=e[0][0]
        isoR=e[0][1]
        EThres=e[0][2]
        QVal=e[0][3]
        tup=(isoE,isoR,EThres,QVal)
        reaction=e[1]
        for ee in reaction:
            if len(ee[1])>0:
                isoE=ee[0][0]
                isoR=ee[0][1]
                print(isoE+'\t'+isoR)
                for states in ee[1]:
                    level=states[0][0]
                    levE=states[0][1]
                    ejectE=states[1][1]
                    resAng=states[1][2]
                    resE=states[1][3]
                    tup=(level,levE,ejectE,resAng,resE)
                    print(stringFormat % tup)
                print("")

    
def pXTremeTest(iso1,iso2,Elab,angle):
    val=xTremeTest(iso1,iso2,Elab,angle)
    stringFormat="%.3f\t%.3f\t%.3f"
    stringFormat2="%s\t%s"
    for v in val:
        isoE=v[0][0]
        isoR=v[0][1]
        ejectE=v[1][0][1]
        resAng=v[1][0][2]
        resE=v[1][0][3]
        tup=(ejectE,resAng,resE)
        print(stringFormat2 %(isoE,isoR))
        print(stringFormat % tuple(tup))
        print("")
        # print("v = ",v)
        ejectE=v[1][1][1]
        resAng=v[1][1][2]
        resE=v[1][1][3]
        tup=(ejectE,resAng,resE)
        print(stringFormat2 %(isoR,isoE))
        print(stringFormat % tuple(tup))
        print("")


#Printing it nicely for a spreadsheet.
def tNReaction(iso1,iso2):
    rList=nReaction(iso1,iso2)
    for e in rList:
        if e[2]=='None':
            string1=str(e[0])+'\t'+str(e[1])+'\t'+str(e[2])+'\t'
            print(string1+"{0:0.2f}".format(float(e[3])))
        else:
            string2=e[0]+'\t'+e[1]+'\t'+"{0:0.2f}".format(float(e[2]))
            string3='\t'+"{0:0.2f}".format(float(e[3]))
            print(string2+string3)

##Printing latex fiendly nReaction
def latexNReaction(iso1,iso2):
    reacList=nReaction(iso1,iso2)
    a1,key1=getIso(iso1)
    a2,key2=getIso(iso2)
    sa1=str(a1)
    sa2=str(a2)
    print("""\\begin{eqnarray*} """)
    
    print(' ^{'+sa1+'}\mathrm{'+key1+'}+'+' ^{'+sa2+'}\mathrm{'+key2+'}\longrightarrow ')
    maxVal=len(reacList)
    for r in reacList:
        if r==reacList[3]:
            fStr='\\:\\rm{MeV}'
        else:
            fStr='\\:\\rm{MeV}\\\\'

        r[3]=str(round(r[3],2))
        aEject,kEject=getIso(r[0])
        aRes,kRes=getIso(r[1])
        aEject,aRes=str(aEject),str(aRes)
        if kEject==None:
            print(' ^{'+aRes+'}'+kRes+'&Q='+r[3]+fStr)
            continue

        print('& ^{'+aEject+'}\mathrm{'+kEject+'}+'+' ^{'+aRes+'}\mathrm{'+kRes+'}&Q='+r[3]+fStr)
    print('\end{eqnarray*}')

def pIsotopes(iso,mFlag=False,flag=True):
    val=getIsotopes(iso)
    eCoef=1
    if mFlag:
        if flag:
            eCoef=931.4941
        if val == False:
            print("Symbol not in database")
            return False
        for i in val:
            i[1]*=eCoef
            print(str(i[0])+"\t"+str(i[1]))
        return 0
    for i in val:
        print(i[0])
    return 0

def pDecay(iso,emit="",num=1):
    if emit == "":
        dec=QDecay(iso)
        for d in dec:
            print("%s\t%s\t\t%.3f\t%.3f\t%.3f" % tuple(d))
    else:
        dec=emitDecay2(iso,emit,num)
        if dec==None or dec==False:
            return 1
        print("%s\t%s\t\t%.3f" % tuple(dec))

def pDecay2(iso,emit,num=1):
    dec=emitDecay2(iso,emit,num)
    if dec==None or dec==False:
        return 1
    print("%s\t%s\t\t%.3f" % tuple(dec))

def pFussion(iso1,iso2,Elab):
    l=fussionCase(iso1,iso2,Elab)
    stringFormat="%s\t%d\t%.3f\t%.3f"
    print(stringFormat % tuple(l))

def pLevels(iso,limit="NaN"):
    levs=getAllLevels(iso)
    if limit=="NaN":
        for l in levs:
            print(str(l[0])+'\t'+str(l[1]))
        return 0
    counter=0
    for l in levs:
        counter+=1
        if counter > limit:
            break
        print(str(l[0])+'\t'+str(l[1]))
    return 0

def pDonation(flag=False):
    if flag==True:
        disp=webbrowser.open(isonavQR)
    print("1LgQ8NuSVxbLmuhVjh9kxpoacKPr7kt4s2")
    return 0

def pName(s):
    eName=getNameFromSymbol(s)
    if eName != False:
        print(eName)
