from string import Template

"""
Take templatefile which is templated as $IMP
replace all occurances of $IMP with value 
writes it to outputfile
"""
def write_inp(templatefile, outputfile, value):
    with open(templatefile,'r') as inf:
        tmp=inf.read()
        t=Template(tmp)
        outs=t.substitute({'IMP': value})
        with open(outputfile,'w') as ouf:
            ouf.write(outs)

if __name__=="__main__":
    import swmm_call as sc
    templatefile="./data/swmm5Example.inp_"
    outputfile="./output/myinpfile.inp"
    write_inp(templatefile, outputfile, 40)
    mv=sc.get_max_flow(outputfile, "T5")
    print(mv)