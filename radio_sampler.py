from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from osmosdr import source
from gnuradio import eng_notation

class top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        samp_rate = 2e6
        center_freq = 97.9e6  # Frequency of the station
        filename = "output.wav"  # Output file

        self.src = source(args="numchan=" + str(1) + " " + "")
        self.src.set_sample_rate(samp_rate)
        self.src.set_center_freq(center_freq, 0)
        self.src.set_freq_corr(0, 0)
        self.src.set_dc_offset_mode(0, 0)
        self.src.set_iq_balance_mode(0, 0)
        self.src.set_gain_mode(False, 0)
        self.src.set_gain(10, 0)
        self.src.set_if_gain(20, 0)
        self.src.set_bb_gain(20, 0)
        self.src.set_antenna("", 0)
        self.src.set_bandwidth(0, 0)

        self.audio_sink = audio.sink(44100, "", True)
        self.analog_wfm_rcv = analog.wfm_rcv(
            quad_rate=samp_rate,
            audio_decimation=10,
        )

        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((32767, ))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_short*1, filename, False)
        self.blocks_file_sink_0.set_unbuffered(False)

        self.connect(self.src, self.analog_wfm_rcv)
        self.connect(self.analog_wfm_rcv, self.blocks_multiply_const_vxx_0)
        self.connect(self.blocks_multiply_const_vxx_0, self.blocks_file_sink_0)

if __name__ == '__main__':
    tb = top_block()
    tb.start()
    tb.wait()