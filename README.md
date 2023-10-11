# mcp-flight-software
Equivalent to scp_v4


# Install
Place install_and_run_mcp.py in ~/mcp/ and run this command \
```python ~/mcp/install_and_run_mcp.py```
\
You can also run this command to delete everything and start fresh \
```python ~/mcp/install_and_run_mcp.py --fresh```

# Run 
To run as a stand alone \
```cd ~/mcp/mcp-flight-software/ && sudo python main_mcp.py``` \
```cd ~/mcp/mcp-flight-software/ && sudo python main_mcp_light.py``` \
The script should execute for 100 sec, then exit.\
You can download artifacts at \
```~/mcp/mcp-flight-software/artifacts.zip``` 

Check results:
```cd ~/mcp/mcp-flight-software/ && cat telemetry.csv``` \

# Experiments 
Pressure experiment & Leak test\
```cd ~/mcp/mcp-flight-software/ && sudo python main_pressure_experiment.py```
