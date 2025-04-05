from math import log, ceil
import sys
import base32
try:
	from bitarray import bitarray
except ImportError:
	print """
	Bitarray module required.
	http://pypi.python.org/pypi/bitarray/
	"""
		  
HASH_BITS = 192
				
class HashBloom(object):
		@staticmethod
		def get_k(_n, _h):
				"""get_k(n, h), get largest possible k"""
				_k = HASH_BITS/_h
				while _k > 1:
						m = HashBloom.get_m(_n, _k)
						if m >> _h == 0:
								return _k
						_k -= 1
				return 1
				
		@staticmethod
		def get_m(_n, _k):
				"""get_m(n,k),   m = int(ceil((_n * _k) /log(2))),  return int(m+64-(m%64))"""
				m = int(ceil((_n * _k) /log(2)))
				return int(m+64-(m%64))
				
		def __init__(self, data=None):
				self.k = 0
				self.h = 0
				self.bitarray = bitarray(0)
				if data: self.add(data)
				
		def add(self, tth):
				"""add(tth), adds tth value to bloomfilter"""
				for i in range(0, self.k):
						self.bitarray[self._pos(tth, i)] = 1
						
		def __len__(self):
				return len(self.bitarray)
				
		def __str__(self):
				return self.bitarray.tostring()
		
		def __contains__(self, tth):
				"""__contains__(tth), check if tth exists in bloomfliter"""
				if len(self.bitarray) == 0:
						return False
				for i in range(0, self.k):
						if not self.bitarray[self._pos(tth, i)]:
								return False
				return True
						
		def reset(self, k, m, h):
				"""reset(k, m, h) , k, h, and resize bitarray to len(m)"""
				self.bitarray = bitarray(m*[0],endian=sys.byteorder)
				self.k = k
				self.h = h
				
		def dataReset(self, data, k, h):
				"""reset(data, k, h) , k, h, and resize bitarray to len(data) and set data to bitarray"""
				self.k = k
				self.h = h
				self.bitarray = bitarray(len(data)*8*[0],endian=sys.byteorder)
				
				for i in range(0, len(data)):
						for j in range(0,7):
								self.bitarray[i*8+j] = (((ord(data[i]) >> j) & 1) != 0)
				
		def match(self, tth):
				"""match(tth), same as __contains__"""
				return self.__contains__(tth)
				
				
		def _pos(self, tth, n):
				if (n+1)*self.h > HASH_BITS:
						return 0
				x=0
				start = n*self.h
				for i in range(0, self.h):
						bit = start+i
						byte = bit/ 8
						pos = bit % 8
						if ord(base32.fromBase32(str(tth))[byte]) & (1 << pos):
								x |= (1 << i)
				return x % len(self.bitarray)
		
		
		
		

def testBloomVectors(k, m, h, tths, ctrl):
		hb=HashBloom()
		hb.reset(k,m,h)
		for tth in tths:
				hb.add(tth)
		ok_ctrl = (ctrl == base32.toBase32(hb.bitarray.tostring()))
		ok_match = hb.match(tths[0])
		
		return ok_ctrl , ok_match
		
testvalues = (
(8, 1024, 24, ('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',), 'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
(8, 1024, 24, ('BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',), 'AEAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
(8, 1024, 24, ('QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',), 'AEAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
(8, 1024, 24, ('BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA','QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'), 'AEAQAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
(8, 1024, 24, ('UDRJ6EGCH3CGWIIU2V6CH7VLFN4N2PCZKSPTBQA',), 'AAAAAAAABAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQACAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAA'),
(2, 1024, 64, ('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',), 'AEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
(2, 1024, 64, ('BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',), 'AEAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
(2, 1024, 64, ('QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',), 'AEAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
(2, 1024, 64, ('BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA','QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',), 'AEAQAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
(2, 1024, 64, ('UDRJ6EGCH3CGWIIU2V6CH7VLFN4N2PCZKSPTBQA',), 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'),
)

def calculateProbability(k, n, m, h):
		return ((1.0 - (1.0 - 1.0 / m)**(k * n))**k)
		

if __name__ == '__main__':
		print "Preforming %d bloomfilter creation tests" % len(testvalues)
		for n,args in enumerate(testvalues):
				ok_ctrl, ok_match = testBloomVectors(*args) 
				print "%d of %d tests complete, bloom creation = %s, bloom match = %s" % (n+1, len(testvalues),str(ok_ctrl), str(ok_match))
		print   
		print 
		print "Calculating of probable false positives"
		
		print
		h=24
		kstr='[h=%d]\t\t|\t'%h
		print '-'*174
		for i in range(1,9):
				kstr += "[k=%d]\t|\t" % i
		print kstr
		print '-'*174
		for n in [500, 2500, 5000, 10000, 20*1000, 50*1000, 100*1000, 150*1000, 200*1000, 250*1000, 500*1000]:
				sep = ''
				if n < 99999:
						sep='\t'
				line = "[n=%d]%s\t|"%(n, sep)#+sep
				for k in range(1,9):
						m = HashBloom.get_m(n,k)
						p= calculateProbability(k, n, m, h)
						#line+= ("\t\t%.2f%%" % (100-p*100))
						line+= "\t%.5f%%\t|" % (p)
				print line
				print '-'*174
				
		print m/8