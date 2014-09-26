#--------------------------------------------------------------------
#Administration Details
#--------------------------------------------------------------------
__author__ = "Mats Larsen"
__copyright__ = "Mats Larsen 2014"
__credits__ = ["Morten Lind"]
__license__ = "GPL"
__maintainer__ = "Mats Larsen"
__email__ = "larsen.mats.87@gmail.com"
__status__ = "Development"
__description__ = "Module is for logging data, it is generic. Meaning that the data will be stored into a text file. The purpose is get a better understand of the given logged data."
__file__ = "log_data.py"
__class__ ="LogData"
__dependencies__ = ["DisplayMsg"]
#--------------------------------------------------------------------
#File: ft_sensor.py
#Module Description
"""
This module handle the force/torque sensor independet of the connector.
Choose of typeconnector and streamming type and sampling periode
"""
#--------------------------------------------------------------------
#IMPORT
#--------------------------------------------------------------------
import traceback
import time
import threading

#--------------------------------------------------------------------
#CONSTANTS
#--------------------------------------------------------------------
LOG_LEVEL = 2 # Information level
ATI_DEVICE = '192.168.0.74'
LOCAL_HOST = '127.0.0.1'
ATI_PORT = 49152
NAME = 'TIMERMANAGER'
#--------------------------------------------------------------------
#METHODS
#--------------------------------------------------------------------
def log(msg, log_level=LOG_LEVEL):
    """
    Print a message, and track, where the log is invoked
    Input:
    -msg: message to be printed, ''
    -log_level: informationlevel, i
    """
    global LOG_LEVEL
    if log_level <= LOG_LEVEL:
        print(str(log_level) + ' : timermanager.py::' +
              traceback.extract_stack()[-2][2] + ' : ' + msg)

class TimerManager(threading.Thread):
    def __init__(self, name='1',
                 sampling_Freq=200,
                 log_level=2):
        self._name = NAME + '#' + name
        self._sampling_Freq = sampling_Freq
        self._log_level = log_level
        #Event
        self._thread_alive = threading.Event() # status for the thread
        self._thread_alive.clear()
        self._thread_terminated = threading.Event() # status for the thread
        self._thread_terminated.clear()
        #threading
        threading.Thread.__init__(self) # initialize th
        self.daemon = True
        self._timer_condition = threading.Condition()
    def get_name(self):
        """Returning the name."""
        return self._name
    name = property(get_name, 'Name Property')
    
    def run(self):
        log('Timermanager is RUNNING',self._log_level)
        self._thread_alive.set()
        self._thread_terminated.clear()
        while self._thread_alive.isSet():
            time.sleep(1.0/self._sampling_Freq)
            self._timer_condition.acquire()
            self._timer_condition.notifyAll()
            self._timer_condition.release()
        self._thread_alive.clear()
        self._thread_terminated.set()
        log(self._name + ' is terminated')
    def stop(self):
        """Stopping the thread."""
        log('Trying to stop "' + self._name + ' ".', self._log_level)
        self._thread_alive.clear()
    def wait_for_timer(self):
        self._timer_condition.acquire()
        self._timer_condition.wait()
        self._timer_condition.release()

    def get_alive(self):
        """Property return if the thread is alive or not.
        Output: true = alive, false = stopped."""
        return self._thread_alive.isSet()
    alive = property(get_alive, "Is the thread alive")

    def wait_startup(self,timeout=None):
        """Wait to this thread is started up, expect
        if a timeout is given.
        Inputs:
        timeout:float-> timeout given in secs."""
        if self._thread_alive.wait(timeout):
            return True
        else:
            return False

    def wait_teminated(self,timeout=None):
        """Wait to this thread is terminated, expect
        if a timeout is given.
        Inputs:
        timeout:float-> timeout given in secs."""
        self.stop()
        if self._thread_terminated.wait(timeout):

            return True
        else:
            return False
