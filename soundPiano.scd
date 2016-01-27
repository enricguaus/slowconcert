(
Server.default = Server.internal;
s = Server.default;
s.waitForBoot({
	SynthDef(\help_mdapiano, { |out=0, freq=440, gate=1|
		var son = MdaPiano.ar(freq, gate, release: 0.9, stereo: 0.3, sustain: 0);
		DetectSilence.ar(son, 0.01, doneAction:2);
		Out.ar(out, son * 0.1);
	}).add;

	n = NetAddr.new("127.0.0.1", 57120);    // create the NetAddr
	//OSCFunc.trace(true); // Turn posting on
	o = OSCresponderNode(nil, '/note', {|pt, pr, pmsg|
		q = pmsg[1].asFloat;
		x=Synth("help_mdapiano",[\freq, q.midicps]);
	}).add;
});
)

s.quit;
