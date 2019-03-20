import time

# This code is inspired by fluent wait concept in Selenium Webdriver
# Reference code: https://github.com/browserstack/selenium-webdriver-python/edit/master/selenium/webdriver/support/wait.py
# However, rather than a Selnium WebDriver specific and driver level concept,
# Setu aims to make it a more generic concept available beyond WebDriver and GUI automation.
# Setu makes waiting accessible through a condition rather than the other way round.
# i.e. object.condition(args).wait(), rather than wait(driver).condition(args)

class ConditionException(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class DynamicCaller:

    def __init__(self, kallable, *args, **kwargs):
        self.__kallable = kallable
        self.__args = args
        self.__kwargs = kwargs

    def call(self):
        return self.__kallable(*self.__args, **self.__kwargs)

class Condition:

    def __init__(self, dynamic_caller, *args, **kwargs):
        self.__dynamic_caller = dynamic_caller
        self.__args = args
        self.__kwargs = kwargs
        self.__call_result = None

    def get_call_result(self):
        return self.__call_result

    def wait(self, *, max_wait_time=60, poll_interval=0.5):
        end_time = time.time() + max_wait_time
        while(True):
            try:
                if self.is_met():
                    return self.get_call_result()
            except ConditionException as ce:
                raise ce
            except Exception as f:
                print(f)
                import traceback
                traceback.print_exc()
                pass
            time.sleep(poll_interval)
            if(time.time() > end_time):
                break
        raise Exception("Timeout in wait.")

    def execute(self):
        self.__call_result = self.__dynamic_caller.call(*self.__args, **self.__kwargs)

class CommandCondition(Condition):

    def __init__(self, dynamic_caller, returns_none=True):
        super().__init__(dynamic_caller)
        self.__returns_none = returns_none

    def is_met(self):
        self.execute()
        if self.__returns_none: return True
        return self.get_call_result() is not None

class BooleanCondition(Condition):

    def __init__(self, dynamic_caller, expectation_type=True):
        super().__init__(dynamic_caller)
        self.__expectation_type = expectation_type

    def is_met(self):
        try:
            self.execute()
            return self.__expectation_type == self.get_call_result()
        except Exception as e:
            print(e)
            import traceback
            traceback.print_exc()
            raise ConditionException("Unexpected exception in boolean condition checking: " + str(e))