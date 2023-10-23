
from datetime import datetime

class ProgressBar:

    def __init__ ( self, prefix, width=50 ):
        self.prefix = prefix
        self.width = width
        self.num_phases = 1
        self._current_phase = 0
        self.num_steps = 100
        self._current_step = 0
        self.start( show=False )
        self.callback = None
    
    def start ( self, show=True ):
        self._start_time = datetime.now()
    
    def end ( self ):
        self._current_phase = self.num_phases
        self._current_step = 0
        self.update()
        print()

    def set_phase ( self, phase, num_phases ):
        self._current_phase = phase
        self._current_step = 0
        self.num_phases = num_phases
        self.update()
    
    def set_step ( self, step, num_steps ):
        self._current_step = step
        self.num_steps = num_steps
        self.update()
    
    def step ( self ):
        self.set_step( self._current_step + 1, self.num_steps )
    
    def update ( self, show=True ):
        self._current_time = datetime.now()
        if show:
            self.print()
    
    def print ( self ):
        step_proportion = self._current_step / self.num_steps
        phase_proportion = self._current_phase / self.num_phases
        proportion = phase_proportion + step_proportion / self.num_phases
        elapsed = self._current_time - self._start_time
        if proportion > 0:
            remaining = elapsed * ( 1 - proportion ) / proportion
            remaining_str = str( remaining )[2:7]
        else:
            remaining = None
            remaining_str = '...'
        elapsed_str = str( elapsed )[2:7]
        if self.callback is not None:
            self.callback( proportion, elapsed, remaining, elapsed_str, remaining_str )
        bars = int( self.width * proportion )
        blanks = self.width - bars
        print( f'{self.prefix} {"#"*bars}{"_"*blanks} {proportion*100:3.0f}% {elapsed_str} / {remaining_str}', end='\r' )
