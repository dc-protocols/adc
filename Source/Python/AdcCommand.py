import unicodedata

def escape(line):
	line = line.replace('\\', "\\")
	line = line.replace('\n', "\\n")
	line =line.replace(' ', '\s')
	return line
	
def unescape(line):
	line = line.replace('\\\\', "\\")
	line = line.replace('\\n', "\n")
	line =line.replace('\s', ' ')
	return line
	
class ParseError(Exception):
	pass
	
class AdcCommand(object):

	#Priorities
	PRIORITY_NORMAL = 0
	PRIORITY_LOW = 1
	PRIORITY_IGNORE = 2
	PRIORITY_HIGH = 3
	
	#Severities
	SEV_SUCSESS=0
	SEV_RECOVERABLE=1
	SEV_FATAL = 2
	
	#Codes
	SUCCESS = 0
	ERROR_GENERIC = 0
	ERROR_HUB_GENERIC = 10
	ERROR_HUB_FULL = 11
	ERROR_HUB_DISABLED = 12
	ERROR_LOGIN_GENERIC = 20
	ERROR_NICK_INVALID = 21
	ERROR_NICK_TAKEN = 22
	ERROR_BAD_PASSWORD = 23
	ERROR_CID_TAKEN = 24
	ERROR_COMMAND_ACCESS = 25
	ERROR_REGGED_ONLY = 26
	ERROR_INVALID_PID = 27
	ERROR_BANNED_GENERIC = 30
	ERROR_PERM_BANNED = 31
	ERROR_TEMP_BANNED = 32
	ERROR_PROTOCOL_GENERIC = 40
	ERROR_PROTOCOL_UNSUPPORTED = 41
	ERROR_CONNECT_FAILED = 42
	ERROR_INF_MISSING = 43
	ERROR_BAD_STATE = 44
	ERROR_FEATURE_MISSING = 45
	ERROR_BAD_IP = 46
	ERROR_NO_HUB_HASH = 47
	ERROR_TRANSFER_GENERIC = 50
	ERROR_FILE_NOT_AVAILABLE = 51
	ERROR_FILE_PART_NOT_AVAILABLE = 52
	ERROR_SLOTS_FULL = 53
	ERROR_NO_CLIENT_HASH = 54
	
	#Command names		
	CMD_MSG = 	'MSG'
	CMD_INF = 	'INF'
	CMD_SID = 	'SID'
	CMD_SUP = 	'SUP'
	CMD_STA = 	'STA'
	CMD_SCH = 	'SCH'
	CMD_RES = 	'RES'
	CMD_CTM = 	'CTM'
	CMD_RCM = 	'RCM'
	CMD_GPA = 	'GPA'
	CMD_PAS = 	'PAS'
	CMD_QUI = 	'QUI'
	CMD_GET = 	'GET'
	CMD_GFI = 	'GFI'
	CMD_SND = 	'SND'
	CMD_CMD = 	'CMD'

	#Command types
	
	TYPE_BROADCAST = 'B'
	TYPE_CLIENT = 'C'
	TYPE_DIRECT = 'D'
	TYPE_ECHO = 'E'
	TYPE_FEATURE = 'F'
	TYPE_INFO = 'I'
	TYPE_HUB = 'H'
	TYPE_UDP = 'U'
	ctypes = [TYPE_BROADCAST , TYPE_CLIENT , TYPE_DIRECT, TYPE_ECHO ,
	TYPE_FEATURE , TYPE_INFO  ,TYPE_HUB ,TYPE_UDP ]
	
	HUB_SID = 0xffffffff
	
	
	
	@staticmethod
	def parse(line, a=None):
		if not a:
			a = AdcCommand()

		if line.length() <4:
			
			raise ParseError('Command too short', line)
	
		params = line.split(' ')

		FCC = params.pop(0)
		if FCC.length() != 4:
			raise ParseError('Invalid fourcc')
			
		ctype = a.ctype = FCC[0]
		cmd = a.command = FCC[1:4]

		if ctype not in a.ctypes:
			raise ParseError('Unknown ctype ' +line)
			
		if ctype == a.TYPE_INFO:
			a.source = a.HUB_SID
			
		if ctype in (a.TYPE_BROADCAST,a.TYPE_DIRECT,a.TYPE_ECHO,a.TYPE_FEATURE, a.TYPE_UDP):
			sid = params.pop(0)
			if sid.length() != 4:
				raise ParseError('Invalid SID length %s' % sid)
			a.source = sid
			
		if ctype in (a.TYPE_DIRECT,a.TYPE_ECHO):
			sid = params.pop(0)
			if sid.length() != 4:  
				raise ParseError('Invalid SID length %s' % sid)
			a.target = sid
			
		if ctype == a.TYPE_FEATURE:
			a.features = params.pop(0)
			if len(a.features) != 5: 
				raise ParseError('Invalid feature length %s' % a.feature)
				
		if cmd == a.CMD_STA:
			xyy = params.pop(0)
			a.severity = int(xyy[0])
			a.code = int(xyy[1:2])
			
		for p in params:
			a.params.append(unescape(p))
			
		return a
	

	
	
	
	def __init__(self, *args, **kwargs):
		self.ctype = kwargs.get('ctype', '')
		self.command =kwargs.get('command', '')
		self.source = kwargs.get('source', '')
		self.target = kwargs.get('target','')
		self.severity = kwargs.get('severity', 0)
		self.code =  kwargs.get('code', 0)
		self.priority = kwargs.get('priority', 0)
		self.message =  kwargs.get('message', '')
		self.params =  kwargs.get('params', []) 
		self.features =  kwargs.get('features', '') 
		if len(args) == 1:
			AdcCommand.parse(QString(args[0]), self)
		if len(args) >= 2:
			self.ctype = args[1]
			self.command = args[0]
		if len(args) == 3:
			self.source = args[2]
			
	def setTo(self, sid):
		self.target = sid
		
	def getIndex(self, index):
		if len(self.params) >= index+1:
			return self.params[index]
			
	def getParam(self, key):
		for param in self.params:
			if param[:2] == key:
				return param[2:]	
				
	def getParameters(self):
		return list(self.params)
		
	def getType(self):
		return self.ctype
		
	def getCommand(self):
		return self.command
		
	def getBuffer(self):
		line = AdcCommand.toString(self, True)
		line +=chr(0x0a)
		
		return unicodedata.normalize('NFC', line)
		
	def getFCC(self):
		return self.ctype+self.command
		
	def addParam(self, param='',val =None):
		if val:
			self.params.append(param+val)
		else:
			self.params.append(param)
		return self
		
	def addParams(self, params):
		if params:
			self.params += params
		return self
		
	def delParam(self, key):
		for param in self.params:
			if param[:2] == key:
				self.params.removeAt(self.params.indexOf(param))
				return
		
	def toString(self, esc=False):
		ret = self.getFCC()
		if self.ctype in (self.TYPE_BROADCAST,self.TYPE_DIRECT,self.TYPE_ECHO,self.TYPE_FEATURE, self.TYPE_UDP):
			ret += ' ' + self.source
			
		if  self.ctype in (self.TYPE_DIRECT,self.TYPE_ECHO):
			ret += ' ' + self.target
			
		if self.ctype == self.TYPE_FEATURE:
			ret+= ' ' + self.features
			
		if self.ctype is self.TYPE_INFO:
			if self.command is self.CMD_STA:
				ret += ' '
				ret+= str(self.severity*100+self.code) if self.severity else '000'
					
		for p in self.params:
			ret += ' '
			if esc:
				ret += escape(p)
				
			else:
				ret += p
		return ret


if __name__ == '__main__':
	pass