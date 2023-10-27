import json
def parse_input_data(text_data):
    data={}
    k=0
    i=0
    while i < len(text_data):
        if text_data[i]=='[':
            s=[]
            st=""
            f=0
            while len(s) or f==0:
                st+=text_data[i]
                f=1
                  #  print(st)
                if text_data[i]=='[':
                    s.append('[')
                elif text_data[i]==']':
                    s.pop()
                i+=1
            data[k]=json.loads(st)

            k+=1
        else:
            i+=1
                
            
                    
    jsonlist=[]
    for key,val in data.items():
        for data in val:
            jsonlist.append(data)
    return jsonlist