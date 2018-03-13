import obspy
from dateutil.relativedelta import relativedelta
import datetime
import sys

INTERVAL = relativedelta(months=+1)
dir = '/lfs/1/krong/ConvNetQuake/diablo/stream/'
fname_format = 'PG.DCD..%s__%sT000000Z__%sT000000Z.mseed'
channels = ['EHE', 'EHN', 'EHZ']

def construct_filename(channel, t):
	return dir + fname_format % (channel, t.strftime('%Y%m%d'), 
		(t + INTERVAL).strftime('%Y%m%d'))

if __name__ == '__main__':
	start_time = datetime.datetime.strptime(sys.argv[1], "%y-%m")
	end_time = datetime.datetime.strptime(sys.argv[2], "%y-%m")

	t = start_time
	while t <= end_time:
		print t
		t1 = obspy.read(construct_filename(channels[0], t))
		t2 = obspy.read(construct_filename(channels[1], t))
		t3 = obspy.read(construct_filename(channels[2], t))
		st = t1 + t2 + t3
		st.write('%sPG.DCD.%s.mseed' % (dir, t.strftime('%Y%m')), format='MSEED')
		t += INTERVAL