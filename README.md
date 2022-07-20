![](https://img.shields.io/badge/SDK-v13.0.0-blue) <Please check version is the same as specified in requirements.txt>

# Sample app parametric football stadium with Grasshopper
Use this open-source sample application to parametrically design a football stadium through an 
integration with grasshopper, without opening the grasshopper interface at all. 
The sample app provides a clear visualization of the stadium, and calculates the maximum number of seats. 
You can then also download the model as a gtb file

## Setting up:
When using this app with VIKTOR there are a few steps required to make this app work.
1. Make sure you have installed Rhino. In the example Rhino is installed at ``C:\Program Files\Rhino 7\System\Rhino.exe``, if your Rhino is installed somewhere else replace the path in [app/grasshopper/data/run_grasshopper.bat](app/grasshopper/data/run_grasshopper.bat).
2. Make sure your Rhino Settings for exporting .obj files are configured correctly. Do this in Rhino by exporting any geometry as .obj, and a dialog box will pop up where you can configure the export settings. Select the checkmark to save these settings.
3. Install a generic worker found on https://docs.viktor.ai/docs/worker. Make sure you select ``generic``
4. Copy the file found at [app/grasshopper/data/run_grasshopper.bat](app/grasshopper/data/run_grasshopper.bat) in the same folder where you just installed your worker. (probably at ``C:\Program Files\<username>\Viktor worker for generic v5.1.1\``)
5. Replace the config.yaml file in your worker folder with the file found at [app/grasshopper/data/config.yaml](app/grasshopper/data/config.yaml)
6. Inside the config.yaml file, replace ``    path: 'C:\Program Files\Viktor\Viktor worker for generic v5.1.1\run_grasshopper.bat'`` with the correct path top your run_grasshopper.bat file
7. Execute the ``viktor-worker-generic.exe`` file with admin rights

**Apply for a [demo account](https://www.viktor.ai/demo-environment) to get access to this and all other VIKTOR sample applications.**

![](manifest/pictures/stadium.png)
In this picture you can see how the app should look like. With on the left all the input parameters and the download button. In the middle there is a 3d view of the mesh. And on the right you can find all the info.

Use the [free version](https://www.viktor.ai/try-for-free) or apply for a [demo account](https://www.viktor.ai/try-for-free) to try the functionality yourself! 
