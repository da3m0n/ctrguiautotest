@echo off
rem SET tests=(test_GUI-1_Valid_Login_Firefox.py test_GUI-2_Invalid_Password_Firefox.py test_GUI-3_Invalid_Username_Firefox.py test_GUI-4_Invalid_Username_and_Password_Firefox.py test_GUI-5_Username_With_Special_Character_Firefox.py test_GUI-13_Help_Button_Firefox.py test_GUI-14_Saving_Current_Config_Firefox.py test_GUI-16_Software_Loading_Activity_Firefox.py test_GUI-17_Unsaved_Config_Changes_Firefox.py test_GUI-18_Connection_Status_Changes_Firefox.py test_GUI-20_Date_Time_Display_Firefox.py test_GUI-22_Device_Up_Time.py test_GUI-32_Device_Info_Display.py)
SET PYTHONPATH=D:\projects\ctrguiautotests\Lib\site-packages
SET tests=(test_GUI-18_Connection_Status_Changes_Firefox)
SET workingTests=D:\projects\ctrguiautotests\Firefox\Working
SET resultPath=d:\projects\ctrguiautotests\tests\Results
SET address=10.16.15.112
SET testPath=d:\projects\ctrguiautotests\tests\Firefox\Working\
xcopy /y %workingTests%\* %testPath%
for %%i in (%workingTests%\*) do c:\python27\python %%i %address% >> %resultPath%\%%~ni.txt 2>&1
rem for %%i in %tests% do echo  copy %resultPath%\%%i + %resultPath%\%%i2 %resultPath%\%%i
rem PAUSE

