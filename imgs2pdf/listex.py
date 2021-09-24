
def list_output(a): 
    print("Answers:\n")
    for b in a:
        ext=""
        if(b[0]%2==0):
            an=""
        else:
            an="`"
        if(len(str(b[0]))==1):
            ext=" "
        try:
            vasat=str(int(float(b[2])))
        except:
            vasat=str(b[2])
        print(ext+an+"✦Q"+str(b[0])+":"+vasat+an+ext,end=" ")
        
        if(b[0]%5==0):
            print("\n")