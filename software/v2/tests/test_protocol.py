import json
import pytest
from protocol import parse_line,ProtocolError,Framer,SequenceTracker,U32

def sample(**kw):
    d=dict(v=2,type='telemetry',fw='v2-r0',seq=0,ms=100,imu_raw=None,echo_us=None,distance_mm=None,flags=5);d.update(kw);return d
def encoded(**kw):return (json.dumps(sample(**kw))+'\r\n').encode()

def test_disabled_and_real_shape():
    assert parse_line(encoded())['imu_raw'] is None
    assert parse_line(encoded(flags=0,imu_raw=[0,0,16384,0,0,0,0],echo_us=1000,distance_mm=172))['distance_mm']==172

@pytest.mark.parametrize('raw',[b'null',b'[]',b'{}',b'{',b'\xff',b'0',b'NaN',b'{"v":2,"v":2}',encoded(seq=True),encoded(ms=-1),encoded(seq=2**32),encoded(v=1),encoded(fw=''),encoded(flags=3),encoded(flags=12),encoded(flags=0),encoded(imu_raw=[1]*7),encoded(flags=4,imu_raw=[0]*6),encoded(flags=4,imu_raw=[32768]*7),encoded(flags=1,echo_us=1000,distance_mm=1),encoded(distance_mm=0),b'x'*513])
def test_rejects_malformed_or_false_measurements(raw):
    with pytest.raises(ProtocolError):parse_line(raw)

def test_framing_chunk_boundaries_and_raw_offsets():
    data=encoded()+encoded(seq=1);framer=Framer(7);entries=[]
    for b in data:entries.extend(framer.feed(bytes([b])))
    assert len(entries)==2 and entries[0][0]==7
    assert entries[1][0]==7+len(encoded())
    assert parse_line(entries[1][2])['seq']==1
    assert framer.finish()==[]

def test_overlong_and_incomplete_frames_recover():
    f=Framer();out=list(f.feed(b'x'*10000+b'\n'+encoded()+b'partial'))
    assert out[0][1]==10001 and len(out[0][2])<=512 and out[0][3]=='overlong frame'
    assert parse_line(out[1][2])['v']==2
    assert f.finish()[0][3].startswith('incomplete')

def test_sequence_gap_reset_duplicate_and_rollovers():
    t=SequenceTracker();assert t.observe(sample(seq=U32,ms=U32-10)) is None
    assert t.observe(sample(seq=0,ms=90)) is None
    assert t.observe(sample(seq=3,ms=390))=='sequence_gap:2'
    assert t.observe(sample(seq=3,ms=490))=='duplicate_sequence'
    assert t.observe(sample(seq=0,ms=100))=='reset_or_out_of_order'
