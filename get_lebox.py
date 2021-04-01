import getopt
import sys
import re
def main():
	getCmd()
	try:
		if i == 1 :
			try:
				GetBox_ligand()
			except Exception:
				print """
 		Please check your command ! """
				PrintUsage()
		elif i == 2 :
			try:
				GetBox_residue()
			except Exception:
				print """
 		Please check your command ! """
				PrintUsage()
	except Exception:
			PrintUsage()


def getCmd():
	global i,inputfile,ligand,residue,chain,_id,extend,outputfile
	extend = 10
	oprts,args=getopt.getopt(sys.argv[1:],'ho:e:d:c:r:l:i:',
				[
					'input=',
					'ligand=',
					'residue=',
					'chain=',
					'_id=',
					'extend=',
					'output=',
				]
				)
	for option,value in oprts:
		if option in ['--help','-h']:
			i = 0
			PrintUsage()
		elif option in ['--input','-i']:
			inputfile = value
		elif option in ['--ligand','-l']:
			ligand = value
			i = 1
		elif option in ['--residue','-r']:
			residue = value
			i = 2
		elif option in ['--chain','-c']:
			chain = value
		elif option in ['--_id','-d']:
			_id = value
		elif option in ['--extend','-e']:
			extend = value
		elif option in ['--output','-o']:
			outputfile = value


def GetBox_ligand():
	f = open(inputfile,'rb')
	c = r'ATOM.+'+ligand+'.+'+chain+'.+[0-9]+\.?[0-9]*.+.*?'
	_str = f.read()
	pattern = re.compile(c,re.UNICODE)
	result = pattern.findall(_str.decode('utf-8'))
	#print(result[0])
	item_x = []
	item_y = []
	item_z = []
	for item in result :
        	item_s = str(item)
        	item_sp = item_s.split(' ')
        	item_sp = filter(lambda x : x, item_sp)
        	item_x.append(float(item_sp[6]))
        	item_y.append(float(item_sp[7]))
        	item_z.append(float(item_sp[8]))
	item_x.sort()
	xmax = item_x[len(item_x)-1]+float(extend)
	xmin = item_x[0]-float(extend)

	item_y.sort()
	ymax = item_y[len(item_y)-1]+float(extend)
	ymin = item_y[0]-float(extend)

	item_z.sort()
	zmax = item_z[len(item_z)-1]+float(extend)
	zmin = item_z[0]-float(extend)	
	data = open(outputfile,"w")
	forward = 'Receptor\npro.pdb\n\nRMSD\n1.0\n\nBinding pocket\n'
	backward = 'Number of binding poses\n20\n\nLigands list\nligands\n\nEND'
	ligandbox =forward+ str(xmax)+' '+str(xmin)+'\n'+str(ymax)+' '+str(ymin)+'\n'+str(zmax)+' '+str(zmin)+'\n\n'+backward
	data.write(ligandbox)
	data.close()



def GetBox_residue():
	f = open(inputfile,'rb')
	c = r'ATOM     +'+_id+'.+'+residue+'.+'+chain+'.+.*?'
        _str = f.read()
        pattern = re.compile(c,re.UNICODE)
        result = pattern.findall(_str.decode('utf-8'))
        #print(result[0])
        for item in result :
                item_s = str(item)
                item_sp = item_s.split(' ')
                item_sp = filter(lambda x : x, item_sp)
                item_x = float(item_sp[6])
                item_y = float(item_sp[7])
                item_z = float(item_sp[8])
	xmax = item_x + float(extend)
	xmin = item_x - float(extend)
	ymax = item_y + float(extend)
	ymin = item_y - float(extend)
	zmax = item_z + float(extend)
	zmin = item_z - float(extend)
	data = open(outputfile,"w")
	forward = 'Receptor\npro.pdb\n\nRMSD\n1.0\n\nBinding pocket\n'
	backward = 'Number of binding poses\n20\n\nLigands list\nligands\n\nEND'
        ligandbox =forward+ str(xmax)+' '+str(xmin)+'\n'+str(ymax)+' '+str(ymin)+'\n'+str(zmax)+' '+str(zmin)+'\n'+backward
        data.write(ligandbox)
        data.close()



def PrintUsage():
	print   """
		Usage:
		Ligand-> .py -i <inputfile> -l <ligand name> -c <chain name> -e <extend size> -o <output name>
                                
		Residue-> .py -i <inputfile> -r <residue name> -d <id> -c <chain name> -e <extend size> -o <output name>
		"""


	
if __name__ == "__main__":
	main()	
