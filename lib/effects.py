from _core import *

######################################################################
### Effects
######################################################################                                       
class Biquad(PyoObject):
    """
    A sweepable general purpose biquadratic digital filter. 
    
    **Parameters**
    
    input : PyoObject
        Input signal to filter.
    freq : float or PyoObject, optional
        Cutoff or center frequency of the filter. Default to 1000.
    q : float or PyoObject, optional
        Q of the filter, defined, for bandpass filters, as bandwidth/cutoff. Should be between 1 and 500. Default to 1.
    type : int, optional
        Filter type. Four possible values :
            0 = lowpass (default)
            1 = highpass
            2 = bandpass
            3 = bandstop

    **Methods**

    setInput(x, fadetime) : Replace the `input` attribute.
    setFreq(x) : Replace the `freq` attribute.
    setQ(x) : Replace the `q` attribute.
    setType(x) : Replace the `type` attribute.

    """
    def __init__(self, input, freq=1000, q=1, type=0, mul=1, add=0):
        self._input = input
        self._freq = freq
        self._q = q
        self._type = type
        self._mul = mul
        self._add = add
        self._in_fader = InputFader(input)
        in_fader, freq, q, type, mul, add, lmax = convertArgsToLists(self._in_fader, freq, q, type, mul, add)
        self._base_objs = [Biquad_base(wrap(in_fader,i), wrap(freq,i), wrap(q,i), wrap(type,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        **Parameters**

        x : PyoObject
            New signal to process.
        fadetime : float, optional
            Crossfade time between old and new input. Default to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)
        
    def setFreq(self, x):
        """
        Replace the `freq` attribute.
        
        **Parameters**

        x : float or PyoObject
            New `freq` attribute.

        """
        self._freq = x
        x, lmax = convertArgsToLists(x)
        [obj.setFreq(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setQ(self, x):
        """
        Replace the `q` attribute. Should be between 1 and 500.
        
        **Parameters**

        x : float or PyoObject
            New `q` attribute.

        """
        self.q = x
        x, lmax = convertArgsToLists(x)
        [obj.setQ(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setType(self, x):
        """
        Replace the `type` attribute.
        
        **Parameters**

        x : int
            New `type` attribute. 0 = lowpass, 1 = highpass, 2 = bandpass, 3 = bandstop.

        """
        self._type = x
        x, lmax = convertArgsToLists(x)
        [obj.setType(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    @property
    def input(self): return self._input
    @input.setter
    def input(self, x): self.setInput(x)
    @property
    def freq(self): return self._freq
    @freq.setter
    def freq(self, x): self.setFreq(x)
    @property
    def q(self): return self._q
    @q.setter
    def q(self, x): self.setQ(x)
    @property
    def type(self): return self._type
    @type.setter
    def type(self, x): self.setType(x)

class Disto(PyoObject):
    """
    Arctan distortion.
    
    Apply an arctan distortion on input signal with control on the drive. 
    
    **Parameters**
    
    input : PyoObject
        Input signal to process.
    drive : float or PyoObject, optional
        Amount of distortion applied on the signal, between 0 and 1. 
        Default to 0.75.
    slope : float or PyoObject, optional
        Slope of a lowpass filter applied after distortion, between 0 and 1. 
        Default to 0.5.

    **Methods**

    setInput(x, fadetime) : Replace the `input` attribute.
    setDrive(x) : Replace the `drive` attribute.
    setSlope(x) : Replace the `slope` attribute.

    """
    def __init__(self, input, drive=.75, slope=.5, mul=1, add=0):
        self._input = input
        self._drive = drive
        self._slope = slope
        self._mul = mul
        self._add = add
        self._in_fader = InputFader(input)
        in_fader, drive, slope, mul, add, lmax = convertArgsToLists(self._in_fader, drive, slope, mul, add)
        self._base_objs = [Disto_base(wrap(in_fader,i), wrap(drive,i), wrap(slope,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        **Parameters**

        x : PyoObject
            New signal to process.
        fadetime : float, optional
            Crossfade time between old and new input. Default to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)
 
    def setDrive(self, x):
        """
        Replace the `drive` attribute.
        
        **Parameters**

        x : float or PyoObject
            New `drive` attribute.

        """
        self._drive = x
        x, lmax = convertArgsToLists(x)
        [obj.setDrive(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setSlope(self, x):
        """
        Replace the `slope` attribute.
        
        **Parameters**

        x : float or PyoObject
            New `slope` attribute.

        """
        self._slope = x
        x, lmax = convertArgsToLists(x)
        [obj.setSlope(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    @property
    def input(self): return self._input
    @input.setter
    def input(self, x): self.setInput(x)
    @property
    def drive(self): return self._drive
    @drive.setter
    def drive(self, x): self.setDrive(x)
    @property
    def slope(self): return self._slope
    @slope.setter
    def slope(self, x): self.setSlope(x)

class Delay(PyoObject):
    """
    Sweepable recursive delay.
    
    **Parameters**
    
    input : PyoObject
        Input signal to delayed.
    delay : float or PyoObject, optional
        Delay time in seconds. Default to 0.25.
    feedback : float or PyoObject, optional
        Amount of output signal sent back into the delay line. Default to 0.
    maxdelay : float, optional
        Maximum delay length in seconds. Available only at initialisation. Default to 1.

    **Methods**

    setInput(x, fadetime) : Replace the `input` attribute.
    setDelay(x) : Replace the `delay` attribute.
    setFeedback(x) : Replace the `feedback` attribute.

    """
    def __init__(self, input, delay=0.25, feedback=0, maxdelay=1, mul=1, add=0):
        self._input = input
        self._delay = delay
        self._feedback = feedback
        self._mul = mul
        self._add = add
        self._in_fader = InputFader(input)
        in_fader, delay, feedback, maxdelay, mul, add, lmax = convertArgsToLists(self._in_fader, delay, feedback, maxdelay, mul, add)
        self._base_objs = [Delay_base(wrap(in_fader,i), wrap(delay,i), wrap(feedback,i), wrap(maxdelay,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]
        
    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        **Parameters**

        x : PyoObject
            New signal to process.
        fadetime : float, optional
            Crossfade time between old and new input. Default to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setDelay(self, x):
        """
        Replace the `delay` attribute.
        
        **Parameters**

        x : float or PyoObject
            New `delay` attribute.

        """
        self._delay = x
        x, lmax = convertArgsToLists(x)
        [obj.setDelay(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setFeedback(self, x):
        """
        Replace the `feedback` attribute.
        
        **Parameters**

        x : float or PyoObject
            New `feedback` attribute.

        """
        self._feedback = x
        x, lmax = convertArgsToLists(x)
        [obj.setFeedback(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    @property
    def input(self): return self._input
    @input.setter
    def input(self, x): self.setInput(x) 
    @property
    def delay(self): return self._delay
    @delay.setter
    def delay(self, x): self.setDelay(x)
    @property
    def feedback(self): return self._feedback
    @feedback.setter
    def feedback(self, x): self.setFeedback(x)