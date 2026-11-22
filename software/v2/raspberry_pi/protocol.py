"""Strict parser and bounded stream framing for proposed LitterBuggy protocol v2."""
import json

MAX_LINE_BYTES=512
U32=0xffffffff
FIELDS={'v','type','fw','seq','ms','imu_raw','echo_us','distance_mm','flags'}
class ProtocolError(ValueError): pass

def integer(value,lo,hi,name):
    if type(value) is not int or not lo<=value<=hi:raise ProtocolError(f'{name}: expected integer {lo}..{hi}')
    return value

def parse_line(raw):
    if len(raw)>MAX_LINE_BYTES:raise ProtocolError('line exceeds 512 bytes including terminator')
    def unique(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise ProtocolError('duplicate JSON key: '+k)
            d[k]=v
        return d
    try:
        value=json.loads(raw.decode('utf-8'),object_pairs_hook=unique,parse_constant=lambda _: (_ for _ in ()).throw(ProtocolError('nonfinite JSON number')))
    except (ValueError,UnicodeError,RecursionError) as exc:raise ProtocolError(str(exc)) from exc
    if type(value) is not dict or set(value)!=FIELDS:raise ProtocolError('expected one telemetry object with exact v2 fields')
    integer(value['v'],2,2,'v')
    if value['type']!='telemetry':raise ProtocolError('wrong type')
    if type(value['fw']) is not str or not 1<=len(value['fw'])<=32 or not value['fw'].isascii() or not value['fw'].isprintable():raise ProtocolError('invalid firmware identifier')
    integer(value['seq'],0,U32,'seq');integer(value['ms'],0,U32,'ms');flags=integer(value['flags'],0,15,'flags')
    if flags&3==3 or flags&12==12:raise ProtocolError('disabled and failed flags are mutually exclusive per sensor')
    imu=value['imu_raw']
    if flags&3:
        if imu is not None:raise ProtocolError('IMU must be null when disabled/failed')
    else:
        if type(imu) is not list or len(imu)!=7:raise ProtocolError('IMU needs 7 raw registers')
        for n in imu:integer(n,-32768,32767,'imu raw')
    if flags&12:
        if value['echo_us'] is not None or value['distance_mm'] is not None:raise ProtocolError('range must be null when disabled/timeout')
    else:
        integer(value['echo_us'],1,25000,'echo_us');integer(value['distance_mm'],0,4288,'distance_mm')
        if abs(value['distance_mm']-value['echo_us']*.343/2)>1:raise ProtocolError('distance inconsistent with draft conversion')
    return value

class Framer:
    """Keep at most MAX_LINE_BYTES in memory, but account for every raw byte."""
    def __init__(self,offset=0):self.offset=offset;self.start=offset;self.count=0;self.buf=bytearray()
    def feed(self,chunk):
        for byte in chunk:
            self.count+=1;self.offset+=1
            if len(self.buf)<MAX_LINE_BYTES:self.buf.append(byte)
            if byte==10:
                yield self.start,self.count,bytes(self.buf),('overlong frame' if self.count>MAX_LINE_BYTES else None)
                self.start=self.offset;self.count=0;self.buf.clear()
    def finish(self):
        if not self.count:return []
        result=[(self.start,self.count,bytes(self.buf),'incomplete frame at session end')]
        self.start=self.offset;self.count=0;self.buf.clear();return result

class SequenceTracker:
    """Report discontinuities without claiming proof of an electrical reset."""
    def __init__(self):self.previous=None
    def observe(self,sample):
        old=self.previous;self.previous=sample
        if old is None:return None
        delta=(sample['seq']-old['seq'])&U32
        elapsed=(sample['ms']-old['ms'])&U32
        if elapsed>=0x80000000 or delta>=0x80000000:return 'reset_or_out_of_order'
        if delta==0:return 'duplicate_sequence'
        if delta>1:return f'sequence_gap:{delta-1}'
        return None
