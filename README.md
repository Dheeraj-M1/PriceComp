# Installing Chromedriver to run Selenium

1. Download [ChromeDriver 107.0.5304](https://chromedriver.storage.googleapis.com/index.html?path=107.0.5304.62/)

2. Add Chrome Driver to your system path (below are instructions for windows machines)
3. Depending on your Windows version
    - If you’re using Windows 8 or 10, press the Windows key + `x` and select **System**
    - If you’re using Windows 7, right click the **Computer** icon on the desktop and click Properties
4. Click **Advanced system settings**
5. Click **Environment Variables**
6. Under **System Variables**, find the `PATH` variable, select it, and click **Edit**. If there is no `PATH` variable, click **New**
7. With `PATH` selected click **Edit**
8. In the **Edit environment variable** window click **New**
9. Copy and paste the folder path that holds the unzipped `chromedriver.exe` into the `PATH` variable (i.e. chromedriver.exe should not be in your pasted path)
10. Click **OK** on all the open windows
11. Check if its worked by open a windows command prompt/terminal and type `chromedriver -v`