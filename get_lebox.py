import getopt
import sys
import re
def main():
		getCmd()
	#try:
		if i == 1 :
			#try:
			GetBox_ligand()
			#except Exception:
			print """
 		Please check your command ! """
			PrintUsage()
		elif i == 2 :
			#try:
			GetBox_residue()
			#except Exception:
			print """
 		Please check your command ! """
			PrintUsage()
	#except Exception:
			#PrintUsage()


def getCmd():
	global i,inputfile,ligand,residue,chain,_id,extend,outputfile
	extend = 10
	chain = '.*?'
	_id = '.*?'
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
			_id = _id.split(' ')
			#print (_id)
		elif option in ['--extend','-e']:
			extend = value
		elif option in ['--output','-o']:
			outputfile = value


def GetBox_ligand():
	result = []
	#for item in _id:
	f = open(inputfile,'rb')
	lines = f.readlines()
	for line in lines:
		#print line
		#print item
		c = r'HETATM+.*?'+ligand+'.+'+chain+'.+'+_id[0]+'.+.*?'
		pattern = re.compile(c,re.UNICODE)
		result_h=pattern.findall(line.decode('utf-8'))
		#print len(result_h)
		for item in result_h:
			if len(item) > 0:
				result.append(item)
	#print(result)
	item_x = []
	item_y = []
	item_z = []
	for item in result :
        	item_s = str(item)
        	item_sp = item_s.split(' ')
        	item_sp = filter(lambda x : x, item_sp)
		#print(item_sp)
		if len(item_sp)==10:
        		item_x.append(float(item_sp[4]))
        		item_y.append(float(item_sp[5]))
        		item_z.append(float(item_sp[6]))
		elif len(item_sp) == 11:
			item_x.append(float(item_sp[5]))
                        item_y.append(float(item_sp[6]))
                        item_z.append(float(item_sp[7]))
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
	result = []
	for item in _id:
		#print item
		f = open(inputfile,'rb')
		lines = f.readlines()
		for line in  lines:
		#	print line
			c = r'ATOM+.*?.+'+chain+'.+'+residue+'.+'+item+'.+.*?'
		#print str(c)
        		#_str = line.read()
        		pattern = re.compile(c,re.UNICODE)
       			result_sh=pattern.findall(line.decode('utf-8'))
		#print len(result_sh)
			try :
				result.append(result_sh[0])
			except Exception:
				pass
			#f.seek(0)
       		#print(result)
	item_x = []
	item_y = []
	item_z = []
        for item in result :
                item_s = str(item)
                item_sp = item_s.split(' ')
                item_sp = filter(lambda x : x, item_sp)
		#print item_sp
		for num in _id :
			#print num
			if len(item_sp)==10 :
				if item_sp[4] == num:
                        		item_x.append(float(item_sp[5]))
                        		item_y.append(float(item_sp[6]))
                        		item_z.append(float(item_sp[7]))
					#print item_sp
                	elif len(item_sp) == 12:
				if item_sp[5] == num:
                        		item_x.append(float(item_sp[6]))
                        		item_y.append(float(item_sp[7]))
                        		item_z.append(float(item_sp[8]))
					#print item_sp
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
        ligandbox =forward+ str(xmax)+' '+str(xmin)+'\n'+str(ymax)+' '+str(ymin)+'\n'+str(zmax)+' '+str(zmin)+'\n'+backward
        data.write(ligandbox)
        data.close()



def PrintUsage():
	print   """
		Usage:
		Ligand-> .py -i <inputfile> -l <ligand name> -c <chain name> -e <extend size> -o <output name>
                                
		Residue-> .py -i <inputfile> -r <residue name> -c <atom name> -d <id>or<"id1 id2 id3 ..."> -e <extend size> -o <output name>
		"""


	
if __name__ == "__main__":
	main()	
